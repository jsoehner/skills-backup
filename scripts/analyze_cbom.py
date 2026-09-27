#!/usr/bin/env python3
"""
analyze_cbom.py - Analyze CycloneDX Cryptographic Bill of Materials (CBOM)

Reads a CycloneDX CBOM JSON file produced by cdxgen (--include-crypto),
inventories cryptographic assets (algorithms, certificates, keys, protocols),
and flags quantum-vulnerable vs post-quantum safe primitives.
"""

import sys
import json
import argparse
from pathlib import Path
from collections import Counter

import re

QUANTUM_VULNERABLE_PATTERNS = [
    r"\bRSA\b", r"\bECDSA\b", r"\bECDH\b", r"\bDIFFIE[-_ ]?HELLMAN\b",
    r"\bED25519\b", r"\bED448\b", r"\bX25519\b", r"\bX448\b",
    r"\bSECP\d+R1\b", r"(?<![A-Z0-9_-])(?:DSA|DH)(?![A-Z0-9_-])"
]

POST_QUANTUM_PATTERNS = [
    r"\bML[-_]KEM\b", r"\bKYBER\b", r"\bML[-_]DSA\b", r"\bDILITHIUM\b",
    r"\bSLH[-_]DSA\b", r"\bSPHINCS\+?\b", r"\bFALCON\b", r"\bLMS\b", r"\bXMSS\b"
]

SYMMETRIC_CLASSICAL = {
    "AES", "CHACHA20", "3DES", "DES", "BLOWFISH", "RC4", "SHA-256", "SHA-384", "SHA-512", "SHA-3"
}


def analyze_cbom(cbom_path: Path):
    with open(cbom_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    bom_format = data.get("bomFormat", "Unknown")
    spec_version = data.get("specVersion", "Unknown")
    components = data.get("components", [])

    crypto_assets = []
    algorithm_counter = Counter()
    asset_types_counter = Counter()
    vulnerable_assets = []
    pqc_assets = []

    for comp in components:
        comp_type = comp.get("type", "")
        crypto_props = comp.get("cryptoProperties", {})

        asset_type = crypto_props.get("assetType", comp_type or "unknown")
        name = str(comp.get("name") or "Unnamed")
        version = str(comp.get("version") or "N/A")

        asset_info = {
            "name": name,
            "version": version,
            "type": comp_type,
            "asset_type": asset_type,
        }

        # Algorithm properties
        algo_details = crypto_props.get("algorithmProperties", {})
        algo_name = str(algo_details.get("name") or comp.get("name") or "")
        algo_upper = algo_name.upper()

        asset_info["algorithm"] = algo_name
        asset_info["primitive"] = str(algo_details.get("primitive") or "unknown")
        asset_info["key_length"] = str(algo_details.get("parameterSetIdentifier") or algo_details.get("keyLength") or "N/A")

        # Certificate / Protocol properties
        cert_details = crypto_props.get("certificateProperties", {})
        proto_details = crypto_props.get("protocolProperties", {})

        if cert_details:
            asset_info["certificate_subject"] = cert_details.get("subjectName")
            asset_info["certificate_expiry"] = cert_details.get("validTo")

        if proto_details:
            asset_info["protocol_type"] = proto_details.get("type")
            asset_info["protocol_version"] = proto_details.get("version")

        # Classify PQC status (check PQC first so ML-DSA/SLH-DSA are not flagged as classical DSA)
        is_pqc = any(re.search(pat, algo_upper) for pat in POST_QUANTUM_PATTERNS)
        is_qv = any(re.search(pat, algo_upper) for pat in QUANTUM_VULNERABLE_PATTERNS)

        if is_pqc:
            asset_info["pqc_status"] = "POST-QUANTUM READY"
            pqc_assets.append(asset_info)
        elif is_qv:
            asset_info["pqc_status"] = "QUANTUM-VULNERABLE"
            vulnerable_assets.append(asset_info)
        else:
            asset_info["pqc_status"] = "CLASSICAL/SYMMETRIC"

        if crypto_props or comp_type in ("cryptographic-asset", "crypto"):
            crypto_assets.append(asset_info)
            asset_types_counter[asset_type] += 1
            if algo_name:
                algorithm_counter[algo_name] += 1

    return {
        "bomFormat": bom_format,
        "specVersion": spec_version,
        "total_components": len(components),
        "total_crypto_assets": len(crypto_assets),
        "quantum_vulnerable_count": len(vulnerable_assets),
        "pqc_ready_count": len(pqc_assets),
        "asset_types": dict(asset_types_counter),
        "algorithm_distribution": dict(algorithm_counter),
        "vulnerable_assets": vulnerable_assets,
        "pqc_assets": pqc_assets,
        "crypto_assets": crypto_assets
    }


def print_report(summary: dict):
    print("=" * 70)
    print(" CBOM Cryptographic Inventory & PQC Readiness Assessment")
    print("=" * 70)
    print(f"Format: {summary['bomFormat']} (v{summary['specVersion']})")
    print(f"Total Components Scanned: {summary['total_components']}")
    print(f"Identified Cryptographic Assets: {summary['total_crypto_assets']}")
    print(f"Quantum-Vulnerable Assets: {summary['quantum_vulnerable_count']}")
    print(f"Post-Quantum Ready Assets: {summary['pqc_ready_count']}")
    print("-" * 70)

    if summary.get("asset_types"):
        print("\nAsset Types:")
        for atype, count in summary["asset_types"].items():
            print(f"  - {atype}: {count}")

    if summary.get("algorithm_distribution"):
        print("\nAlgorithm Breakdown:")
        for algo, count in summary["algorithm_distribution"].items():
            print(f"  - {algo}: {count}")

    if summary.get("vulnerable_assets"):
        print("\n⚠️ Quantum-Vulnerable Cryptographic Findings (Requires Migration Plan):")
        for asset in summary["vulnerable_assets"][:10]:
            print(f"  • [{asset['pqc_status']}] {asset['name']} (Primitive: {asset['primitive']}, Key/Param: {asset['key_length']})")
        if len(summary["vulnerable_assets"]) > 10:
            print(f"  ... and {len(summary['vulnerable_assets']) - 10} more.")

    if summary.get("pqc_assets"):
        print("\n✅ Post-Quantum Ready Assets Detected:")
        for asset in summary["pqc_assets"]:
            print(f"  • [{asset['pqc_status']}] {asset['name']} ({asset['primitive']})")

    print("=" * 70)


def main():
    parser = argparse.ArgumentParser(description="Analyze CycloneDX CBOM files.")
    parser.add_argument("cbom_file", type=Path, help="Path to CycloneDX CBOM JSON file")
    parser.add_argument("--json", action="store_true", help="Output summary as raw JSON")
    args = parser.parse_args()

    if not args.cbom_file.exists():
        print(f"Error: CBOM file not found: {args.cbom_file}", file=sys.stderr)
        sys.exit(1)

    summary = analyze_cbom(args.cbom_file)

    if args.json:
        print(json.dumps(summary, indent=2))
    else:
        print_report(summary)


if __name__ == "__main__":
    main()

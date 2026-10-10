#!/usr/bin/env python3
"""
update_os_inventory.py - Automatically update the known_cbom_catalog.json with OS-level 
cryptographic components.

This script scans the local operating system for installed packages related to cryptography,
updates the local CBOM catalog, and ensures that the inventory of third-party OS 
binaries is current.
"""

import json
import sys
import subprocess
import os
from pathlib import Path
from typing import List, Dict, Any

def get_installed_packages() -> List[Dict[str, Any]]:
    """Get installed packages based on the OS distribution."""
    packages = []
    try:
        # Try Debian/Ubuntu/Mint/Pop!_OS
        dpkg_output = subprocess.check_output(["dpkg", "-l"], stderr=subprocess.DEVNULL).decode()
        for line in dpkg_output.splitlines():
            if line and not line.startswith("x"):
                parts = line.split()
                if len(parts) >= 3:
                    name = parts[1]
                    version = parts[2]
                    packages.append({"name": name, "version": version})
        return packages
    except (subprocess.CalledProcessError, FileNotFoundError):
        try:
            # Try RHEL/CentOS/Fedora
            rpm_output = subprocess.check_output(["rpm", "-qa", "--queryformat", "%{NAME} %{VERSION}\n"], stderr=subprocess.DEVNULL).decode()
            for line in rpm_output.splitlines():
                parts = line.split()
                if len(parts) >= 2:
                    packages.append({"name": parts[0], "version": parts[1]})
            return packages
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("Warning: Could not detect package manager (dpkg or rpm). Skipping OS inventory update.", file=sys.stderr)
            return []

def update_catalog(catalog_path: Path):
    """Update the known_cbom_catalog.json with OS-specific cryptographic packages."""
    if not catalog_path.exists():
        print(f"Error: Catalog file not found at {catalog_path}", file=sys.stderr)
        return

    with open(catalog_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    installed = get_installed_packages()
    
    # Keywords for cryptographic components
    crypto_keywords = ["ssl", "crypto", "gnutls", "ca-certificates", "ssh", "pkcs"]
    
    new_components = []
    # Keep existing components
    for comp in data.get("components", []):
        if comp.get("category") != "os-runtime": # Keep non-OS components as they are
            new_components.append(comp)

    # Add or update OS components
    os_component_names = set()
    for pkg in installed:
        name = pkg["name"].lower()
        version = pkg["version"]
        if any(kw in name for kw in crypto_keywords):
            # Avoid duplicates
            if name not in os_component_names:
                # Create/Update entry
                # Try to construct a purl
                purl = f"pkg:os:{name}"
                
                # Basic crypto assessment for OS components
                # We assume OS-level crypto is generally quantum-vulnerable unless it's a specific PQC lib
                is_pqc = "pqc" in name or "ml-kem" in name or "ml-dsa" in name or "sphincs" in name
                
                comp_entry = {
                    "name": pkg["name"],
                    "purlPattern": f"^pkg:os:{pkg['name']}$",
                    "category": "os-runtime",
                    "confidence": "HIGH",
                    "source": "OS Inventory Update",
                    "cryptoAssets": [
                        {
                            "name": f"{pkg['name']} Crypto Primitives",
                            "primitive": "library",
                            "algorithm": "Various",
                            "pqc_status": "POST-QUANTUM READY" if is_pqc else "QUANTUM-VULNERABLE",
                            "key_length": "Varies",
                            "remediation": "Ensure package is updated to latest version supporting ML-KEM"
                        }
                    ]
                }
                new_components.append(comp_entry)
                os_component_names.add(name)

    data["components"] = new_components
    
    with open(catalog_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    
    print(f"Successfully updated OS inventory. Added/Updated {len(os_component_names)} components.")

if __name__ == "__main__":
    catalog_path = Path(__file__).parent / "known_cbom_catalog.json"
    update_catalog(catalog_path)

# Cryptographic Bill of Materials (CBOM) & PQC Taxonomy

## Overview

A Cryptographic Bill of Materials (CBOM) extends standard SBOM concepts to identify and catalog all cryptographic assets within an application, repository, or container image. This includes:
- **Algorithms**: Ciphers, digests, signatures, key-exchange mechanisms.
- **Certificates**: X.509 certificates, CA bundles, expiry dates.
- **Keys**: Private/public key pairs, key sizes, parameter sets.
- **Protocols**: TLS versions, SSH, IPsec configurations.
- **Libraries & Dependencies**: OpenSSL, BouncyCastle, cryptography modules.

## CycloneDX Cryptographic Extension (`cryptoProperties`)

Under CycloneDX 1.5+, cryptographic assets are represented with the `cryptoProperties` block:

```json
{
  "bomFormat": "CycloneDX",
  "specVersion": "1.6",
  "components": [
    {
      "type": "cryptographic-asset",
      "name": "RSA-2048",
      "cryptoProperties": {
        "assetType": "algorithm",
        "algorithmProperties": {
          "primitive": "signature",
          "parameterSetIdentifier": "2048",
          "curve": null,
          "executionEnvironment": "software-plain-ram"
        },
        "oid": "1.2.840.113549.1.1.1"
      }
    }
  ]
}
```

## Post-Quantum Cryptography (PQC) Readiness Mapping

| Category | Classical / Vulnerable Primitive | Post-Quantum Replacement (NIST Standard) | Migration Status |
| :--- | :--- | :--- | :--- |
| **Key Encapsulation / KEM** | RSA Encryption, Diffie-Hellman (DH), ECDH (Curve25519, NIST P-256) | **ML-KEM** (FIPS 203, Crystals-Kyber) | Critical Priority |
| **Digital Signatures** | RSA Signatures, ECDSA, Ed25519, DSA | **ML-DSA** (FIPS 204, Crystals-Dilithium), **SLH-DSA** (FIPS 205, SPHINCS+) | High Priority |
| **Stateful Hash-Based Signatures** | Legacy RSA / DSA firmware signing | **LMS** (RFC 8554), **XMSS** (RFC 8391) | Specialized (Firmware / Boot) |
| **Symmetric Encryption** | AES-128, 3DES, Blowfish | **AES-256** (Quantum-resistant against Grover's algorithm) | Recommended bit-length increase |
| **Cryptographic Hash Functions** | MD5, SHA-1, SHA-224 | **SHA-256, SHA-384, SHA-512, SHA-3** | Already Quantum-Resistant |

## Generation Commands Reference

- **Container Image CBOM**:
  ```bash
  cdxgen -t docker --include-crypto -o oss/cbom.json <image-name>
  ```
- **Local Source Code CBOM**:
  ```bash
  cdxgen --include-crypto -o oss/cbom.json <directory>
  ```
- **Java / Maven / Gradle specific scan**:
  ```bash
  cdxgen -t java --include-crypto -o oss/cbom.json
  ```
- **Python scan**:
  ```bash
  cdxgen -t python --include-crypto -o oss/cbom.json
  ```

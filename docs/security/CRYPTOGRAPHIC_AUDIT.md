## 🛡️ Cryptographic Bill of Materials (CBOM) & PQC Migration Assessment

**Format**: CycloneDX (v1.6) | **First-Party Code Crypto Assets**: 1 | **Total Tracked Crypto Assets**: 1

### 📊 Post-Quantum Migration Scorecard

| Metric | Count | Migration Status |
|---|---|---|
| **Post-Quantum Ready (PQC)** | **0** | 🟢 Quantum-Resistant (NIST FIPS 203/204/205) |
| **Quantum-Vulnerable (Backlog)** | **1** | 🔴 At Risk of 'Harvest Now, Decrypt Later' |
| **Classical Symmetric / Hashing** | **0** | 🟡 Classical Security (Requires AES-256 / SHA-256+) |
| **Asymmetric PQC Migration Progress** | **0.0%** | (0 of 1 asymmetric primitives migrated) |

### 🎯 Cryptographic Supply Chain Coverage & Confidence

| Evaluation Layer | Coverage / Status | Audit Confidence Assessment |
|---|---|---|
| **First-Party Code (`src/`)** | **100% Audited** (0 Custom Primitives) | 🟢 **HIGH** (Direct AST & SAST verified clean) |
| **Third-Party Supply Chain** | **0.0%** (0 of 13 dependencies cataloged) | 🔴 LOW (Known profiles assimilated) |
| **Overall Audit Confidence Score** | **7.1%** | **🔴 LOW** (13 unassimilated supply chain dependencies) |

### ✅ Post-Quantum Cryptography Migrated Assets

> ⚠️ **No Post-Quantum Ready assets detected.** Immediate migration planning recommended for asymmetric key exchanges and digital signatures.

### ⚠️ Quantum-Vulnerable Assets & Remediation Plan

| Component / Algorithm | Type / Primitive | Key Length / Curve | Recommended Target | Provenance / Context |
|---|---|---|---|---|
| **`RSA-2048`**<br><sub>RSA-2048</sub> | algorithm / signature | 2048 | **ML-KEM-768 / Kyber (FIPS 203)** | First-Party Code (SAST/AST)<br>`security-governance-orchestrator/templates/pre_commit.py:21`<br><sub><code>(r"-----BEGIN (?:RSA\|EC\|DSA\|OPENSSH) PRIVATE KEY-----", "Private Encryption Key"),</code></sub><br><br>`skills/security-governance-orchestrator/templates/pre_commit.py:21`<br><sub><code>(r"-----BEGIN (?:RSA\|EC\|DSA\|OPENSSH) PRIVATE KEY-----", "Private Encryption Key"),</code></sub> |

### 🔒 Classical Symmetric & Digest Assets

### ⚠️ Unassimilated Third-Party Binaries & Cryptographic Blind Spots

> ℹ️ *The following third-party dependencies do not have verified upstream CBOM attestations in the catalog. They lower the audit confidence score until explicit CBOMs or attestations are published.* 

| Dependency Name | Version | Package URL (purl) | Status |
|---|---|---|---|
| `actions/checkout` | v4 | `pkg:github/actions/checkout@v4` | 🟡 Unassimilated (No upstream CBOM) |
| `actions/checkout` | v7.0.1 | `pkg:github/actions/checkout@v7.0.1` | 🟡 Unassimilated (No upstream CBOM) |
| `actions/setup-python` | v5.6.0 | `pkg:github/actions/setup-python@v5.6.0` | 🟡 Unassimilated (No upstream CBOM) |
| `actions/upload-artifact` | v4.6.2 | `pkg:github/actions/upload-artifact@v4.6.2` | 🟡 Unassimilated (No upstream CBOM) |
| `anchore/sbom-action` | v0.24.2 | `pkg:github/anchore/sbom-action@v0.24.2` | 🟡 Unassimilated (No upstream CBOM) |
| `aquasecurity/trivy-action` | master | `pkg:github/aquasecurity/trivy-action@master` | 🟡 Unassimilated (No upstream CBOM) |
| `cbomkit/cbomkit-action` | v2.3.0 | `pkg:github/cbomkit/cbomkit-action@v2.3.0` | 🟡 Unassimilated (No upstream CBOM) |
| `docker/build-push-action` | v6 | `pkg:github/docker/build-push-action@v6` | 🟡 Unassimilated (No upstream CBOM) |
| `docker/setup-buildx-action` | v3 | `pkg:github/docker/setup-buildx-action@v3` | 🟡 Unassimilated (No upstream CBOM) |
| `gitleaks/gitleaks-action` | v2 | `pkg:github/gitleaks/gitleaks-action@v2` | 🟡 Unassimilated (No upstream CBOM) |
| `semgrep/semgrep-action` | v1 | `pkg:github/semgrep/semgrep-action@v1` | 🟡 Unassimilated (No upstream CBOM) |
| `/home/runner/work/skills-backup/skills-backup/.github/workflows/sbom-cbom.yml` | N/A | `N/A` | 🟡 Unassimilated (No upstream CBOM) |
| `/home/runner/work/skills-backup/skills-backup/.github/workflows/security-testing.yml` | N/A | `N/A` | 🟡 Unassimilated (No upstream CBOM) |

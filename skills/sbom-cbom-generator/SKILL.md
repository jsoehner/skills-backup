---
name: sbom-cbom-generator
group: security_compliance
description: Generate, validate, and manage Software Bill of Materials (SBOM) and Cryptographic Bill of Materials (CBOM) for container images, filesystems, and repositories using tools like Anchore Syft, anchore/sbom-action, cbomkit-action (cbomkit/cbomkit-action), and CycloneDX cdxgen. Trigger when creating or maintaining SBOM/CBOM pipelines, conducting cryptographic asset discovery (PQC migration, certificate and cipher audits), generating SPDX or CycloneDX reports, or setting up GitHub Actions workflow automation for BOM artifacts.
---

# SBOM & CBOM Generator

Provides workflows, automation scripts, and verification procedures to generate Software Bill of Materials (SBOM) and Cryptographic Bill of Materials (CBOM) across local environments and CI/CD pipelines.

## Progressive Disclosure & External Resources

This skill bundles automation scripts and technical references to perform generation and audit tasks without cluttering context:

- **Generation Script**: Execute `bash scripts/generate_boms.sh [OPTIONS] <TARGET>` to generate both SBOM and CBOM for Docker images or local source trees.
- **AST Crypto Scanner & Reconciler**: Run `python3 scripts/scan_crypto_ast.py <REPO_DIR> --cbom <CBOM_PATH>` to perform dual-engine semantic AST discovery across active languages (Python, JS/TS, Go, Java, Rust, C#, C/C++) and guarantee 100% CBOM reconciliation.
- **CBOM Analyzer & PQC Dashboard**: Run `python3 scripts/analyze_cbom.py <path/to/cbom.json>` to inspect cryptographic assets, evaluate algorithm distributions, calculate PQC migration progress percentages, and identify quantum-vulnerable primitives.
- **OS Inventory Update**: Run `python3 scripts/update_os_inventory.py` to scan the local operating system for cryptographic components and update the `known_cbom_catalog.json` inventory. This can be scheduled as a nightly task.
- **Repository Installer**: Run `bash scripts/install_to_repo.sh [OPTIONS] <TARGET_REPO>` to automatically install generation scripts, verification test harness, AST scanner, and GitHub Actions CI workflow into any target repository.
- **BOM Verification Harness**: Run `bash scripts/test_boms.sh [BOM_DIR]` to validate that generated SBOM/CBOM artifacts exist, conform to JSON/CycloneDX schemas, and pass cryptographic audits.
- **Skill Test Suite**: Run `bash tests/run_tests.sh` to run structural validation, CLI checks, and CBOM analyzer unit tests.
- **Workflow Template**: Refer to [references/workflow_template.yml](file://references/workflow_template.yml) for a production-grade, hardened GitHub Actions configuration using `cbomkit/cbomkit-action`.
- **Crypto Taxonomy**: Consult [references/cbom_crypto_taxonomy.md](file://references/cbom_crypto_taxonomy.md) for CycloneDX cryptographic property mappings and Post-Quantum Cryptography (PQC) standards.

---

## Freedom Calibration & Constraints

- **Constraint Level: High**
  - **High Rigidity**: CBOM generation in CI/CD should utilize `cbomkit/cbomkit-action` (or local `--include-crypto`). SBOM and CBOM artifacts must be generated in valid JSON standards (SPDX 2.3+ JSON or CycloneDX 1.5+ JSON).
  - **Medium Freedom**: Output directory paths, image tags, retention policies, and choice of SBOM engine (Syft vs cdxgen) can adapt to project conventions.

---

## Decision Tree: Choosing the Right Strategy

```
What is the target artifact and objective?
 ├─ Container Image (.tar, local docker daemon, or registry tag)
 │   ├─ Generate standard software packages/OS dependencies → Syft / anchore/sbom-action (SPDX-JSON)
 │   └─ Generate cryptographic assets, certs, and ciphers → cdxgen -t docker --include-crypto (CycloneDX)
 ├─ Local Source Code Directory / Repository
 │   ├─ Package-level software dependencies → syft dir:. or cdxgen .
 │   └─ Source code crypto algorithms & dependencies → cbomkit or cdxgen --include-crypto .
 └─ CI/CD Integration
     └─ Use GitHub Actions workflow with anchore/sbom-action + cbomkit/cbomkit-action + actions/upload-artifact
```

---

## Procuring Third-Party Metadata

When vetting third-party commercial or open-source image providers, request their cryptographic metadata directly to avoid the overhead of independent scanning. Ask for:
- **In-Toto Attestation**: Embedded with a `cosign` layer containing the CycloneDX crypto schema.
- **ORAS Attach Payload**: Flagged with the custom artifact type `application/vnd.cyclonedx+json`.

This ensures that you receive cryptographically signed and verified metadata that is ready for ingestion into your CBOM pipeline.

---

## Distribution Strategies


### Production Distribution: OCI Artifacts
For production environments, it is highly recommended to distribute CBOMs as standalone OCI artifacts rather than embedding them within the container image. This follows the **OCI Distribution Specification (v1.1+)** and the **ORAS (OCI Registry As Storage) graph standard**.

**Benefits:**
- **Decoupled Lifecycle**: Update or rotate the CBOM independently of the application image.\n- **Native Registry Integration**: Leverage standard registry tools for querying, listing, and verifying CBOMs.\n- **Admission Control**: Facilitate gatekeeping by allowing security scanners to verify the presence and signature of a linked CBOM artifact before deployment.\n

**Implementation Path:**
1. Generate the CBOM (e.g., `oss/cbom.json`).
2. Use a tool like `oras` or `skopeo` to push the JSON as an OCI artifact to the registry.\n3. Link the CBOM to the image via OCI annotations or by following a deterministic naming convention (e.g., `my-app:v1.0.0-cbom`).

### Aggregation & Merging (CycloneDX 1.6+)

Leverage the global standardization of OWASP CycloneDX 1.6+ to aggregate multiple CBOMs into a unified primary system mapping.

**Strategy:**
- **Tooling**: Use generic CycloneDX aggregation tools (e.g., `bom-merge`) to merge retrieved JSON files from various sources (upstream vendors, internal microservices, etc.).
- **Unified Mapping**: Create a single source of truth for your organization's cryptographic footprint by merging individual component CBOMs into a consolidated master record.
- **Advantage**: Simplifies cross-component vulnerability analysis and PQC migration planning by providing a holistic view of all cryptographic assets in a standard format.

---

## Step-by-Step Execution Procedure



### Step 1: Environment & Tooling Verification

Verify that the required runtimes and command-line tools are available:

1. **Docker Engine**: Required if scanning container images. Verify with `docker info`.
2. **Node.js**: Required for `cdxgen` (Node.js 20+ recommended).
3. **cdxgen**: Install globally via `npm install -g @cyclonedx/cdxgen`.
4. **Syft** (Optional if cdxgen is used as fallback): Install via:
   ```bash
   curl -sSfL https://raw.githubusercontent.com/anchore/syft/main/install.sh | sh -s -- -b /usr/local/bin
   ```

### Step 2: Generate SBOM (Software Bill of Materials)

To generate an SBOM detailing packages, licenses, and operating system packages:

- **Using Syft (SPDX Format - Preferred for Container Images)**:
  ```bash
  syft <IMAGE_NAME> -o spdx-json > oss/sbom.spdx.json
  ```
- **Using cdxgen (CycloneDX Format)**:
  ```bash
  cdxgen -t docker -o oss/sbom.cyclonedx.json <IMAGE_NAME>
  ```
- **From Directory / Source Repository**:
  ```bash
  syft dir:. -o spdx-json > oss/sbom.spdx.json
  ```

### Step 3: Generate CBOM (Cryptographic Bill of Materials)

To inventory all cryptographic algorithms, keys, certificates, and protocols:

- **From Container Image**:
  ```bash
  cdxgen -t docker --include-crypto -o oss/cbom.json <IMAGE_NAME>
  ```
- **From Source Code Directory**:
  ```bash
  cdxgen --include-crypto -o oss/cbom.json <PATH_TO_DIR>
  ```

Alternatively, run the bundled script to execute both steps in a single command:
```bash
bash scripts/generate_boms.sh -t docker -o oss my-demo-app:local
```

### Step 4: Audit & Analyze Cryptographic Inventory & Supply Chain Coverage

Inspect the generated `cbom.json` for security compliance, Post-Quantum Cryptography (PQC) readiness, and third-party supply chain confidence:

```bash
python3 scripts/analyze_cbom.py oss/cbom.json --sbom oss/sbom.cyclonedx.json
```

Examine the findings:
- **First-Party Code Visibility**: Confirms direct AST/SAST scanning across project code (ensuring no custom unvetted crypto).
- **Third-Party Binary CBOM Assimilation**: Ingests known cryptographic profiles from `scripts/known_cbom_catalog.json` (or upstream CBOM attestations) for third-party dependencies (e.g. Tomcat TLS, RabbitMQ AMQPS, Spring WebClient).
- **Audit Confidence Score**: Calculates an overall confidence index based on cataloged/verified dependencies vs unassimilated supply chain blind spots, lowering the score when upstream CBOMs are unavailable.
- **PQC Migration Progress**: Evaluates quantum-vulnerable asymmetric algorithms (`RSA`, `ECDSA`, `ECDH`, `Ed25519`, `DH`) vs post-quantum standards (`ML-KEM`, `ML-DSA`, `SLH-DSA`) with honest zero-baseline handling (`N/A` when no asymmetric assets exist).
- **Classical Symmetric Security**: Confirms symmetric key lengths (recommending `AES-256` / `SHA-256+` for Grover resistance).

### Step 5: Implement CI/CD Workflow with Verification Harness

Integrate into `.github/workflows/sbom-cbom.yml` using the template at [references/workflow_template.yml](file://references/workflow_template.yml):

1. Trigger on `push`, `pull_request`, and `workflow_dispatch`.
2. Restrict workflow permissions: `contents: read`.
3. Use `actions/checkout@v7` to check out repository code.
4. Run `anchore/sbom-action` with pinned commit SHA to generate standard SBOM (`oss/sbom.spdx.json`).
5. Run `cbomkit/cbomkit-action` (pinned commit SHA `34a3d96...` or `@v2`) with `CBOMKIT_OUTPUT_DIR: oss` to generate `oss/cbom.json`.
6. **Automated Verification**: Run `bash scripts/test_boms.sh oss` to assert JSON syntax, CycloneDX compliance, and non-empty crypto components prior to upload.
7. Upload the `oss/` directory using `actions/upload-artifact@v4` with specified retention days.

### Step 6: Add SBOM/CBOM Functionality & Test Harness to Any Repo

To scaffold SBOM/CBOM generation, cryptographic analysis, and the verification test harness into any target repository in a single step:

```bash
bash scripts/install_to_repo.sh [OPTIONS] <TARGET_REPO_PATH>
```

**Options**:
- `-a, --app-name <tag>`: Custom container image tag (default: auto-detected from folder name)
- `-t, --type <docker|dir>`: `docker` for container-based projects or `dir` for directory-based projects (auto-detected if `Dockerfile` is present)

This installs:
- `.github/workflows/sbom-cbom.yml` (configured with automated CI verification)
- `scripts/generate_boms.sh` (local generation utility with `npx` fallback)
- `scripts/analyze_cbom.py` (cryptographic asset & PQC auditor)
- `scripts/test_boms.sh` (automated verification test harness)

---

## Verification & Testing Strategies

To ensure reliability, test the skill across these five distinct layers:

1. **Static Validation & Structure**:
   - Run `python3 tests/validate_skill.py .`.
   - Ensures valid YAML frontmatter, naming conventions, and resource links.
2. **Component Unit Tests**:
   - Run `python3 tests/test_cbom_analysis.py` to test parsing logic against `tests/fixtures/sample_cbom.json`.
   - Verifies accurate identification of quantum-vulnerable algorithms (`RSA`, `ECDSA`), post-quantum primitives (`ML-KEM`, `ML-DSA`), symmetric ciphers (`AES`), and certificates.
3. **CLI Interface Validation**:
   - Run `bash tests/test_generate_script.sh`.
   - Tests parameter parsing, help documentation, target validation, and exit code handling.
4. **End-to-End Test Suite Execution**:
   - Run `bash tests/run_tests.sh` to execute all validation and unit test suites in a single command.
5. **CI/CD Workflow Validation**:
   - Lint workflow syntax using Python `yaml.safe_load` or `actionlint` (if installed).
   - Test locally using [`act`](https://github.com/nektos/act) or in a repository PR branch.

---

## Critical Anti-Patterns (NEVER List)

| Anti-Pattern | Description | Alternative / Solution |
| :--- | :--- | :--- |
| **NEVER** omit `--include-crypto` | Running `cdxgen` without `--include-crypto` produces only a standard SBOM, missing all cryptographic assets. | Always pass `--include-crypto` when generating CBOMs. |
| **NEVER** scan unbuilt or mismatched tags | Scanning a remote tag without building local changes produces stale BOM data. | Build the local container tag first (`docker build -t <tag> .`), then scan that exact tag. |
| **NEVER** run container scans without docker daemon access | Invoking `cdxgen -t docker` inside environments without Docker socket access causes silent failures or empty components. | Verify `docker ps` before running container scans, or fallback to filesystem scan `cdxgen --include-crypto .`. |
| **NEVER** leave BOMs unversioned or unpersisted | Generating BOM files into transient directories without artifact upload prevents compliance auditing. | Archive output directories (e.g. `oss/`) via CI/CD artifact upload with appropriate retention periods. |
| **NEVER** use unpinned actions in production pipelines | Using mutable tags (`@main` or `@v1`) can introduce unexpected supply-chain breaks. | Pin GitHub Actions to immutable full commit SHAs with semantic version comments. |

---

## Common Error Scenarios & Fallbacks

### Scenario 1: `cdxgen: command not found` or Node version incompatibility
- **Root Cause**: Node.js is missing, outdated, or `@cyclonedx/cdxgen` was not installed globally.
- **Fallback**:
  1. Verify Node.js version is 20+: `node -v`.
  2. Install cdxgen: `npm install -g @cyclonedx/cdxgen`.
  3. If permissions prevent global install, run via npx: `npx @cyclonedx/cdxgen -t docker --include-crypto -o oss/cbom.json <IMAGE>`.

### Scenario 2: Docker image inspection fails (`Cannot connect to the Docker daemon`)
- **Root Cause**: Docker daemon is stopped, user lacks socket access permissions, or running inside rootless container without socket mount.
- **Fallback**:
  1. Check Docker status: `sudo systemctl status docker` or `docker info`.
  2. If running in CI without Docker-in-Docker, run `cdxgen` against the project source directory directly (`cdxgen --include-crypto -o oss/cbom.json .`).

### Scenario 3: Empty or minimal CBOM output
- **Root Cause**: The container base image is extremely stripped (e.g., `FROM scratch` or minimal distroless) without inspectable binaries, or the application framework does not expose recognizable crypto libraries.
- **Fallback**:
  1. Scan both the application source repository (`cdxgen --include-crypto .`) and the container image to cross-reference application-level vs OS-level cryptographic assets.
  2. Use `analyze_cbom.py --json oss/cbom.json` to inspect the raw component types.

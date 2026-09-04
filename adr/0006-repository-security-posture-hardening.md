# ADR-0006: Repository Security Posture Assessment and Script Hardening

## Status

Accepted

## Context

The `skills-backup` repository serves as the central source of truth for over 460 modular AI agent skills deployed across various agentic runtimes (e.g., Gemini, Pi, Claude, OpenCode). The repository contains automation scripts (`restore_skills.py`, `sync.py`, `deploy_skills.py`, `import_builtins.py`) that perform local filesystem operations, directory traversal, and inter-client environment synchronization.

A threat modeling (STRIDE) and Static Application Security Testing (SAST) assessment identified several critical areas for hardening:
1. **Path Traversal & Boundary Escapes**: Unvalidated skill directory names and symlink dereferencing during `os.walk` and `shutil.copytree` could allow directory traversal or symlink following attacks.
2. **Destructive File Operation Risks**: In `sync.py`, `shutil.rmtree` could potentially execute destructive deletions if destination paths were tainted or unconfined.
3. **Hardcoded Platform Assumptions**: In `import_builtins.py`, hardcoded Windows system paths prevented cross-platform execution and consistent path validation.
4. **Secrets & Artifact Exposure**: `.gitignore` lacked exclusion patterns for private keys (`*.pem`, `*.key`), API credentials (`credentials.json`, `token.json`), environment files (`.env`), local databases, and temporary artifacts.
5. **JSON Parse Resilience**: `deploy_skills.py` lacked robust error boundaries when parsing external skill manifests.

## Decision

We have implemented a defense-in-depth security hardening model across the entire repository and synchronization toolchain:

1. **Strict Canonical Path Containment (`is_safe_subpath`)**:
   - Both `restore_skills.py` and `sync.py` now enforce canonical path resolution (`os.path.realpath`) and common path boundaries (`os.path.commonpath`) before performing any read, write, copy, or deletion operations.
   - Skill folder names are validated against strict alphanumeric/hyphen/dot regex patterns (`^[a-zA-Z0-9_\-\.]+$`) to block path manipulation.

2. **Symlink Traversal Prevention**:
   - Disabled symlink following in directory walkers (`followlinks=False`).
   - Forced `shutil.copytree(..., symlinks=False)` and `shutil.copy2(..., follow_symlinks=False)` to prevent arbitrary file reading/copying via dangling or out-of-boundary symlinks.
   - Explicitly validated that any symlink targets reside within allowed source boundaries before processing.

3. **Safe Recursive Deletion Guards**:
   - In `sync.py`, before any `shutil.rmtree(dst)` call, `dst` is rigorously verified to reside strictly within the expected client skills directory or repo directory.

4. **Secrets and Artifact Isolation**:
   - Expanded `.gitignore` with comprehensive rules covering certificates, cryptographic private keys, environment secrets, token files, local SQLite databases, virtual environments, and OS/IDE metadata.

5. **Cross-Platform Path Portability**:
   - Standardized path handling in `import_builtins.py` using `os.path.expanduser` instead of hardcoded platform-specific roots.

6. **Error Resilient Manifest Parsing**:
   - Wrapped manifest JSON loading in `deploy_skills.py` with structured try-except blocks to gracefully fallback to atomic skill handling on malformed files.

## Rationale

- **Confidentiality & Integrity**: Prevents accidental leakage of local secrets or manipulation of system files outside the designated skills root.
- **Availability & Resilience**: Eliminates risks of inadvertent data loss from unconstrained `rmtree` calls during bidirectional synchronization.
- **Compliance & Governance**: Aligns with OWASP DevSecOps guidelines, ISO 27001 access boundaries, and the project's Regulated Architecture Decision Record (RADR) standards.

## Consequences

### Positive
- Robust protection against path traversal, symlink injection, and destructive file operations.
- Prevention of accidental secrets commits via hardened Git ignore configurations.
- Seamless, secure cross-platform synchronization for Gemini, Pi, and other agent runtimes.
- Clear audit traceability for compliance and security reviews.

### Negative
- Non-standard skill directory names containing disallowed special characters will be skipped with warning logs (mitigated by naming conventions).

## Related ADRs
- [ADR-0004: Adopt Regulated Architecture Decision Record (RADR) Framework](0004-adopt-regulated-adr-framework.md)
- [ADR-0005: Local Memory RAG Architecture](0005-local-memory-rag-architecture.md)

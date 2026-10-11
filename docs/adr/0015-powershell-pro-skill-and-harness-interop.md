# ADR 0015: Addition of powershell-pro Shell Skill and Harness Interop

## Context
Cross-platform AI harnesses and terminal agents frequently operate in environments where PowerShell (`pwsh` or `powershell.exe`) is the designated primary shell, rather than POSIX shells or Bash. While the repository maintained comprehensive shell skills for Bash (`bash-pro`, `bash-defensive-patterns`) and strict POSIX sh (`posix-shell-pro`), it lacked a dedicated production-grade PowerShell skill.

A reference specification (*PowerShell Master Agent*) was identified in the community ecosystem (`jukeyman-skills`). However, the source specification contained personal author branding, promotional copy, local path artifacts, and unbalanced focus areas that needed refactoring into an objective, idiomatic skill suited for production harnesses.

## Decision
1. Author and integrate a new skill named `powershell-pro` adhering to repository standards (hyphenated naming per ADR-0008, self-contained `SKILL.md`).
2. Scrub author-promotional elements while maintaining transparent attribution and sourcing notes to the upstream community work.
3. Establish defensive PowerShell standards for AI harness agents:
   - Mandatory `$ErrorActionPreference = 'Stop'` and `Set-StrictMode -Version Latest`.
   - `SupportsShouldProcess` (`-WhatIf`/`-Confirm`) support for mutating commands.
   - Cross-platform PowerShell 7+ compatibility alongside Windows PowerShell 5.1 awareness.
   - Integration guidance across CIM/WMI, registry, event logs, .NET interop, Python.NET bridging, and cloud provider modules (`Az`, AWS, GCP).
4. Update `scripts/update_readme.py` and categories so `powershell` skills map to the `software_languages` category.

## Rationale
- **Consistency**: Mirrors the established `*-pro` shell tooling conventions (`bash-pro`, `posix-shell-pro`).
- **Safety**: AI agents running in PowerShell harnesses without defensive defaults frequently fail to catch non-terminating errors or produce brittle string-munging scripts instead of leveraging typed object pipelines.
- **Cross-Harness Interop**: Provides any AI harness operating in PowerShell with immediate, structured context and guardrails.

## Consequences
- **Positive**: Complete coverage of major shell environments (Bash, POSIX sh, PowerShell); enhanced safety and reliability when agents execute in Windows or cross-platform PowerShell sessions; documentation automatically updated across catalog and category files.
- **Negative**: Adds another skill entry to track and synchronize across target client directories.
- **Mitigation**: Managed automatically by existing sync and restore tooling (`restore_skills.py`, `sync.py`, and `update_readme.py`).

## Status
Accepted

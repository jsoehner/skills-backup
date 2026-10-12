# ADR 0016: Fork Guardrail and Pre-Flight Memory Retrieval Protocol

## Context
Autonomous AI agent runtimes (such as Gemini CLI, Pi Agent, Claude Code, and OpenCode) frequently execute across diverse local and remote software repositories. In multi-repository and open-source workflows, two recurring failure modes compromise operational integrity and governance:

1. **Unilateral Fork Divergence**: AI agents operating within a local clone of a forked open-source repository often apply automated dependency updates, architectural refactorings, or unilateral direct commits to the default branch (`main`/`master`). This diverges from the active upstream repository, causing merge friction, breaking sync capabilities, and generating unauthorized modifications in public or shared repositories.
2. **Contextual Amnesia (Lack of Memory Pre-Flight Recall)**: AI agents frequently begin executing tasks, writing code, and altering configurations without querying local memory stores (Organizational Knowledge Framework / OKF policies and ChromaDB vector-indexed lessons learned). This leads to violations of established security baselines, repeating previously resolved bugs, and neglecting organization-wide architectural decisions.

A formalized, machine-executable guardrail and pre-flight briefing protocol was required across all agent workflows and deployment automation.

## Decision
1. **Repository Origin & Fork Guardrail Utility (`scripts/check_fork_guardrail.py`)**:
   - Provide a dedicated, standalone guardrail utility that inspects git remotes (`origin`, `upstream`) and uses the GitHub CLI (`gh repo view --json isFork,parent,pushedAt,isArchived`) to determine whether a target repository is a standalone repository or an active fork.
   - Enforce the **Fork Guardrail**:
     - Standalone repositories: Modifications permitted.
     - Active forked repositories: Direct modifications and unilateral commits on the default branch are **halted**. Agents must refresh via `gh repo sync` or submit improvements upstream via feature pull requests.
     - Abandoned forks (upstream parent archived, deleted, or inactive >18 months): Maintained as adopted forks with modifications permitted under local governance.
2. **Integrated Agent Pre-Flight Briefing Protocol (`scripts/inspect_memory.py --preflight`)**:
   - Enhance the central memory inspector to combine repository fork origin verification, mandatory OKF policy retrieval (e.g. Post-Quantum Cryptography standards, Enterprise Security Baselines, GitHub Actions security governance), and local ChromaDB lessons learned into a single, high-signal pre-flight briefing.
   - Standardize CLI flags across `setup.sh` (`-p`, `--preflight`, `--check-fork`) and `setup.ps1` (`-Preflight`, `-CheckFork`).
3. **Automated Client Governance Synchronization (`scripts/restore_skills.py`)**:
   - Extend skill restoration routines to automatically write and synchronize organizational fork guardrails and memory pre-flight policies into target client configuration directories (`~/.gemini/rules/fork-and-memory-governance.md`, `~/.claude/CLAUDE.md`, `~/.pi/agent/AGENTS.md`, and `~/.opencode/AGENTS.md`).
4. **Master Orchestrator and Skill Schema Hardening**:
   - Mandate Step 1 / Phase 1 pre-flight memory recall and fork guardrail execution across foundational skills and master orchestrators (`repo-governance-orchestrator`, `dependency-lifecycle-orchestrator`, `dependency-updater`, `git-pr-workflows-git-workflow`, `memory-capture`, and `template-skill`).
   - Define strict anti-pattern rules prohibiting unilateral fork updates and pre-flight memory omission.
5. **Global Agent Policy (`AGENTS.md`)**:
   - Elevate the Forked Repository & Upstream Guardrail and Mandatory Memory Pre-Flight Protocol to top-level organizational rules in `AGENTS.md`.

## Rationale
- **Upstream Protection**: Prevents AI agents from unintentionally corrupting forks or diverging from upstream open-source projects.
- **Architectural & Security Consistency**: Guarantees that agent decisions incorporate organizational policies (such as FIPS 203/204 PQC migration, credential hygiene, and pinned actions) and historic lessons learned prior to formulating execution plans.
- **Client Agnostic Enforcement**: Injecting governance into Gemini rules, Claude context, and Pi/OpenCode agents ensures universal enforcement across all supported agent runtimes.

## Consequences
- **Positive**: Eliminates rogue commits on active forks; systematically enforces corporate policies and prior lessons learned; standardizes pre-flight diagnostics across Bash and PowerShell runtimes.
- **Negative**: Adds a brief initial check step before agents commence modifying code.
- **Mitigation**: Pre-flight commands execute in <1 second and cache/fallback gracefully when network or GitHub CLI access is unavailable.

## Status
Accepted

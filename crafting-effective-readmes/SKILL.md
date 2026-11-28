---
name: crafting-effective-readmes
description: Use when writing or improving README files. Not all READMEs are the same — provides templates and guidance matched to your audience and project type.
---

# Crafting Effective READMEs

## Overview

READMEs answer questions your audience will have. Different audiences need different information - a contributor to an OSS project needs different context than future-you opening a config folder.

**Always ask:** Who will read this, and what do they need to know?

## Process

### Step 1: Identify the Task

**Ask:** "What README task are you working on?"

| Task | When |
|------|------|
| **Creating** | New project, no README yet |
| **Adding** | Need to document something new |
| **Updating** | Capabilities changed, content is stale |
| **Reviewing** | Checking if README is still accurate |

### Step 2: Task-Specific Questions

**Creating initial README:**
1. What type of project? (see Project Types below)
2. What problem does this solve in one sentence?
3. What's the quickest path to "it works"?
4. Anything notable to highlight?

**Adding a section:**
1. What needs documenting?
2. Where should it go in the existing structure?
3. Who needs this info most?

**Updating existing content:**
1. What changed?
2. Read current README, identify stale sections
3. Propose specific edits

**Reviewing/refreshing:**
1. Read current README
2. Check against actual project state (package.json, main files, etc.)
3. Flag outdated sections
4. Update "Last reviewed" date if present

### Step 3: Sync GitHub Repository "About" Description

When running this skill during or after repository creation (or when updating a GitHub-hosted repository's README):
1. Check if the repository has a GitHub remote and inspect its current **About → Description** field:
   ```bash
   gh repo view --json description --jq '.description'
   ```
2. **If the Description is empty**, summarize the project into a concise, plain-text 1-sentence summary (no Markdown links, badges, or emojis; under ~160–200 characters) and populate it:
   ```bash
   gh repo edit --description "<brief 1-sentence summary of the project>"
   ```
3. **If a Description already exists**, preserve it unless the user explicitly asks to update it.

### Step 4: Always Ask

After drafting, ask: **"Anything else to highlight or include that I might have missed?"**

## Project Types

| Type | Audience | Key Sections | Template |
|------|----------|--------------|----------|
| **Open Source** | Contributors, users worldwide | Install, Usage, Contributing, License | `templates/oss.md` |
| **Personal** | Future you, portfolio viewers | What it does, Tech stack, Learnings | `templates/personal.md` |
| **Internal** | Teammates, new hires | Setup, Architecture, Runbooks | `templates/internal.md` |
| **Config** | Future you (confused) | What's here, Why, How to extend, Gotchas | `templates/xdg-config.md` |

**Ask the user** if unclear. Don't assume OSS defaults for everything.

## Essential Sections (All Types)

Every README needs at minimum:

1. **Name** - Self-explanatory title
2. **Description** - What + why in 1-2 sentences  
3. **Usage** - How to use it (examples help)

## Progressive Disclosure for Growing Sections (4-Item Rule)

Keep `README.md` scannable as a project matures. Never let repeating operational or historical lists grow unbounded in the root README.

### Gotchas & Troubleshooting (> 4 Entries)
When a project accumulates **more than 4 gotchas or troubleshooting items**:
1. **Extract to a dedicated file:** Create or update `docs/GOTCHAS.md` (or `docs/TROUBLESHOOTING.md`) containing the full list, giving each entry its own `### Heading` so it has a stable Markdown anchor.
2. **Show only the 4 key entries in `README.md`:** Keep only the **latest 4 key/high-impact entries** in `README.md`, each formatted as a brief 1-line summary hyperlinked directly to its anchor in the dedicated file.
3. **Add a "Learn More" paragraph:** Follow the 4-item list with a short paragraph directing readers to the dedicated document for the full catalog.

**Example (`README.md`):**
```markdown
## ⚠️ Gotchas & Troubleshooting

- **[Docker Base Image Java Alignment](docs/GOTCHAS.md#docker-base-image-java-alignment):** Keep Dockerfile JDK/JRE tags matched to the Gradle toolchain version.
- **[Spring Boot 4.2 RabbitMQ Starter](docs/GOTCHAS.md#spring-boot-42-rabbitmq-starter):** Use `spring-boot-starter-rabbitmq` for AMQP 0-9-1 instead of `spring-boot-starter-amqp`.
- **[Log File Volume Mapping](docs/GOTCHAS.md#log-file-volume-mapping):** Pre-create single-file log mounts on the host so Docker does not create a directory.
- **[ChatClient Builder Mutability](docs/GOTCHAS.md#chatclient-builder-mutability):** Build a base `ChatClient` and call `.mutate()` rather than reusing a mutable builder.

To learn more and browse every operational gotcha, root cause, and workaround, visit [docs/GOTCHAS.md](docs/GOTCHAS.md).
```

### Architecture Decision Records — ADRs (> 4 Entries)
Apply the same methodology to the **Architecture Decisions (ADRs)** section when a project has **more than 4 ADRs**:
1. **Maintain the canonical index:** Keep the complete ADR log in the repository's ADR README (e.g., `docs/adr/README.md`), where every entry links to its full ADR document.
2. **Show only the latest 4 key ADRs in `README.md`:** Display only the **last 4 key ADRs**, each with a concise 1-line summary hyperlinked to its entry/section in the ADR README (or the full ADR document via the ADR index) so readers can jump straight to the details.
3. **Add a "Learn More" paragraph:** Follow the 4-item list with a short paragraph pointing readers to the ADR README to explore the full decision history.
4. **Consolidate:** Do not scatter separate ADR sections across the README; keep a single concise ADR section.

**Example (`README.md`):**
```markdown
## 📐 Architecture Decisions (ADRs)

- **[ADR-0032: Natural Sentence Cadence](docs/adr/README.md#index-of-architectural-decisions)** ([Full ADR](docs/adr/0032-eliminate-trailing-adverb-padding-and-restore-natural-cadence.md)) — Removes trailing adverb padding to restore natural prose rhythm.
- **[ADR-0031: Nightly Dependency Auto-Merge](docs/adr/README.md#index-of-architectural-decisions)** ([Full ADR](docs/adr/0031-automated-nightly-dependency-updates-and-unattended-auto-merge.md)) — Governs unattended nightly dependency updates and auto-merge gates.
- **[ADR-0030: SBOM/CBOM & PQC Governance](docs/adr/README.md#index-of-architectural-decisions)** ([Full ADR](docs/adr/0030-automated-sbom-cbom-supply-chain-governance.md)) — Automates supply chain SBOM/CBOM auditing and PQC readiness scoring.
- **[ADR-0029: Consolidate Security Workflows](docs/adr/README.md#index-of-architectural-decisions)** ([Full ADR](docs/adr/0029-consolidate-security-workflows-and-remove-redundant-testing-workflow.md)) — Standardizes CI security scanning into a single governance workflow.

To learn more about the project's full architectural and security decision history, visit the complete ADR index in [docs/adr/README.md](docs/adr/README.md).
```

## Anti-Patterns

| Avoid | Why | Instead |
|-------|-----|---------|
| Vague/Stale Instructions | Misleads users, creates setup friction | Keep commands matching `package.json` |
| Empty Placeholder Sections | Looks unfinished and sloppy | Remove TBD sections entirely |
| Generic tutorials | Wastes tokens | Explain specific installation steps |
| Unbounded Gotchas or ADR Lists (> 4 items) | Bloats the README and buries setup/usage info | Show only the latest 4 key items with brief hyperlinked summaries + a closing paragraph linking to `docs/GOTCHAS.md` or `docs/adr/README.md` |

## References & Templates

**MANDATORY - LOADING TRIGGERS**:
- Once the user confirms the project type, you **MUST** read the corresponding template file, such as `templates/internal.md` or `templates/oss.md`.
- Before editing or formatting, you **MUST** read [style-guide.md](style-guide.md) to inspect common phrasing errors.
- **Do NOT load** external templates or references for simple config README files.

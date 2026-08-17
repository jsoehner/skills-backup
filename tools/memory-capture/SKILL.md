---
name: memory-capture
description: Automatically classify and route agent outputs, findings, policies, or troubleshooting logs into OKF or ChromaDB RAG.
---

# Memory Capture Skill

Use this skill whenever you synthesize key findings, architecture decisions, coding standards, bug root causes, or reusable technical knowledge during a task.

## Initialization & Setup

Before using memory storage for the first time on a new system or harness, initialize the required directories and ChromaDB persistent collection:

```bash
python C:\Users\jsoehner\memory_system\init_storage.py
```

This will automatically create:
- **ChromaDB Storage**: `C:\Users\jsoehner\memory_system\db`
- **OKF Storage**: `C:\Users\jsoehner\memory_system\knowledge\okf`
- **Inbox Directories**: `C:\Users\jsoehner\memory_system\inbox\` (`processed/`, `error/`)

---

## Instructions for AI Harnesses

When completing a task or documenting a decision:

1. **Format the Output**:
   Write the knowledge summary into a temporary file or directly into `C:\Users\jsoehner\memory_system\inbox\<filename>.md`.

2. **Specify Classification Hint (Optional Header)**:
   Add a header at the top of the file to guide routing if necessary:
   - For **Source of Truth / Rules / Policies**:
     ```markdown
     # OKF Decision
     Type: Policy / Architecture Standard
     Summary: ...
     ```
   - For **Logs / Bug Fixes / Technical Snippets**:
     ```markdown
     # Chroma Context
     Type: Troubleshooting / Bug Report
     Summary: ...
     ```

3. **Trigger Processing**:
   Run the capture command directly from the shell:
   ```bash
   python C:\Users\jsoehner\memory_system\capture_knowledge.py <path_to_file>
   ```
   Or place the file into `C:\Users\jsoehner\memory_system\inbox/` for automatic background processing.

## Classification Standard
- **OKF (`./knowledge/okf`)**: High-level rules, team standards, architectural design decisions, and security policies.
- **CHROMA (`./db`)**: Specific bug fixes, terminal outputs, error tracebacks, API snippets, and step-by-step guides.

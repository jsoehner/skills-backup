---
name: memory-capture
description: Automatically classify, route, and retrieve agent outputs, findings, policies, or troubleshooting logs into OKF or ChromaDB RAG.
---

# Memory Capture & Retrieval Skill

Use this skill whenever you synthesize key findings, architecture decisions, coding standards, bug root causes, or reusable technical knowledge during a task, or when querying historical agent memory.

## Initialization & Setup

Before using memory storage for the first time on a new system or harness, initialize the required directories and ChromaDB persistent collection:

```bash
python ~/memory_system/init_storage.py
```

This will automatically create:
- **ChromaDB Storage**: `~/memory_system/db`
- **OKF Storage**: `~/memory_system/knowledge/okf`
- **Inbox Directories**: `~/memory_system/inbox/` (`processed/`, `error/`)

---

## Instructions for AI Harnesses

### 1. Ingestion & Classification

When completing a task or documenting a decision:

1. **Format the Output**:
   Write the knowledge summary into a temporary file or directly into `~/memory_system/inbox/<filename>.md`.

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
   python /capture_knowledge.py <path_to_file>
   ```
   Or place the file into `~/memory_system/inbox//` for automatic background processing.

### 2. Memory Retrieval Architecture (RAG Integration)

When querying historical agent memory:

- **OKF Direct Search (Rules & Policies)**: Perform keyword or regex search across `~/memory_system/knowledge/okf\*.md` for deterministic architectural policies and rules.
- **Chroma Vector Retrieval (Troubleshooting & Context)**: Query the persistent ChromaDB collection at `~/memory_system/db` using semantic similarity search (chunk size: 500–1000 tokens, 150 token overlap).
- **Metadata Filtering**: Filter vector queries using `filter={"type": "Troubleshooting"}` or `filter={"type": "Policy"}` to isolate specific domain contexts.

## Classification Standard
- **OKF (`~/memory_system/knowledge/okf`)**: High-level rules, team standards, architectural design decisions, and security policies.
- **CHROMA (`~/memory_system/db`)**: Specific bug fixes, terminal outputs, error tracebacks, API snippets, and step-by-step guides.

## 6) Memory Sync

After completing a task, key decision, or report, you **MUST** trigger the local memory capture. 

1. Save the final document, report, or summary as a Markdown file in the project directory.
2. Invoke the capture script: 
   ```bash
   python $MEMORY_SYSTEM_ROOT\capture_knowledge.py <file_path>
   ```
3. This ensures that new requirements, technical standards, and findings are automatically routed to the correct storage (OKF or ChromaDB).


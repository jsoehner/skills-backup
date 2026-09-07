# 0005. Local Memory RAG Architecture and Zero-Cloud Token Injection

* Status: accepted
* Deciders: jsoehner, AI Assistance Team
* Date: 2026-08-20

## Technical Story
* Issue / Request: Review, categorize, and deploy local memory RAG integration for AI harnesses with zero-cloud token pre-prompt injection.

## Context and Problem Statement
AI harness models (Gemini, Claude, OpenCode) require consistent historical memory, technical policies, and troubleshooting knowledge across sessions. Uploading entire codebases or long documentation files into every prompt consumes massive token context windows and incurs unnecessary cloud LLM token costs.

## Decision Drivers
* **Token Cost & Latency**: Minimize cloud LLM token costs by fetching only top-K relevant context before sending API requests.
* **Deterministic vs. Semantic Retrieval**: Need a split mechanism for exact policy rules (zero hallucination) versus fuzzy troubleshooting snippets.
* **Local Privacy**: Keep indexed vectors and embedding generation 100% on the local host.

## Decision Outcome
Chosen option: **Dual-Store Local Memory System (`~/memory_system`)**.

1. **Deterministic Store (OKF)**: High-level architectural rules and policies are routed to `~/memory_system/knowledge/okf/*.md` for deterministic keyword/regex matching.
2. **Semantic Store (ChromaDB)**: Troubleshooting notes, error logs, and code snippets are embedded locally into ChromaDB at `~/memory_system/db/` using local ONNX embeddings (`all-MiniLM-L6-v2`).
3. **Automated Inbox Daemon**: Background user service `memory-inbox.service` monitors `~/memory_system/inbox/` for continuous background file processing.
4. **Pre-Prompt Injection**: Local RAG retrieves relevant context and injects it into prompt payloads *before* transmitting tokens to frontier cloud models.

### Positive Consequences
* Reduces cloud LLM token consumption by injecting only targeted memory chunks (500–1000 tokens).
* Preserves zero cloud token cost for local retrieval and embedding generation.
* Ensures strict policy compliance via OKF file matching alongside fuzzy semantic vector search.

### Negative Consequences
* Requires running a background user daemon (`memory-inbox.service`) on the local OS.
* Initial ingestion requires local Disk I/O and storage for ChromaDB SQLite indices.

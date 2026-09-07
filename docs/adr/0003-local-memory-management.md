# ADR-0003: Local Memory Management (LanceDB)

## Status
Accepted

## Context
We need a way to store and retrieve long-term memories (user preferences, engineering lessons, project facts) across sessions. We want to avoid the high costs and potential latency of paid cloud-based vector services.

## Decision
We will implement a local memory management system using LanceDB and `sentence-transformers`.

## Rationale
- **Cost**: LanceDB is free and open-source.
- **Performance**: LanceDB is a high-performance vector database designed for speed and scalability.
- **Privacy**: Data remains local to the execution environment.
- **Simplicity**: Easy to integrate with existing Python workflows.

## Consequences
- **Pros**: Zero cost for memory storage, high-speed semantic search, and local data control.
- **Cons**: Requires local storage space and local CPU/GPU for embedding generation.

## Related ADRs
- ADR-0001: Use PostgreSQL as Primary Database
- ADR-0002: Caching Strategy (Redis)

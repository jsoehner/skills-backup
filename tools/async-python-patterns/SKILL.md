---
name: async-python-patterns
description: Master Python asyncio, concurrent programming, and async/await patterns for high-performance applications. Use when building async APIs, concurrent systems, or I/O-bound applications requiring non-blocking operations.
---

# Async Python Patterns

Comprehensive guidance for implementing asynchronous Python applications using asyncio, concurrent programming patterns, and async/await for building high-performance, non-blocking systems.

## Use this skill when

- Building async web APIs (FastAPI, aiohttp, Sanic)
- Implementing concurrent I/O operations (database, file, network)
- Creating web scrapers with concurrent requests
- Developing real-time applications (WebSocket servers, chat systems)
- Processing multiple independent tasks simultaneously
- Building microservices with async communication
- Optimizing I/O-bound workloads
- Implementing async background tasks and queues

## Do not use this skill when

- The workload is CPU-bound with minimal I/O.
- A simple synchronous script is sufficient.
- The runtime environment cannot support asyncio/event loop usage.

## Instructions

- Clarify workload characteristics (I/O vs CPU), targets, and runtime constraints.
- Pick concurrency patterns (tasks, gather, queues, pools) with cancellation rules.
- Add timeouts, backpressure, and structured error handling.
- Include testing and debugging guidance for async code paths.
- If detailed examples are required, open `resources/implementation-playbook.md`.

Refer to `resources/implementation-playbook.md` for detailed patterns and examples.

## Resources

- `resources/implementation-playbook.md` for detailed patterns and examples.

## Anti-Patterns

- NEVER execute blocking I/O calls (like standard `requests` or `time.sleep`) inside an async event loop thread; use `asyncio.to_thread` or non-blocking libraries.
- NEVER use `asyncio.gather` without setting explicit timeouts or handling individual task exceptions.

## 6) Memory Sync

After an async system design, concurrent workload analysis, or non-blocking I/O optimization is completed, you **MUST** trigger the local memory capture. 

1. Save the final async architecture, concurrency plan, or I/O optimization report as a Markdown file in the project directory.
2. Invoke the capture script: 
   ```bash
   python $MEMORY_SYSTEM_ROOT\capture_knowledge.py <file_path>
   ```
3. This ensures that async patterns, concurrency strategies, and non-blocking I/O plans are automatically routed to the correct storage (OKF or ChromaDB).


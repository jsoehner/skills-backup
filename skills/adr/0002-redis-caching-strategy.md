# ADR-0002: Caching Strategy (Redis)

## Status
Accepted

## Context
To improve system performance and reduce database load, we need a high-speed, in-memory data store for frequently accessed data, session management, and rate limiting.

## Decision
We will use Redis as our primary caching layer.

## Rationale
- **Speed**: Sub-millisecond latency for read/write operations.
- **Versatility**: Supports strings, hashes, lists, sets, and sorted sets.
- **Pub/Sub**: Useful for real-time notifications and event-driven patterns.
- **Persistence**: Options for RDB and AOF ensure data durability where needed.

## Consequences
- **Pros**: Significant reduction in primary database load, faster response times for common queries.
- **Cons**: Introduces complexity in cache invalidation and requires monitoring of memory usage.

## Related ADRs
- ADR-0001: Use PostgreSQL as Primary Database

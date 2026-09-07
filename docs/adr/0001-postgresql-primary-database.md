# ADR-0001: Use PostgreSQL as Primary Database

## Status
Accepted

## Context
We need a primary relational database to handle structured data, maintain ACID compliance, and support complex queries for user profiles, transactions, and system configuration.

## Decision
We will use PostgreSQL as our primary relational database.

## Rationale
- **ACID Compliance**: Ensures data integrity for critical transactions.
- **Extensibility**: Strong support for JSONB, indexing, and complex joins.
- **Ecosystem**: Mature tooling, excellent community support, and high availability options (e.g., RDS, Cloud SQL).
- **Scalability**: Proven ability to handle large datasets and high concurrency.

## Consequences
- **Pros**: Reliable data consistency, rich feature set, and strong community support.
- **Cons**: Requires careful schema design and indexing to maintain performance as data grows.

## Related ADRs
- ADR-0002: Caching Strategy (Redis)
- ADR-0005: Search Architecture

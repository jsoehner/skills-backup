# Current State of Architecture

## Overview
The system is designed as a high-performance, scalable, and maintainable platform leveraging a modern cloud-native stack. It emphasizes local-first memory management, robust architectural governance, and a consistent brand identity.

## Core Technology Stack
- **Frontend**: Next.js 15 / React 19 with Tailwind CSS.
- **Backend**: Python 3.12+ with FastAPI.
- **Primary Database**: PostgreSQL (ACID compliant, relational).
- **Caching**: Redis (high-speed key-value storage).
- **Local Memory**: LanceDB with `sentence-transformers` for local, free, and performant vector search and semantic memory.
- **Orchestration**: Kubernetes for container orchestration and Temporal for durable workflow management.

## Architectural Patterns
- **Monorepo Management**: Managed via Nx/Turborepo for efficient builds and shared dependency handling.
- **Design Patterns**: Implements Clean Architecture, Hexagonal Architecture, and Domain-Driven Design (DDD) principles.
- **Workflow Orchestration**: Temporal-based saga patterns for distributed transactions and long-running processes.
- **Architecture Governance**: Decision-making is formalized through Architecture Decision Records (ADRs) and C4 modeling.

## Brand & Design System
- **Identity**: YUV.AI brand identity.
- **Design System**: Custom-built system including design tokens, component libraries, and accessibility standards.
- **Visual Language**: "Fly High" motifs, phoenix mark, and specific color palettes (Neon, Decks, Warm Editorial).

## Memory & Context Management
- **Local-First**: Replaced paid cloud-based vector services with a local LanceDB implementation.
- **Batch Consolidation**: Active process of consolidating skills and memories to optimize context window usage and reduce token costs.
- **Session Handoff**: Structured system for transferring state between AI agent sessions.

## Roadmap & Governance
- **ADRs**: All significant technical decisions are logged in the `docs/adr/` directory.
- **Documentation**: Automated and manual documentation generation for APIs, runbooks, and system diagrams.
- **Security**: Integrated SAST, threat modeling, and compliance checks (GDPR, etc.).

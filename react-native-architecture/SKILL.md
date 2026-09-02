---
name: react-native-architecture
description: Build production React Native apps with Expo, navigation, native modules, offline sync, and cross-platform patterns. Use when developing mobile apps, implementing native integrations, or architecting React Native projects.
---

# React Native Architecture

Production-ready patterns for React Native development with Expo, including navigation, state management, native modules, and offline-first architecture.

## Use this skill when

- Starting a new React Native or Expo project
- Implementing complex navigation patterns
- Integrating native modules and platform APIs
- Building offline-first mobile applications
- Optimizing React Native performance
- Setting up CI/CD for mobile releases

## Do not use this skill when

- The task is unrelated to react native architecture
- You need a different domain or tool outside this scope

## Instructions

- Clarify goals, constraints, and required inputs.
- Apply relevant best practices and validate outcomes.
- Provide actionable steps and verification.
- If detailed examples are required, open `resources/implementation-playbook.md`.

## Resources

- `resources/implementation-playbook.md` for detailed patterns and examples.

## Anti-Patterns

- NEVER load massive datasets directly into client memory; use pagination or infinite scroll.
- NEVER use generic, unstyled components or default browser styling in production-ready UIs.

## 6) Capture Knowledge

After the React Native architecture or mobile-specific pattern is finalized, automatically trigger the `capture_knowledge.py` script.
The script will analyze the mobile architecture, navigation flow, and native integration points to identify:
- New cross-platform architectural patterns or native module interfaces.
- Offline-first sync strategies and local storage schemas.
- Mobile-specific performance optimizations or navigation optimizations.
The script will then route this information to the appropriate storage:
- **OKF**: High-level mobile architecture rules, navigation standards, and cross-platform policies.
- **ChromaDB**: Specific native module definitions, offline sync logic, and mobile-specific configuration details.
",path:
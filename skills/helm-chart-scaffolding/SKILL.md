---
name: helm-chart-scaffolding
description: Design, organize, and manage Helm charts for templating and packaging Kubernetes applications with reusable configurations. Use when creating Helm charts, packaging Kubernetes applications, or implementing templated deployments.
---

# Helm Chart Scaffolding

Expert guidance for creating production-ready, reusable, and maintainable Helm charts for Kubernetes applications.

## Use this skill when

- Creating a new Helm chart from scratch
- Scaffolding a multi-component application (e.g., app, service, ingress)
- Designing reusable Helm libraries or common subcharts
- Implementing environment-specific configurations (dev, staging, prod)
- Packaging applications for distribution

## Do not use this skill when

- You are only deploying a single, static manifest (use `kubectl apply`)
- You are managing raw Kubernetes manifests without templating

## Instructions

- Clarify requirements (deployment type, scaling, secrets, networking)
- Apply best practices for Helm templates and Kustomize integration
- Provide actionable steps and verification.

## Purpose

Create production-ready Helm charts that follow industry standards, minimize duplication, and provide clear configuration interfaces.

## Core Capabilities

1. **Chart Structure**: Designing logical folder structures for values, templates, and helpers.
2. **Template Design**: Writing clean, maintainable Go templates with proper logic and scoping.
3. **Value Management**: Implementing hierarchical values (global vs. local) and environment-specific overrides.
4. **Dependency Management**: Managing subcharts and external dependencies.
5. **Reusable Logic**: Creating helper functions and named templates for common patterns (e.g., labels, annotations).

## Design Principles

### 1. DRY (Don't Repeat Yourself)
- Use `_helpers.tpl` for common labels, selectors, and names.
- Use `range` and `with` blocks to avoid repeated logic.
- Abstract common configurations into subcharts or shared values.

### 2. Clarity & Predictability
- Use clear, descriptive names for values (e.g., `replicaCount` vs `count`).
- Provide sensible defaults in `values.yaml`.
- Group related values together (e.g., `service.port`, `service.type`).

### 3. Scalability & Flexibility
- Support for multiple replicas, resources, and environment variables.
- Easy overrides for different environments (dev, prod).
- Support for secrets (ExternalSecrets, SealedSecrets, or env vars).

## Chart Structure

### Standard Layout

```text
my-chart/
├── Chart.yaml           # Metadata (version, name, description)
├── values.yaml          # Default configuration values
├── charts/              # Subcharts (dependencies)
├── templates/           # Kubernetes manifest templates
│   ├── _helpers.tpl     # Named templates (helpers)
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── ingress.yaml
│   ├── hpa.yaml
│   └── secrets.yaml
├── .helmignore          # Files to ignore during packaging
├── README.md            # Documentation and installation guide
└── tests/               # Helm unit tests (optional)
```

### Helper Templates (`_helpers.tpl`)

```yaml
{{/* Standard labels for all resources */}}
{{- define "my-app.labels" -}}
app.kubernetes.io/name: {{ .Chart.Name }}
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/component: {{ .Values.component }}
app.kubernetes.io/part-of: {{ .Values.appName }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/* Standard name template */}}
{{- define "my-app.fullname" -}}
{{- printf "%s-%s" .Release.Name .Chart.Name | trunc 63 | trimSuffix "-" -}}
{{- end }}
```

## Deployment Patterns

### 1. Environment Overrides

Use `values.yaml` for defaults and `values-dev.yaml`, `values-prod.yaml` for environment-specific overrides.

```bash
helm install my-app ./my-chart -f values.yaml -f values-prod.yaml
```

### 2. Subcharts

For complex applications, break out components into subcharts (e.g., a database or redis instance) to allow independent versioning and configuration.

### 3. Secret Management

Avoid plain-text secrets in `values.yaml`. Use:
- **ExternalSecrets**: Fetch from AWS SM, GCP SM, or HashiCorp Vault.
- **SealedSecrets**: Encrypted secrets stored in Git.
- **Env Vars**: Pass sensitive data via `--set` (only for CI/CD).

## Best Practices

- **Pin Versions**: Always pin chart versions and dependency versions.
- **Validate Schemas**: Use `values.schema.json` to validate input.
- **Use Labels**: Ensure consistent labeling for monitoring and selection.
- **Resource Limits**: Always include `resources` (requests/limits) in templates.
- **Liveness/Readiness**: Always define probes.
- **Helm Lint**: Run `helm lint` and `helm install --dry-run` frequently.

## Quality Standards

1. **Completeness**: All required K8s resources are templated.
2. **Maintainability**: Templates are readable and not overly complex.
3. **Scalability**: Supports dynamic replicas, images, and ports.
4. **Security**: Follows least-privilege principles for RBAC and PodSecurity.
5. **Documentation**: `README.md` is clear and includes example `values.yaml`.

## Reference Building Process

1. **Requirement Analysis**: Define app requirements (port, replicas, secrets).
2. **Structure Design**: Create the directory tree and `Chart.yaml`.
3. **Template Authoring**: Write manifests with `_helpers.tpl` integration.
4. **Values Definition**: Populate `values.yaml` with defaults and types.
5. **Validation**: Run `helm lint` and `helm install --dry-run`.
6. **Documentation**: Create the installation guide and examples.

## Best Practices

- Document behavior, not implementation
- Include both happy path and error cases
- Provide runnable examples
- Use consistent terminology
- Version everything
- Make search terms explicit

## Anti-Patterns

- NEVER hardcode secrets in `values.yaml`.
- NEVER use `{{ .Values.something }}` without checking if it's set or providing a default.
- NEVER create monolithic charts; use subcharts for independent components.
- NEVER skip `helm lint` before pushing a chart.

## 6) Capture Knowledge


## Memory Sync

After completing key technical findings, architectural decisions, code refactorings, or risk assessments, you **MUST** trigger the local memory capture.

1. Save the final summary or artifact as a Markdown file in the project directory.
2. Invoke the capture script:
   ```bash
   python3 ~/memory_system/capture_knowledge.py <file_path>
   ```
3. This ensures that new learnings, policies, and technical snippets are automatically routed to the correct local storage (OKF or ChromaDB).

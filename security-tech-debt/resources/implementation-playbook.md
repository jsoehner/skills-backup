# Security Tech Debt Management Playbook

This playbook provides actionable patterns, mathematical quantification models, assessment checklists, and templates for identifying and eliminating security technical debt.

---

## 1. Security Debt Taxonomy (5 Dimensions)

```
                              ┌────────────────────────────────────────┐
                              │          Security Tech Debt            │
                              └───────────────────┬────────────────────┘
          ┌─────────────────────┬─────────────────┼─────────────────┬─────────────────────┐
          ▼                     ▼                 ▼                 ▼                     ▼
    [1. Code & CWE]      [2. Supply Chain] [3. Architecture] [4. Cloud & Infra]   [5. Governance/Process]
    - Hardcoded Secrets  - Outdated SCA    - Broken Auth/RBAC- Permissive IAM     - Expired Risk Waivers
    - Injection Flaws    - EOL Runtimes    - Insecure Comms  - Unencrypted Storage- Lingering Pentest Gaps
    - Missing Input Val  - Vulnerable Pkg  - Leaky Boundaries- Exposed Ports      - Unpatched Systems
```

### Dimension 1: Code-Level Vulnerabilities & Flaws (CWEs)
- **Hardcoded Secrets & Tokens**: Passwords, private keys, API credentials in source or config files.
- **Injection Flaws**: Dynamic query composition (SQLi, Command Injection, LDAP injection).
- **Broken Cryptography**: Weak ciphers (DES, RC4, MD5, SHA1), custom cryptographic algorithms, hardcoded IVs/seeds.
- **Inadequate Input Sanitization**: Missing type validation, unrestricted file uploads, missing output encoding (XSS).

### Dimension 2: Supply Chain & Dependency Debt
- **Vulnerable Direct/Transitive Dependencies**: Known CVEs lingering in third-party libraries.
- **End-of-Life (EOL) Runtimes & Frameworks**: Framework versions unsupported by upstream vendors.
- **Abandoned / Unmaintained Packages**: Libraries with no commits or security maintainers for >24 months.
- **Missing Software Bill of Materials (SBOM)**: Inability to trace component provenance and licenses.

### Dimension 3: Architectural Security Debt
- **Legacy Authentication / Session Schemes**: Basic auth, non-expiring session tokens, unvalidated JWT algorithms (`none` algorithm).
- **Missing / Inconsistent Authorization**: Insecure Direct Object References (IDOR), missing multi-tenant scoping.
- **Monolithic Trust Boundaries**: Flat internal networks without micro-segmentation or mTLS.
- **Missing Telemetry & Audit Trails**: Inability to reconstruct attacker activity due to insufficient logging.

### Dimension 4: Infrastructure & Cloud Configuration Debt
- **Over-Privileged IAM Roles**: `*` permissions, wildcard resource policies, long-lived access keys.
- **Unencrypted Data Stores**: Unencrypted databases, EBS/PersistentVolumes, or S3/GCS buckets.
- **Publicly Exposed Services**: Database ports (5432, 3306, 6379) or internal dashboards exposed directly to the internet.
- **Container & OS Drift**: Outdated base container images with critical OS-level CVEs.

### Dimension 5: Governance, Process & Audit Debt
- **Expired Risk Waivers**: Security exceptions granted without renewal or sunset plans.
- **Lingering Penetration Testing & Bug Bounty Findings**: Unresolved remediation items beyond 90 days.
- **Non-Compliant Data Retention**: Failure to purge expired PII or compliance-regulated customer data.

---

## 2. Quantitative Scoring & Impact Models

### 2.1 Security Debt Index (SDI)
To compute an aggregate risk score across a codebase or service portfolio:

$$\text{SDI} = \sum_{i=1}^{N} \Big( \text{CVSS}_i \times \text{EPSS}_i \times \text{AgeWeight}_i \Big)$$

Where:
- **$\text{CVSS}_i$**: Vulnerability Base Score (0.0 to 10.0).
- **$\text{EPSS}_i$**: Exploit Prediction Scoring System probability (0.0 to 1.0) indicating probability of exploitation in the wild.
- **$\text{AgeWeight}_i$**: Multiplier based on days outstanding past SLA:
  - $\le 30\text{ days}$: $1.0\times$
  - $31 - 90\text{ days}$: $1.5\times$
  - $91 - 180\text{ days}$: $2.5\times$
  - $> 180\text{ days}$: $4.0\times$

### 2.2 Financial Risk Exposure: Annual Loss Expectancy (ALE)

$$\text{ALE} = \text{SLE} \times \text{ARO}$$

- **Single Loss Expectancy (SLE)**: Asset Value $\times$ Exposure Factor (incident response + fines + downtime + reputation loss).
- **Annual Rate of Occurrence (ARO)**: Likelihood probability derived from threat exposure and EPSS.

---

## 3. Prioritized Remediation Roadmap Model

```
                    ┌──────────────────────────────────────────────┐
                    │               EFFORT / COST                  │
                    │         LOW                   HIGH           │
   ┌──────────────┬─┼──────────────────────┬───────────────────────┤
   │              │ │   QUICK WINS         │   STRATEGIC REDESIGN  │
   │  HIGH /      │ │ - Dependency bumps   │ - Zero-Trust Network  │
   │  CRITICAL    │ │ - Secret removal     │ - Auth/SSO Migration  │
   │              │ │ - SQL param binding  │ - Tenant IAM Isolation│
   │ IMPACT /     ├─┼──────────────────────┼───────────────────────┤
   │ RISK         │ │   HYGIENE / MINOR    │   DE-PRIORITIZE       │
   │              │ │ - Security headers   │ - Low-risk legacy     │
   │  LOW         │ │ - Non-sensitive EOL  │   patterns in dormant │
   │              │ │   patching           │   isolated services   │
   └──────────────┴─┴──────────────────────┴───────────────────────┘
```

---

## 4. Programmatic Security Debt Analyzer (Python Template)

```python
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Dict, Optional
import datetime

class DebtCategory(Enum):
    CODE_CWE = "code_cwe"
    SUPPLY_CHAIN = "supply_chain"
    ARCHITECTURE = "architecture"
    CLOUD_INFRA = "cloud_infra"
    GOVERNANCE = "governance"

class Severity(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4

@dataclass
class SecurityDebtItem:
    id: str
    title: str
    category: DebtCategory
    severity: Severity
    cvss: float
    epss: float  # 0.0 to 1.0
    discovered_date: datetime.date
    sla_days: int = 30
    remediation_effort_hours: float = 8.0
    estimated_cost_to_fix: float = 1200.0  # USD
    mitigation_notes: str = ""

    @property
    def age_days(self) -> int:
        return (datetime.date.today() - self.discovered_date).days

    @property
    def is_sla_breached(self) -> bool:
        return self.age_days > self.sla_days

    @property
    def age_weight(self) -> float:
        if self.age_days <= 30:
            return 1.0
        elif self.age_days <= 90:
            return 1.5
        elif self.age_days <= 180:
            return 2.5
        return 4.0

    @property
    def risk_score(self) -> float:
        return round(self.cvss * self.epss * self.age_weight, 2)

    @property
    def roi_score(self) -> float:
        """Risk reduction per dollar invested."""
        return round((self.risk_score * 1000) / max(self.estimated_cost_to_fix, 1.0), 3)


class SecurityDebtTracker:
    def __init__(self, project_name: str):
        self.project_name = project_name
        self.items: List[SecurityDebtItem] = []

    def add_item(self, item: SecurityDebtItem) -> None:
        self.items.append(item)

    def total_security_debt_score(self) -> float:
        return round(sum(item.risk_score for item in self.items), 2)

    def get_sla_breaches(self) -> List[SecurityDebtItem]:
        return [item for item in self.items if item.is_sla_breached]

    def get_prioritized_backlog(self) -> List[SecurityDebtItem]:
        """Rank by ROI (risk reduction vs remediation effort)."""
        return sorted(self.items, key=lambda x: x.roi_score, reverse=True)

    def generate_summary(self) -> Dict:
        total = len(self.items)
        breached = len(self.get_sla_breaches())
        return {
            "project": self.project_name,
            "total_debt_items": total,
            "sla_breached_count": breached,
            "total_risk_score": self.total_security_debt_score(),
            "critical_count": len([i for i in self.items if i.severity == Severity.CRITICAL]),
            "high_count": len([i for i in self.items if i.severity == Severity.HIGH]),
            "by_category": {
                cat.value: len([i for i in self.items if i.category == cat])
                for cat in DebtCategory
            }
        }
```

---

## 5. Security Debt Remediation & Audit Report Template

```markdown
# Security Technical Debt Assessment Report

## 1. Executive Summary
- **Target System / Portfolio**: [Project Name / Microservice Cluster]
- **Current Security Debt Index (SDI)**: [Aggregate Score]
- **SLA Compliance Rate**: [X% Within SLA | Y SLA Breaches]
- **Estimated Remediation Investment**: [X Developer Hours / $Y]

## 2. Debt Distribution & Health Metrics

```
                     SECURITY DEBT BY CATEGORY
  ┌────────────────────────┬──────────────────────────────────────────┐
  │ Category               │ Count | Critical | SLA Breached (>30d)   │
  ├────────────────────────┼──────────────────────────────────────────┤
  │ 1. Code (CWEs/Secrets) │   12  |    3     |        2                 │
  │ 2. Supply Chain (SCA)  │   45  |    7     |       14                 │
  │ 3. Architecture        │    4  |    2     |        4                 │
  │ 4. Cloud & Infra (IAM) │    8  |    1     |        3                 │
  │ 5. Governance/Process  │    3  |    0     |        1                 │
  └────────────────────────┴──────────────────────────────────────────┘
```

## 3. High-Risk Security Debt Items

| ID | Category | Flaw Description | CVSS | EPSS | Age | Remediation Action | ROI Rank |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **SEC-01** | Code | Hardcoded Database Credentials in config.py | 9.8 | 0.85 | 120d | Migrate to AWS Secrets Manager / Vault | #1 (Quick Win) |
| **SEC-02** | Supply Chain | End-of-Life Node.js 14 runtime in legacy auth-worker | 8.8 | 0.60 | 210d | Upgrade runtime to Node.js 20 LTS | #2 |
| **SEC-03** | Architecture | Lack of tenant validation on document download | 8.5 | 0.40 | 95d | Implement centralized ABAC policy filter | #3 |
| **SEC-04** | Cloud Infra | Wildcard `AdministratorAccess` on worker instance profile | 8.2 | 0.15 | 150d | Scrape least-privilege IAM policy via CloudTrail | #4 |

## 4. Phased Remediation Plan

### Sprint 1-2 (Immediate Paydown / Quick Wins)
- [ ] Remove hardcoded tokens from git history and rotate all active keys.
- [ ] Upgrade high-risk direct dependencies with available patch versions.
- [ ] Enforce automated secret scanning in pre-commit hooks.

### Month 2-3 (Systemic & Code Refactoring)
- [ ] Replace legacy raw SQL queries with parameterized ORM bindings.
- [ ] Restrict IAM policies on service roles using least-privilege scoping.
- [ ] Implement central input validation schema (Pydantic / Zod).

### Quarter 2-4 (Architectural Modernization)
- [ ] Migrate legacy monolithic session storage to distributed OAuth2/OIDC + short-lived JWTs.
- [ ] Implement mTLS and service mesh policies across all internal microservice boundaries.
- [ ] Decommission EOL container runtimes across production clusters.

## 5. Prevention & Shift-Left Guardrails
- **Pre-commit**: GitLeaks / TruffleHog for secrets detection.
- **CI Pipeline**: Semgrep / SonarQube (Fail build on CVSS $\ge 7.0$ for new code).
- **Dependency Audit**: Dependabot / Renovate automated PRs for patch and minor updates.
- **Security Debt Budget**: Max allowable 10% sprint capacity dedicated to security debt backlog until SDI < baseline threshold.
```

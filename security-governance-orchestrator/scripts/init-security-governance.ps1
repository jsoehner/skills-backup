<#
.SYNOPSIS
    Initialize complete Security Governance on Windows (PowerShell)
.DESCRIPTION
    Scaffolds docs/adr/, .github/workflows/, .github/dependabot.yml,
    .github/CODEOWNERS, and installs Git pre-commit hooks for any repository.
.EXAMPLE
    .\init-security-governance.ps1 -TargetDir "C:\projects\my-repo"
#>

[CmdletBinding()]
param(
    [Parameter(Position = 0, Mandatory = $false)]
    [string]$TargetDir = "."
)

$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$skillRoot = Split-Path -Parent $scriptDir
$templatesDir = Join-Path $skillRoot "templates"
$resolvedTarget = (Resolve-Path $TargetDir).Path

Write-Host "🛡️ Initializing Security Governance in: $resolvedTarget" -ForegroundColor Cyan
$todayStr = (Get-Date).ToString("yyyy-MM-dd")

# 1. Create docs/adr/ directory and baseline files
$adrDir = Join-Path $resolvedTarget "docs\adr"
if (-not (Test-Path $adrDir)) {
    New-Item -ItemType Directory -Path $adrDir -Force | Out-Null
}

$adr0000 = Join-Path $adrDir "0000-record-architecture-decisions.md"
if (-not (Test-Path $adr0000)) {
    $adr0000Content = @"
# 0. Record Architecture Decisions

- **Status**: Accepted
- **Date**: $todayStr
- **Security Classification**: Internal
- **Decision Makers**: Architecture Review Board & Security Team

## Context
We need to record architecturally significant decisions, security controls, cryptographic choices, and compliance exception rationale.

## Decision
We will use Architectural Decision Records (ADRs) and Security ADRs stored directly in `docs/adr/`. All significant design choices affecting security, data boundaries, or system architecture must be documented here.

## Consequences
- Architectural rationale and security decisions are preserved in git.
- Pull requests modifying security-sensitive architecture are checked for corresponding ADRs.
- Superseded decisions will be linked bidirectionally.
"@
    Set-Content -Path $adr0000 -Value $adr0000Content -Encoding UTF8
    Write-Host "  ✅ Created docs/adr/0000-record-architecture-decisions.md" -ForegroundColor Green
}

$adrReadme = Join-Path $adrDir "README.md"
if (-not (Test-Path $adrReadme)) {
    $adrReadmeContent = @"
# Architecture & Security Decision Log

This directory contains Architectural Decision Records (ADRs) and Security Architecture Decision Records (SecADRs) for this repository.

## Index of Decisions

| ID | Title | Date | Status | Classification |
| :--- | :--- | :--- | :--- | :--- |
| 0000 | [Record Architecture Decisions](0000-record-architecture-decisions.md) | $todayStr | Accepted | Internal |
"@
    Set-Content -Path $adrReadme -Value $adrReadmeContent -Encoding UTF8
    Write-Host "  ✅ Created docs/adr/README.md index" -ForegroundColor Green
}

# Copy Security ADR Template
$srcSecAdr = Join-Path $templatesDir "Security_ADR_Template.md"
$destSecAdr = Join-Path $adrDir "Security_ADR_Template.md"
if ((Test-Path $srcSecAdr) -and (-not (Test-Path $destSecAdr))) {
    Copy-Item -Path $srcSecAdr -Destination $destSecAdr -Force
    Write-Host "  ✅ Added docs/adr/Security_ADR_Template.md" -ForegroundColor Green
}

# 2. Setup GitHub Actions workflows (.github/workflows/)
$workflowsDir = Join-Path $resolvedTarget ".github\workflows"
if (-not (Test-Path $workflowsDir)) {
    New-Item -ItemType Directory -Path $workflowsDir -Force | Out-Null
}

$srcWf = Join-Path $templatesDir "security-governance.yml"
$destWf = Join-Path $workflowsDir "security-governance.yml"
if ((Test-Path $srcWf) -and (-not (Test-Path $destWf))) {
    Copy-Item -Path $srcWf -Destination $destWf -Force
    Write-Host "  ✅ Deployed .github/workflows/security-governance.yml" -ForegroundColor Green
}

# 3. Setup Dependabot (.github/dependabot.yml)
$githubDir = Join-Path $resolvedTarget ".github"
$srcDep = Join-Path $templatesDir "dependabot.yml"
$destDep = Join-Path $githubDir "dependabot.yml"
if ((Test-Path $srcDep) -and (-not (Test-Path $destDep))) {
    Copy-Item -Path $srcDep -Destination $destDep -Force
    Write-Host "  ✅ Deployed .github/dependabot.yml" -ForegroundColor Green
}

# 4. Setup CODEOWNERS (.github/CODEOWNERS)
$destCodeowners = Join-Path $githubDir "CODEOWNERS"
if (-not (Test-Path $destCodeowners)) {
    $codeownersContent = @"
# Security Governance CODEOWNERS
# Require review from security champions on high-risk paths

# Security and Cryptography
/auth/              @security-team
/crypto/            @security-team
/security/          @security-team
/certs/             @security-team

# CI/CD Workflows & Policies
/.github/workflows/ @platform-team @security-team
/.github/CODEOWNERS @security-team

# Architectural Decisions
/docs/adr/          @architecture-board @security-team
"@
    Set-Content -Path $destCodeowners -Value $codeownersContent -Encoding UTF8
    Write-Host "  ✅ Deployed .github/CODEOWNERS" -ForegroundColor Green
}

# 5. Copy Gatekeeper scripts to repo's scripts/ directory
$repoScriptsDir = Join-Path $resolvedTarget "scripts"
if (-not (Test-Path $repoScriptsDir)) {
    New-Item -ItemType Directory -Path $repoScriptsDir -Force | Out-Null
}

$srcPyGatekeeper = Join-Path $scriptDir "adr_security_gatekeeper.py"
$destPyGatekeeper = Join-Path $repoScriptsDir "adr_security_gatekeeper.py"
if ((Test-Path $srcPyGatekeeper) -and (-not (Test-Path $destPyGatekeeper))) {
    Copy-Item -Path $srcPyGatekeeper -Destination $destPyGatekeeper -Force
    Write-Host "  ✅ Deployed scripts/adr_security_gatekeeper.py" -ForegroundColor Green
}

$srcPsGatekeeper = Join-Path $scriptDir "adr-security-gatekeeper.ps1"
$destPsGatekeeper = Join-Path $repoScriptsDir "adr-security-gatekeeper.ps1"
if ((Test-Path $srcPsGatekeeper) -and (-not (Test-Path $destPsGatekeeper))) {
    Copy-Item -Path $srcPsGatekeeper -Destination $destPsGatekeeper -Force
    Write-Host "  ✅ Deployed scripts/adr-security-gatekeeper.ps1" -ForegroundColor Green
}

# 6. Setup client-side Git pre-commit hooks (if .git exists)
$gitHooksDir = Join-Path $resolvedTarget ".git\hooks"
if (Test-Path $gitHooksDir) {
    # Copy pre_commit.py
    $srcPyHook = Join-Path $templatesDir "pre_commit.py"
    $destPyHook = Join-Path $gitHooksDir "pre_commit.py"
    Copy-Item -Path $srcPyHook -Destination $destPyHook -Force

    # Copy pre-commit.ps1
    $srcPsHook = Join-Path $templatesDir "pre-commit.ps1"
    $destPsHook = Join-Path $gitHooksDir "pre-commit.ps1"
    Copy-Item -Path $srcPsHook -Destination $destPsHook -Force

    # Copy pre-commit.bat
    $srcBatHook = Join-Path $templatesDir "pre-commit.bat"
    $destBatHook = Join-Path $gitHooksDir "pre-commit.bat"
    Copy-Item -Path $srcBatHook -Destination $destBatHook -Force

    # Copy unix pre-commit wrapper for Git Bash / WSL
    $srcShHook = Join-Path $templatesDir "pre-commit.sh"
    $destShHook = Join-Path $gitHooksDir "pre-commit"
    Copy-Item -Path $srcShHook -Destination $destShHook -Force

    Write-Host "  ✅ Configured Git hooks (.git/hooks/pre-commit and pre-commit.bat/ps1)" -ForegroundColor Green
}

Write-Host "`n🎉 Security Governance setup complete!" -ForegroundColor Green
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host " 1. Run local ADR Gatekeeper: powershell -File scripts\adr-security-gatekeeper.ps1" -ForegroundColor Gray
Write-Host " 2. Conduct a STRIDE threat model on core data flows" -ForegroundColor Gray
Write-Host " 3. Record decisions in docs/adr/ using the Security ADR template" -ForegroundColor Gray

<#
.SYNOPSIS
    ADR Security Gatekeeper (PowerShell for Windows)
.DESCRIPTION
    Analyzes Git changes (pull request diff, branch diff, or staged files)
    and enforces that changes to security-critical architecture paths must include
    an Architectural Decision Record (ADR) in docs/adr/.
.EXAMPLE
    .\adr-security-gatekeeper.ps1 -Base "origin/main"
.EXAMPLE
    .\adr-security-gatekeeper.ps1 -Staged
#>

[CmdletBinding()]
param(
    [Parameter(Mandatory = $false)]
    [string]$Base = "",

    [Parameter(Mandatory = $false)]
    [switch]$Staged,

    [Parameter(Mandatory = $false)]
    [string[]]$Paths = @(
        "auth/",
        "crypto/",
        "security/",
        "certs/",
        ".github/workflows/",
        "api/",
        "policy/"
    )
)

$ErrorActionPreference = "Stop"

Write-Host "🛡️ [ADR Security Gatekeeper] Analyzing changes with PowerShell..." -ForegroundColor Cyan

# Determine changed files
if ($Staged) {
    $rawOutput = git diff --cached --name-only --diff-filter=ACM
} elseif ($Base -ne "") {
    $rawOutput = git diff --name-only "$Base...HEAD"
    if (-not $rawOutput) {
        $rawOutput = git diff --name-only $Base HEAD
    }
} else {
    $rawOutput = git diff --name-only "HEAD~1" "HEAD"
}

$changedFiles = @()
if ($rawOutput) {
    $changedFiles = @($rawOutput -split "`r?`n" | Where-Object { $_.Trim() -ne "" } | ForEach-Object { $_.Trim() -replace "\\", "/" })
}

if ($changedFiles.Count -eq 0) {
    Write-Host "ℹ️ No files changed in analyzed scope." -ForegroundColor Gray
    exit 0
}

Write-Host "Total changed files: $($changedFiles.Count)"

# Check for sensitive paths
$sensitiveModified = @()
foreach ($file in $changedFiles) {
    foreach ($prefix in $Paths) {
        if ($file.StartsWith($prefix)) {
            $sensitiveModified += $file
            break
        }
    }
}

if ($sensitiveModified.Count -eq 0) {
    Write-Host "✅ No security-critical architecture paths modified. ADR not required." -ForegroundColor Green
    exit 0
}

Write-Host "`n⚠️ Security-critical files modified in this change set:" -ForegroundColor Yellow
foreach ($file in $sensitiveModified) {
    Write-Host "   - $file" -ForegroundColor Gray
}

# Check for ADR update
$adrFiles = @($changedFiles | Where-Object { $_.StartsWith("docs/adr/") -and $_.EndsWith(".md") -and -not $_.EndsWith("README.md") })

if ($adrFiles.Count -gt 0) {
    Write-Host "`n✅ Architectural Decision Record(s) found in docs/adr/:" -ForegroundColor Green
    foreach ($adr in $adrFiles) {
        Write-Host "   + $adr" -ForegroundColor Green
    }
    Write-Host "`n🎉 ADR Gatekeeper check passed!" -ForegroundColor Green
    exit 0
} else {
    Write-Host "`n======================================================================" -ForegroundColor Red
    Write-Host "❌ ERROR: ADR SECURITY GATEKEEPER CHECK FAILED" -ForegroundColor Red
    Write-Host "======================================================================" -ForegroundColor Red
    Write-Host "Changes touch security-sensitive paths, but no Architectural Decision Record" -ForegroundColor Red
    Write-Host "was added or updated in 'docs/adr/'." -ForegroundColor Red
    Write-Host "`nRemediation:" -ForegroundColor Yellow
    Write-Host "  1. Review 'docs/adr/Security_ADR_Template.md'" -ForegroundColor Gray
    Write-Host "  2. Create a new ADR (e.g. 'docs/adr/000X-security-decision-name.md')" -ForegroundColor Gray
    Write-Host "  3. Update 'docs/adr/README.md' index table" -ForegroundColor Gray
    Write-Host "  4. Commit the ADR alongside your changes." -ForegroundColor Gray
    Write-Host "======================================================================`n" -ForegroundColor Red
    exit 1
}

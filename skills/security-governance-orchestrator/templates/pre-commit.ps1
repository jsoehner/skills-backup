<#
.SYNOPSIS
    Pre-Commit Security & ADR Gatekeeper (PowerShell for Windows)
.DESCRIPTION
    Checks staged git files on Windows for:
    1. Plaintext credentials, private keys, and API tokens.
    2. Security-sensitive architectural changes requiring an accompanying ADR.
#>

[CmdletBinding()]
param()

$ErrorActionPreference = "Stop"

Write-Host "🔒 [Security Governance] Running PowerShell pre-commit checks..." -ForegroundColor Cyan

# 1. Get staged files
$stagedFilesRaw = git diff --cached --name-only --diff-filter=ACM
if (-not $stagedFilesRaw) {
    exit 0
}

$stagedFiles = @($stagedFilesRaw -split "`r?`n" | Where-Object { $_.Trim() -ne "" } | ForEach-Object { $_.Trim() -replace "\\", "/" })
if ($stagedFiles.Count -eq 0) {
    exit 0
}

# 2. Secret regex patterns
$secretPatterns = @(
    @{ Pattern = "AKIA[0-9A-Z]{16}"; Description = "AWS Access Key ID" },
    @{ Pattern = "ghp_[0-9a-zA-Z]{36}"; Description = "GitHub Personal Access Token" },
    @{ Pattern = "gho_[0-9a-zA-Z]{36}"; Description = "GitHub OAuth Token" },
    @{ Pattern = "-----BEGIN (?:RSA|EC|DSA|OPENSSH) PRIVATE KEY-----"; Description = "Private Encryption Key" },
    @{ Pattern = "eyJhbGciOi[0-9a-zA-Z_-]{10,}\.[0-9a-zA-Z_-]{10,}\.[0-9a-zA-Z_-]{10,}"; Description = "JSON Web Token (JWT)" },
    @{ Pattern = "sk_live_[0-9a-zA-Z]{24}"; Description = "Stripe Live API Key" },
    @{ Pattern = "xox[baprs]-[0-9]{10,13}-[0-9]{10,13}-[a-zA-Z0-9]{24,32}"; Description = "Slack Token" }
)

$foundSecrets = @()
foreach ($file in $stagedFiles) {
    $diffText = git diff --cached $file
    foreach ($item in $secretPatterns) {
        if ($diffText -match $item.Pattern) {
            $foundSecrets += [PSCustomObject]@{
                File = $file
                Description = $item.Description
            }
        }
    }
}

if ($foundSecrets.Count -gt 0) {
    Write-Host "`n❌ SECURITY GATE FAILURE: Plaintext credentials detected in staged commit!" -ForegroundColor Red
    foreach ($item in $foundSecrets) {
        Write-Host "   - $($item.File): Detected $($item.Description)" -ForegroundColor Yellow
    }
    Write-Host "`nPlease remove the credentials, revoke if exposed, and use environment variables or secret vaults.`n" -ForegroundColor Red
    exit 1
}

# 3. Check for security-sensitive architecture modifications
$sensitivePaths = @(
    "auth/",
    "crypto/",
    "security/",
    "certs/",
    ".github/workflows/",
    "api/",
    "policy/"
)

$touchesSensitive = @()
foreach ($file in $stagedFiles) {
    foreach ($prefix in $sensitivePaths) {
        if ($file.StartsWith($prefix)) {
            $touchesSensitive += $file
            break
        }
    }
}

if ($touchesSensitive.Count -gt 0) {
    $hasAdr = $false
    foreach ($file in $stagedFiles) {
        if ($file.StartsWith("docs/adr/") -and $file.EndsWith(".md")) {
            $hasAdr = $true
            break
        }
    }

    if (-not $hasAdr) {
        Write-Host "`n⚠️  ARCHITECTURAL NOTICE: Staged changes touch security-critical boundaries:" -ForegroundColor Yellow
        $previewCount = [Math]::Min($touchesSensitive.Count, 5)
        for ($i = 0; $i -lt $previewCount; $i++) {
            Write-Host "   - $($touchesSensitive[$i])" -ForegroundColor Gray
        }
        if ($touchesSensitive.Count -gt 5) {
            Write-Host "   - ... and $($touchesSensitive.Count - 5) other files" -ForegroundColor Gray
        }
        Write-Host "   No accompanying ADR found in 'docs/adr/'." -ForegroundColor Yellow
        Write-Host "   Ensure this architectural change is documented in docs/adr/ before opening a PR." -ForegroundColor Yellow
        Write-Host "   (CI will enforce ADR presence on protected branches).`n" -ForegroundColor Gray
    }
}

Write-Host "✅ [Security Governance] Pre-commit checks passed." -ForegroundColor Green
exit 0

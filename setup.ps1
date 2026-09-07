<#
.SYNOPSIS
    Setup and skills management script for Skills Backup repository (Windows PowerShell).

.DESCRIPTION
    Restores agent skills, displays skills catalog, or inspects installation status (new vs existing skills)
    for target AI client runtimes (pi, gemini, claude, opencode).

.PARAMETER Client
    Target AI runtime client. Options: pi, gemini, claude, opencode. Default: pi.

.PARAMETER Catalog
    Switch to display the skill catalog grouped by category.

.PARAMETER Status
    Switch to show installation status (existing vs new skills) for the target client.

.PARAMETER New
    Switch to show only new/uninstalled skills for the target client.

.PARAMETER Installed
    Switch to show only existing/installed skills for the target client.

.PARAMETER Categories
    Switch to list all available skill categories and counts.

.PARAMETER Memory
    Switch to show information and host status for the local memory system (OKF + ChromaDB).

.PARAMETER Info
    Switch to display repository overview, skills summary, and local memory architecture info.

.PARAMETER Category
    Filter catalog or status by category name.

.PARAMETER Search
    Search skills by keyword in name or description.

.PARAMETER Restore
    Explicitly run restore action (default action if no display flags are provided).

.PARAMETER PythonPath
    Optional path to a specific Python 3 executable.

.EXAMPLE
    .\setup.ps1 -Client gemini

.EXAMPLE
    .\setup.ps1 -Status -Client gemini

.EXAMPLE
    .\setup.ps1 -Memory

.EXAMPLE
    .\setup.ps1 -Info

.EXAMPLE
    .\setup.ps1 -Catalog -Category databases_data

.EXAMPLE
    .\setup.ps1 -Catalog -Search postgres
#>

[CmdletBinding()]
param (
    [ValidateSet("pi", "gemini", "claude", "opencode", IgnoreCase = $true)]
    [string]$Client = "pi",

    [switch]$Catalog,
    [switch]$Status,
    [switch]$New,
    [switch]$Installed,
    [switch]$Categories,
    [switch]$Memory,
    [switch]$Info,

    [string]$Category = "",
    [string]$Search = "",
    [switch]$Restore,

    [string]$PythonPath = ""
)

$ErrorActionPreference = "Stop"

# Determine script directory
$RepoRoot = if ($PSScriptRoot) { $PSScriptRoot } else { Split-Path -Parent $MyInvocation.MyCommand.Path }
$RestoreScript = Join-Path -Path $RepoRoot -ChildPath "scripts\restore_skills.py"
$CatalogScript = Join-Path -Path $RepoRoot -ChildPath "scripts\catalog.py"

# Locate Python 3
$PythonExecutable = $null

if ($PythonPath -and (Test-Path -Path $PythonPath)) {
    $PythonExecutable = $PythonPath
} else {
    $Candidates = @("python", "python3", "py")
    foreach ($Cmd in $Candidates) {
        $CommandInfo = Get-Command $Cmd -ErrorAction SilentlyContinue
        if ($CommandInfo) {
            # Test Python version
            try {
                $VersionCheck = & $Cmd -c "import sys; sys.exit(0 if sys.version_info >= (3, 7) else 1)" 2>$null
                if ($LASTEXITCODE -eq 0) {
                    $PythonExecutable = $Cmd
                    break
                }
            } catch {
                # Continue searching
            }
        }
    }
}

if (-not $PythonExecutable) {
    Write-Error "Error: Python 3 (version 3.7+) was not found in PATH. Please install Python 3 or specify -PythonPath."
    exit 1
}

# Determine action
$IsDisplayAction = $Catalog -or $Status -or $New -or $Installed -or $Categories -or $Memory -or $Info -or ($Category -and -not $Restore) -or ($Search -and -not $Restore)

if ($IsDisplayAction) {
    if (-not (Test-Path -Path $CatalogScript)) {
        Write-Error "Error: Catalog script not found at '$CatalogScript'."
        exit 1
    }

    $CatArgs = @($CatalogScript, "--client", $Client)

    if ($Catalog)    { $CatArgs += "--catalog" }
    if ($Status)     { $CatArgs += "--status" }
    if ($New)        { $CatArgs += "--new" }
    if ($Installed)  { $CatArgs += "--installed" }
    if ($Categories) { $CatArgs += "--categories" }
    if ($Memory -or $Info) { $CatArgs += "--memory" }

    if ($Category) {
        $CatArgs += "--category"
        $CatArgs += $Category
    }
    if ($Search) {
        $CatArgs += "--search"
        $CatArgs += $Search
    }

    & $PythonExecutable $CatArgs
    exit $LASTEXITCODE
} else {
    if (-not (Test-Path -Path $RestoreScript)) {
        Write-Error "Error: Restore script not found at '$RestoreScript'."
        exit 1
    }

    $PythonVersion = & $PythonExecutable --version 2>&1

    Write-Host "==================================================" -ForegroundColor Cyan
    Write-Host "Skills Backup Setup" -ForegroundColor Cyan
    Write-Host "==================================================" -ForegroundColor Cyan
    Write-Host "Repository Root : $RepoRoot"
    Write-Host "Target Client   : $Client"
    Write-Host "Python Runtime  : $PythonVersion"
    Write-Host "==================================================" -ForegroundColor Cyan
    Write-Host ""

    try {
        & $PythonExecutable $RestoreScript $RepoRoot --client $Client
        if ($LASTEXITCODE -ne 0) {
            Write-Error "Setup failed with exit code $LASTEXITCODE."
            exit $LASTEXITCODE
        }
        Write-Host ""
        Write-Host "==================================================" -ForegroundColor Green
        Write-Host "Setup Complete!" -ForegroundColor Green
        Write-Host "==================================================" -ForegroundColor Green
        Write-Host "All skills successfully restored to target client [$Client]."
        Write-Host ""
        Write-Host "🧠 Local Memory & Context Systems:" -ForegroundColor Cyan
        Write-Host "  • Key Skills Restored : memory-capture, context-manager, session-handoff"
        Write-Host "  • Inspect Memory Host : .\setup.ps1 -Memory"
        Write-Host "  • Storage Location    : ~/memory_system (OKF policies & ChromaDB vectors)"
        Write-Host "  • Ingestion Script    : python ~/memory_system/capture_knowledge.py <file.md>"
        Write-Host ""
        Write-Host "💡 Helpful Next Commands:" -ForegroundColor Yellow
        Write-Host "  • Check Installed vs New : .\setup.ps1 -Status -Client $Client"
        Write-Host "  • Browse Skills Catalog  : .\setup.ps1 -Catalog"
        Write-Host "  • Search Skills          : .\setup.ps1 -Catalog -Search <keyword>"
        Write-Host "==================================================" -ForegroundColor Green
    } catch {
        Write-Error "An error occurred during setup: $_"
        exit 1
    }
}

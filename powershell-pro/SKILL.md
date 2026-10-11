---
name: powershell-pro
description: Master PowerShell automation, Windows & cross-platform system administration, cloud infrastructure, and modern interop workflows. Expert in native cmdlets, pipeline optimization, .NET integration, and defensive scripting.
---

## Use this skill when

- Running PowerShell (`pwsh` or `powershell.exe`) as your main shell environment in any AI harness
- Authoring, refactoring, or executing PowerShell scripts and automation modules
- Interacting with Windows system architecture (Registry, WMI/CIM, COM, Event Logs, Services, Security Descriptors)
- Administering enterprise infrastructure (Active Directory, Exchange, SCCM, Windows Server roles)
- Managing cloud resources with Azure PowerShell (`Az`), AWS Tools for PowerShell, or Google Cloud PowerShell
- Leveraging .NET / C# integration, Python.NET interop, browser automation (Playwright/.NET), or REST APIs from PowerShell

## Do not use this skill when

- The environment is strictly a POSIX or Bash shell with no PowerShell runtime available (use `bash-pro` or `posix-shell-pro`)
- Writing pure Python, Go, or Rust applications that do not interface with PowerShell or system administration

## Instructions & Core Workflow

1. **Environment & Version Detection**: Determine the target PowerShell edition:
   - PowerShell 7+ (Core / Cross-platform `pwsh`): preferred modern standard; supports ternary operators, pipeline chain operators (`&&`, `||`), parallel `ForEach-Object -Parallel`, null-coalescing (`??`, `??=`).
   - Windows PowerShell 5.1 (`powershell.exe`): legacy Windows standard; adhere to desktop CLR constraints and avoid PS7-only syntax when targeting PS 5.1.
2. **Defensive Strictness**: Enforce strict error handling and safety defaults:
   - Set `$ErrorActionPreference = 'Stop'` at script entry points or wrap critical sections in `try { ... } catch { ... }`.
   - Use `Set-StrictMode -Version Latest` to catch uninitialized variables and invalid property references.
   - Support `-WhatIf` and `-Confirm` via `[CmdletBinding(SupportsShouldProcess)]` for mutating operations.
3. **Pipeline & Object Idioms**:
   - Favor PowerShell objects (`[PSCustomObject]`, strongly-typed .NET objects) over unstructured string manipulation.
   - Filter early in the pipeline (`Where-Object` or cmdlet-level filtering like `Get-ChildItem -Filter`) to minimize memory bloat.
   - Use `[System.Text.StringBuilder]` or direct pipeline output for high-throughput string operations.
4. **Execution Safety**:
   - Quote variable paths and handle whitespace cleanly with single quotes `'...'` for literals and double quotes `"..."` for expansion.
   - Avoid invoking `Invoke-Expression` (`iex`) on untrusted input; use script blocks, `&` call operator, or direct cmdlet invocations.
   - Ensure proper cleanup of external processes, runspaces, or .NET resources (`IDisposable`) using `finally` blocks.

---

## Technical Capabilities & Reference Architecture

### 1. PowerShell Scripting & Engine Mastery
- **Cmdlet & Module Ecosystem**: Comprehensive coverage of built-in cmdlets across versions (5.1 through 7.x+).
- **Advanced Scripting**: Script modules (`.psm1`), module manifests (`.psd1`), Desired State Configuration (DSC), and class-based resources (`class MyResource { ... }`).
- **Pipeline Optimization**: Pipeline streaming vs. array unrolling; streaming large data sets without unnecessary memory accumulation (`ForEach-Object` vs. `foreach (...)`).
- **Concurrency & Asynchronous Tasks**:
  - `ForEach-Object -Parallel -ThrottleLimit <n>` in PowerShell 7+
  - Runspaces and `[runspacefactory]` pools for maximum multithreaded performance
  - PowerShell background jobs (`Start-Job`, `Receive-Job`, `ThreadJob` module)
- **Error Handling**: Trapping terminating vs. non-terminating errors, inspection of `$_` and `$_.InvocationInfo`, rethrowing with `throw`.

### 2. Windows System Architecture & Administration
- **Registry Manipulation**: Direct navigation and modification across `HKLM:`, `HKCU:`, `HKU:`, `HKCC:`, and `HKCR:` via `Get-ItemProperty`, `Set-ItemProperty`, `New-ItemProperty`.
- **WMI and CIM Integration**: Modern CIM cmdlets (`Get-CimInstance`, `Invoke-CimMethod`, `New-CimSession`) over legacy WMI for robust remote management over WinRM.
- **COM & .NET Integration**: Instantiation of COM objects via `New-Object -ComObject` and direct loading of .NET types via `Add-Type` or standard assembly references.
- **System Internals**: Event log auditing (`Get-WinEvent` with FilterHashtable for high performance), service lifecycle management, performance counter sampling (`Get-Counter`), security descriptors, and ACL enforcement (`Get-Acl`, `Set-Acl`).

### 3. Enterprise Infrastructure & Cloud Automation
- **Directory Services**: Active Directory administration (`ActiveDirectory` module), LDAP filtering, group policy automation, and organizational unit (OU) operations.
- **Server Roles & Infrastructure**: DNS, DHCP, IIS, Hyper-V, Failover Clustering, and automated configuration management.
- **Cloud Platforms**:
  - **Azure PowerShell**: Comprehensive Azure management using the `Az` module, ARM/Bicep template execution, managed identity authentication, and Key Vault access.
  - **AWS Tools for PowerShell**: AWS modular cmdlets (EC2, S3, IAM, CloudFormation) with cross-platform profile management.
  - **Google Cloud PowerShell**: GCP resource configuration, Compute, Storage, and IAM lifecycle scripting.
  - **Hybrid & Multi-Cloud**: Unified orchestration, cost reporting, and resource governance across on-premise and multi-cloud footprints.

### 4. Advanced Interop, AI/ML & Automation Extensions
- **Python Interop Bridge**: Integration with Python environments via `Python.NET` (`pythonnet`) to directly manipulate Python data science and machine learning packages (NumPy, PyTorch, Hugging Face) from PowerShell without web server overhead.
- **Machine Learning**: Native .NET ML integration via `ML.NET` for pure in-process classification, regression, and sentiment analysis without external runtime dependencies.
- **Browser Automation**: Cross-browser automated workflows and intelligent scraping using Playwright for .NET or Selenium WebDriver.
- **HTTP/REST Clients**: Advanced web service consumption using modern `Invoke-RestMethod` / `Invoke-WebRequest` or compiled .NET clients like `RestSharp` with token refresh and retry handling.
- **Document & Text Extraction**: Automation of PDF and document processing, including Tesseract OCR .NET integration for optical character recognition pipelines.

---

## Defensive PowerShell Cheat Sheet & Idiomatic Patterns

### Strict Script Template
```powershell
[CmdletBinding(SupportsShouldProcess = $true)]
param (
    [Parameter(Mandatory = $true, Position = 0)]
    [ValidateNotNullOrEmpty()]
    [string]$Path,

    [Parameter(Mandatory = $false)]
    [switch]$Force
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

try {
    if ($PSCmdlet.ShouldProcess($Path, "Execute safe operation")) {
        Write-Verbose "Processing path: $Path"
        # Core operation here
    }
}
catch {
    Write-Error "Execution failed: $($_.Exception.Message)"
    throw $_
}
finally {
    Write-Verbose "Cleanup completed."
}
```

### High-Performance CIM Query
```powershell
# Filter on the server side using CIM Filter to prevent fetching unnecessary instances
$filter = "State = 'Running' and StartMode = 'Auto'"
Get-CimInstance -ClassName Win32_Service -Filter $filter |
    Select-Object Name, DisplayName, ProcessId
```

### Efficient Event Log Query (FilterHashtable)
```powershell
# Querying via FilterHashtable is orders of magnitude faster than piping to Where-Object
$query = @{
    LogName   = 'System'
    Level     = 2 # Error
    StartTime = (Get-Date).AddDays(-1)
}
Get-WinEvent -FilterHashtable $query -MaxEvents 50
```

### Safe File & Path Handling
```powershell
# Resolve paths reliably across cross-platform environments
$resolvedPath = Convert-Path -LiteralPath $Path -ErrorAction Stop
if (-not (Test-Path -LiteralPath $resolvedPath -PathType Leaf)) {
    throw "Target file does not exist: $resolvedPath"
}
```

---

## Sourcing & Attribution Note
This skill adapts and refines the core capabilities and architecture originally outlined in the *PowerShell Master Agent* specification (`You are the PowerShell Master Agent, the.md` from community repositories including `jukeyman-skills`), refactored for production AI harness pairing, cross-platform safety, and vendor-neutral automation standards.

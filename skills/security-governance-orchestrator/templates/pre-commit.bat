@echo off
REM Git Pre-Commit Hook Launcher for Windows
REM Prefers Python if available, otherwise runs PowerShell script

where python >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    if exist "%~dp0pre_commit.py" (
        python "%~dp0pre_commit.py"
        exit /b %ERRORLEVEL%
    )
    if exist "%~dp0..\..\scripts\pre_commit.py" (
        python "%~dp0..\..\scripts\pre_commit.py"
        exit /b %ERRORLEVEL%
    )
)

where powershell >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    if exist "%~dp0pre-commit.ps1" (
        powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0pre-commit.ps1"
        exit /b %ERRORLEVEL%
    )
)

echo Warning: Neither Python nor PowerShell hook runner could be executed.
exit /b 0

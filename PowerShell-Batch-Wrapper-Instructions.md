# PowerShell Script Batch File Wrapper Instructions

## Overview
This guide provides templates and instructions for creating batch file wrappers that make PowerShell scripts double-clickable and user-friendly, eliminating common issues like execution policy restrictions and auto-closing windows.

## Problem Statement
PowerShell scripts when double-clicked typically:
- Fail due to execution policy restrictions
- Close immediately after execution
- Don't request Administrator privileges automatically
- Provide poor user experience for non-technical users

## Solution: Batch File Wrapper Template

### Basic Template
```batch
@echo off
title [SCRIPT_NAME] - Administrator Required
color 0E
echo.
echo ================================================================
echo                    [SCRIPT_TITLE]
echo ================================================================
echo.
echo [SCRIPT_DESCRIPTION]
echo.
echo Administrator privileges are required to:
echo  - [REASON_1]
echo  - [REASON_2]
echo  - [REASON_3]
echo.
echo ================================================================
echo.

REM Check if already running as administrator
net session >nul 2>&1
if %errorLevel% == 0 (
    echo Already running as Administrator - proceeding...
    goto :RunScript
) else (
    echo Requesting Administrator privileges...
    echo.
    echo NOTE: You may see a UAC prompt - please click 'Yes' to continue
    echo.
    pause
    goto :ElevateScript
)

:ElevateScript
REM Create temporary VBS script for elevation
echo Set UAC = CreateObject^("Shell.Application"^) > "%temp%\getadmin.vbs"
echo UAC.ShellExecute "cmd.exe", "/c ""%~s0""", "", "runas", 1 >> "%temp%\getadmin.vbs"
"%temp%\getadmin.vbs"
del "%temp%\getadmin.vbs"
exit /B

:RunScript
REM Change to script directory
cd /d "%~dp0"

REM Check if PowerShell script exists
if not exist "[PS_SCRIPT_NAME].ps1" (
    echo.
    echo ERROR: [PS_SCRIPT_NAME].ps1 not found in current directory!
    echo.
    echo Please ensure both files are in the same folder:
    echo  - [BATCH_FILE_NAME].bat
    echo  - [PS_SCRIPT_NAME].ps1
    echo.
    echo Current directory: %~dp0
    echo.
    pause
    exit /b 1
)

echo.
echo ================================================================
echo                Starting [SCRIPT_NAME]
echo ================================================================
echo.

REM Run PowerShell script with proper execution policy
powershell.exe -WindowStyle Normal -ExecutionPolicy Bypass -Command "& '%~dp0[PS_SCRIPT_NAME].ps1'"

REM Check PowerShell exit code
if %errorlevel% equ 0 (
    echo.
    echo ================================================================
    echo                    Script Completed Successfully
    echo ================================================================
) else (
    echo.
    echo ================================================================
    echo                    Script Completed with Errors
    echo ================================================================
    echo.
    echo Error Code: %errorlevel%
    echo.
    echo Common issues:
    echo  - Script requires Administrator privileges
    echo  - PowerShell execution policy restrictions
    echo  - Antivirus blocking script execution
    echo.
)

echo.
echo ================================================================
echo                       [SCRIPT_NAME] Complete
echo ================================================================
echo.
echo [POST_EXECUTION_INSTRUCTIONS]
echo.
echo Press any key to close this window...
pause >nul
```

## Required PowerShell Script Modifications

### Add to Beginning of PS1 Script
```powershell
# Set window title and console properties for better UX
$host.ui.RawUI.WindowTitle = "[SCRIPT_TITLE]"
if ($host.UI.RawUI.WindowSize.Width -lt 120) {
    try {
        $size = $host.UI.RawUI.WindowSize
        $size.Width = 120
        $host.UI.RawUI.WindowSize = $size
    } catch {
        # Ignore if can't resize
    }
}

# Function to pause and wait for user input
function Wait-ForUser {
    param($Message = "Press any key to continue...")
    Write-Host ""
    Write-Host $Message -ForegroundColor Yellow
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
}

# Enhanced error handling for execution policy
function Test-ExecutionPolicy {
    $currentPolicy = Get-ExecutionPolicy
    if ($currentPolicy -eq "Restricted") {
        Write-Host "WARNING: PowerShell execution policy is set to Restricted" -ForegroundColor Red
        Write-Host "This script may not run properly. Consider running with -ExecutionPolicy Bypass" -ForegroundColor Yellow
        Wait-ForUser "Press any key to continue anyway..."
    }
}

# Enhanced Administrator check
if (-NOT ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Host "ERROR: This script requires Administrator privileges" -ForegroundColor Red
    Write-Host "Please run PowerShell as Administrator and try again" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "To run with elevated privileges:" -ForegroundColor Cyan
    Write-Host "1. Right-click on PowerShell and select 'Run as Administrator'" -ForegroundColor Cyan
    Write-Host "2. Or use the provided [BATCH_FILE_NAME].bat file" -ForegroundColor Cyan
    Wait-ForUser "Press any key to exit..."
    exit 1
}

# Test execution policy
Test-ExecutionPolicy
```

### Add to End of PS1 Script
```powershell
# Final pause before exit to keep window open
Write-Host ""
Write-Host "======================================================================" -ForegroundColor Green
Write-Host "                           SCRIPT COMPLETED                          " -ForegroundColor Green
Write-Host "======================================================================" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. [POST_COMPLETION_STEP_1]" -ForegroundColor Cyan
Write-Host "2. [POST_COMPLETION_STEP_2]" -ForegroundColor Cyan
Write-Host "3. [POST_COMPLETION_STEP_3]" -ForegroundColor Cyan
Write-Host ""

# Keep window open for user to read results
Wait-ForUser "Press any key to close this window..."
```

## Alternative: VBScript Wrapper Template

### Basic VBS Template
```vbscript
' [SCRIPT_NAME] VBScript Launcher
' Provides silent elevation and execution of PowerShell script

Option Explicit

Dim objShell, objFSO, scriptPath, psScriptPath, psCommand, result

' Initialize objects
Set objShell = CreateObject("Shell.Application")
Set objFSO = CreateObject("Scripting.FileSystemObject")

' Get the directory where this VBS script is located
scriptPath = objFSO.GetParentFolderName(WScript.ScriptFullName)
psScriptPath = scriptPath & "\[PS_SCRIPT_NAME].ps1"

' Check if PowerShell script exists
If Not objFSO.FileExists(psScriptPath) Then
    MsgBox "Error: [PS_SCRIPT_NAME].ps1 not found!" & vbCrLf & vbCrLf & _
           "Please ensure both files are in the same folder:" & vbCrLf & _
           "- [VBS_FILE_NAME].vbs" & vbCrLf & _
           "- [PS_SCRIPT_NAME].ps1" & vbCrLf & vbCrLf & _
           "Current directory: " & scriptPath, _
           vbCritical + vbOKOnly, "[SCRIPT_NAME] - File Not Found"
    WScript.Quit 1
End If

' Show information dialog
result = MsgBox("[SCRIPT_TITLE]" & vbCrLf & vbCrLf & _
                "This tool will:" & vbCrLf & _
                "• [FEATURE_1]" & vbCrLf & _
                "• [FEATURE_2]" & vbCrLf & _
                "• [FEATURE_3]" & vbCrLf & vbCrLf & _
                "Administrator privileges are required." & vbCrLf & _
                "You may see a UAC prompt - please click 'Yes' to continue." & vbCrLf & vbCrLf & _
                "Do you want to proceed?", _
                vbQuestion + vbYesNo + vbDefaultButton1, _
                "[SCRIPT_NAME] - Confirmation")

If result = vbNo Then
    WScript.Quit 0
End If

' PowerShell arguments
Dim psArgs
psArgs = "-WindowStyle Normal " & _
         "-ExecutionPolicy Bypass " & _
         "-NoExit " & _
         "-Command """ & _
         "& '" & psScriptPath & "'; " & _
         "Write-Host ''; " & _
         "Write-Host 'Script execution completed.' -ForegroundColor Green; " & _
         "Write-Host 'Press any key to close this window...' -ForegroundColor Yellow; " & _
         "$null = $Host.UI.RawUI.ReadKey('NoEcho,IncludeKeyDown')" & _
         """"

' Execute with elevation
On Error Resume Next
objShell.ShellExecute "powershell.exe", psArgs, scriptPath, "runas", 1

If Err.Number <> 0 Then
    MsgBox "Failed to launch PowerShell script with elevation." & vbCrLf & vbCrLf & _
           "Error: " & Err.Description, _
           vbCritical + vbOKOnly, "[SCRIPT_NAME] - Launch Error"
    WScript.Quit 1
End If

WScript.Quit 0
```

## Placeholder Replacement Guide

When creating a new wrapper, replace these placeholders:

### Batch File Placeholders
- `[SCRIPT_NAME]` - Short name (e.g., "System Cleaner")
- `[SCRIPT_TITLE]` - Full descriptive title
- `[SCRIPT_DESCRIPTION]` - What the script does
- `[REASON_1/2/3]` - Why admin privileges are needed
- `[PS_SCRIPT_NAME]` - PowerShell filename without .ps1 extension
- `[BATCH_FILE_NAME]` - Batch filename without .bat extension
- `[POST_EXECUTION_INSTRUCTIONS]` - What to do after completion

### PowerShell Script Placeholders
- `[SCRIPT_TITLE]` - Window title
- `[BATCH_FILE_NAME]` - Batch wrapper filename
- `[POST_COMPLETION_STEP_1/2/3]` - Next steps for user

### VBScript Placeholders
- `[SCRIPT_NAME]` - Short name for dialogs
- `[SCRIPT_TITLE]` - Full title for confirmation dialog
- `[FEATURE_1/2/3]` - What the script will do
- `[PS_SCRIPT_NAME]` - PowerShell filename without .ps1
- `[VBS_FILE_NAME]` - VBS filename without .vbs extension

## Best Practices

### File Naming Convention
- PowerShell Script: `[Function]-[Purpose].ps1`
- Batch Wrapper: `Run-[Function]-[Purpose].bat`
- VBS Wrapper: `Run-[Function]-[Purpose]-Silent.vbs`

### Example
- PowerShell: `System-Cleanup-Tool.ps1`
- Batch: `Run-System-Cleanup-Tool.bat`
- VBS: `Run-System-Cleanup-Tool-Silent.vbs`

### User Experience Guidelines
1. **Clear Communication**: Always explain what the script will do
2. **Administrator Warning**: Explain why elevation is needed
3. **Error Handling**: Provide helpful error messages
4. **Completion Feedback**: Show clear completion status
5. **Next Steps**: Tell users what to do after completion
6. **Window Management**: Keep window open to read results

### Security Considerations
1. **Execution Policy**: Use `-ExecutionPolicy Bypass` only when necessary
2. **Path Validation**: Always verify script files exist
3. **Error Codes**: Check and handle PowerShell exit codes
4. **Temporary Files**: Clean up any temporary elevation scripts

## Testing Checklist

Before deploying a wrapper:
- [ ] Test double-click execution
- [ ] Verify UAC prompt appears and works
- [ ] Confirm script runs with proper privileges
- [ ] Check error handling for missing files
- [ ] Verify window stays open after completion
- [ ] Test on different Windows versions if possible
- [ ] Ensure proper cleanup of temporary files

## Common Issues and Solutions

### Issue: "Execution Policy Restricted"
**Solution**: Use `-ExecutionPolicy Bypass` parameter

### Issue: Script window closes immediately
**Solution**: Add pause commands and Wait-ForUser functions

### Issue: UAC prompt doesn't appear
**Solution**: Use the VBS elevation method or check UAC settings

### Issue: Script can't find files
**Solution**: Use `%~dp0` to reference script directory

### Issue: PowerShell doesn't start elevated
**Solution**: Verify "runas" verb is used correctly

## Example Implementation

See the WinRing0 detector implementation in this repository for a complete working example:
- `WinRing0-Detector-Remover.ps1` (main script)
- `Run-WinRing0-Detector.bat` (batch wrapper)
- `Run-WinRing0-Detector-Silent.vbs` (VBS wrapper)

## Conclusion

Using these templates ensures consistent, user-friendly PowerShell script execution across different environments while maintaining security best practices and providing excellent user experience.
# Windows Server 2025 Evaluation Edition Product Key Extraction Guide

## Overview
This guide covers methods to extract product keys from Windows Server 2025 Datacenter Evaluation edition and convert it to a full version.

## Current System Status (Example)
```
Software licensing service version: 10.0.26100.4652
Name: Windows(R), ServerDatacenterEval edition
Description: Windows(R) Operating System, TIMEBASED_EVAL channel
Activation ID: 96794a98-097f-42fe-8f28-2c38ea115229
Application ID: 55c92734-d682-4d71-983e-d6ec3f16059f
Extended PID: 03612-04921-000-000001-00-1033-26100.0000-2062025
Product Key Channel: Retail:TB:Eval
Installation ID: 033255090385053904665824186342756737844895181384546394354129604
Partial Product Key: J2T92
License Status: Licensed
Timebased activation expiration: 243800 minute(s) (170 day(s))
Remaining Windows rearm count: 1
Remaining SKU rearm count: 1
```

## Product Key Extraction Methods

### 1. PowerShell Registry Method - BackupProductKeyDefault
```powershell
(Get-ItemProperty -Path "HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion\SoftwareProtectionPlatform" -Name BackupProductKeyDefault -ErrorAction SilentlyContinue).BackupProductKeyDefault
```

### 2. WMI Query for OEM/Firmware Keys
```powershell
(Get-WmiObject -query 'select * from SoftwareLicensingService').OA3xOriginalProductKey
```

### 3. Alternative Registry Value Extraction
```powershell
Get-ItemPropertyValue 'HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion\SoftwareProtectionPlatform' -Name BackupProductKeyDefault -ErrorAction SilentlyContinue
```

### 4. Command Prompt Method (OEM Only)
```cmd
wmic path softwarelicensingservice get OA3xOriginalProductKey
```

## Registry Locations for Product Keys

### Primary Registry Paths:
1. **Main location:**
   ```
   HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion
   ```

2. **Software Protection Platform:**
   ```
   HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\SoftwareProtectionPlatform
   ```

3. **SPP Store (if exists):**
   ```
   HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\SPP\Store\2.0\cache
   ```

4. **BackupProductKeyDefault location:**
   ```
   HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\SoftwareProtectionPlatform\BackupProductKeyDefault
   ```

## Converting Evaluation to Full Version

### Primary DISM Command
```cmd
DISM /online /Set-Edition:ServerDatacenter /ProductKey:XXXXX-XXXXX-XXXXX-XXXXX-XXXXX /AcceptEula
```
*Replace XXXXX-XXXXX-XXXXX-XXXXX-XXXXX with your purchased product key*

### Pre-Conversion Steps (Alternative Method)
1. **Remove existing evaluation key:**
   ```cmd
   slmgr.vbs /cpky
   ```

2. **Uninstall the key:**
   ```cmd
   slmgr.vbs /upk
   ```

3. **Convert using DISM with public KMS key:**
   ```cmd
   DISM /Online /Set-Edition:ServerStandard /ProductKey:N69G4-B89J2-4G8F4-WWYCC-J464C /AcceptEula
   ```

4. **Install purchased key:**
   ```cmd
   slmgr /ipk YOUR-PURCHASED-PRODUCT-KEY
   ```

5. **Activate:**
   ```cmd
   slmgr /ato
   ```

## Public KMS Keys for Server Editions

### Windows Server 2019:
- **Standard:** N69G4-B89J2-4G8F4-WWYCC-J464C
- **Datacenter:** WMDGN-G9PQG-XVVXX-R3X43-63DFG

### Windows Server 2022:
- **Standard:** VDYBN-27WPP-V4HQT-9VMD4-VMK7H
- **Datacenter:** WX4NM-KYWYW-QJJR4-XV3QB-6VM33

### Windows Server 2025:
- **Standard:** TBD (use generic conversion method)
- **Datacenter:** TBD (use generic conversion method)

## Important Limitations and Notes

### Security Restrictions:
- Full product keys are **never stored in plain text** in the registry
- Only **partial keys** (last 5 characters) are visible
- Keys are encrypted/hashed for security reasons

### Evaluation Edition Reality:
- Evaluation editions use **generic/public keys** that expire
- **No full retail key exists** in evaluation versions
- The partial key shown (e.g., "J2T92") is just the last 5 characters of the evaluation key

### Prerequisites for Conversion:
- Must have a **valid Windows Server 2025 Datacenter product key**
- Server **cannot be an Active Directory Domain Controller** (must demote first)
- Cannot downgrade editions (Datacenter Eval can only go to Datacenter full)
- Process requires system restart and takes several minutes

### Troubleshooting:
- If process hangs over 20 minutes: `Stop-Service sppsvc -Force`
- Check available target editions: `DISM /online /Get-TargetEditions`
- Verify current edition: `DISM /online /Get-CurrentEdition`

## Alternative Solutions

### Enterprise Options:
1. **Volume Licensing/KMS Server** activation
2. **Azure Hybrid Benefit** if applicable
3. **SPLA licensing** for service providers

### Testing Options:
1. **Continue with evaluation** (170 days remaining in example)
2. **Extend evaluation period** (limited rearms available)
3. **Fresh installation** with new 180-day period

## Summary

While various PowerShell and registry methods exist to extract product keys, **Windows Server evaluation editions typically do not contain extractable full retail keys**. The evaluation is designed to require purchasing a legitimate license for permanent activation.

**Bottom Line:** You will most likely need to purchase a Windows Server 2025 Datacenter license key to convert from evaluation to full version.

---
*Generated: 2025-08-06*
*Context: Windows Server 2025 Datacenter Evaluation Edition conversion*
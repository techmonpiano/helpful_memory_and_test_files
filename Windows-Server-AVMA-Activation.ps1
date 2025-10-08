#Requires -RunAsAdministrator

# AVMA Keys for Windows Server editions
$AVMAKeys = @{
    "2025_Datacenter" = "YQB4H-NKHHJ-Q6K4R-4VMY6-VCH67"
    "2025_Standard" = "WWVGQ-PNHV9-B89P4-8GGM9-9HPQ4"
    "2022_Datacenter" = "W3GNR-8DDXR-2TFRP-H8P33-DV9BG"
    "2022_Standard" = "YDFWN-MJ9JR-3DYRK-FXXRW-78VHK"
    "2019_Datacenter" = "H3RNG-8C32Q-Q8FRX-6TDXV-WMBMW"
    "2019_Standard" = "TNK62-RXVTB-4P47B-2D623-4GF74"
    "2019_Essentials" = "2CTP7-NHT64-BP62M-FV6GG-HFV28"
    "2016_Datacenter" = "Y4TGP-NPTV9-HTC2H-7MGQ3-DV4TW"
    "2016_Standard" = "DBGBW-NPF86-BJVTX-K3WKJ-MTB6V"
    "2016_Essentials" = "K2XGM-NMBT3-2R6Q8-WF2FK-P36R2"
}

function Write-ColorOutput {
    param(
        [string]$Message,
        [string]$Color = "White"
    )
    Write-Host $Message -ForegroundColor $Color
}

function Get-WindowsServerInfo {
    try {
        $OSInfo = Get-CimInstance -ClassName Win32_OperatingSystem
        $OSCaption = $OSInfo.Caption
        
        $Version = ""
        $Edition = ""
        
        if ($OSCaption -match "Windows Server (\d{4})") {
            $Version = $Matches[1]
        }
        
        if ($OSCaption -match "Datacenter") {
            $Edition = "Datacenter"
        }
        elseif ($OSCaption -match "Standard") {
            $Edition = "Standard"
        }
        elseif ($OSCaption -match "Essentials") {
            $Edition = "Essentials"
        }
        
        return @{
            FullName = $OSCaption
            Version = $Version
            Edition = $Edition
            Key = "${Version}_${Edition}"
        }
    }
    catch {
        Write-ColorOutput "Error detecting Windows Server information: $($_.Exception.Message)" "Red"
        return $null
    }
}

function Invoke-AVMAActivation {
    param(
        [string]$AVMAKey
    )
    
    try {
        Write-ColorOutput "Step 1: Removing existing product key..." "Cyan"
        $result1 = & cscript //nologo C:\Windows\System32\slmgr.vbs /upk 2>&1
        Write-ColorOutput $result1 "Gray"
        
        Write-ColorOutput "Step 2: Installing AVMA key: $AVMAKey" "Cyan"
        $result2 = & cscript //nologo C:\Windows\System32\slmgr.vbs /ipk $AVMAKey 2>&1
        Write-ColorOutput $result2 "Gray"
        
        if ($result2 -like "*successfully*" -or $result2 -like "*installed*") {
            Write-ColorOutput "Step 3: Activating through Hyper-V host..." "Cyan"
            $result3 = & cscript //nologo C:\Windows\System32\slmgr.vbs /ato 2>&1
            Write-ColorOutput $result3 "Gray"
            
            if ($result3 -like "*successfully*" -or $result3 -like "*activated*") {
                Write-ColorOutput "AVMA activation completed successfully!" "Green"
                return $true
            }
            else {
                Write-ColorOutput "Activation failed. Check Hyper-V host configuration." "Red"
                return $false
            }
        }
        else {
            Write-ColorOutput "Failed to install AVMA key." "Red"
            return $false
        }
    }
    catch {
        Write-ColorOutput "Error during activation: $($_.Exception.Message)" "Red"
        return $false
    }
}

function Show-ActivationStatus {
    try {
        Write-ColorOutput "=== Current Activation Status ===" "Cyan"
        $status = & cscript //nologo C:\Windows\System32\slmgr.vbs /dlv 2>&1
        Write-ColorOutput $status "White"
    }
    catch {
        Write-ColorOutput "Error retrieving activation status: $($_.Exception.Message)" "Red"
    }
}

# Main execution
Write-ColorOutput "Windows Server AVMA Activation Script" "Green"
Write-ColorOutput "=====================================" "Green"

# Check if running as administrator
if (-not ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-ColorOutput "This script must be run as Administrator!" "Red"
    exit 1
}

# Detect Windows Server information
Write-ColorOutput "Detecting Windows Server edition..." "Cyan"
$ServerInfo = Get-WindowsServerInfo

if (-not $ServerInfo) {
    Write-ColorOutput "Failed to detect Windows Server information. Exiting." "Red"
    exit 1
}

Write-ColorOutput "Detected: $($ServerInfo.FullName)" "White"
Write-ColorOutput "Version: $($ServerInfo.Version)" "White"
Write-ColorOutput "Edition: $($ServerInfo.Edition)" "White"

# Check if AVMA key exists for this edition
if (-not $AVMAKeys.ContainsKey($ServerInfo.Key)) {
    Write-ColorOutput "No AVMA key available for $($ServerInfo.Key)" "Red"
    Write-ColorOutput "Available editions:" "Yellow"
    $AVMAKeys.Keys | Sort-Object | ForEach-Object { Write-ColorOutput "  - $_" "Yellow" }
    exit 1
}

$SelectedKey = $AVMAKeys[$ServerInfo.Key]
Write-ColorOutput "AVMA Key for $($ServerInfo.Key): $SelectedKey" "White"

# Confirm activation
Write-ColorOutput "Ready to activate $($ServerInfo.FullName) using AVMA" "Yellow"
$Confirm = Read-Host "Continue? (Y/N)"

if ($Confirm -notmatch "^[Yy]") {
    Write-ColorOutput "Activation cancelled by user." "Yellow"
    exit 0
}

# Perform AVMA activation
Write-ColorOutput "Starting AVMA activation process..." "Green"
$Success = Invoke-AVMAActivation -AVMAKey $SelectedKey

# Show final status
Show-ActivationStatus

if ($Success) {
    Write-ColorOutput "Windows Server AVMA activation completed successfully!" "Green"
    Write-ColorOutput "The VM should now be activated through the Hyper-V host." "Green"
} else {
    Write-ColorOutput "AVMA activation failed. Please check:" "Red"
    Write-ColorOutput "  - Hyper-V host is running Datacenter edition" "Red"
    Write-ColorOutput "  - Hyper-V host is properly activated" "Red"
    Write-ColorOutput "  - Data Exchange integration service is enabled" "Red"
    Write-ColorOutput "  - VM can communicate with the host" "Red"
}
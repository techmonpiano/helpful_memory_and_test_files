# uStandard ISO Build Session Memory Bank
Generated: 2025-07-16

## Project Overview
- **Repository**: https://github.com/linuxmative/uStandard
- **Author**: Maksym Titenko (@titenko)
- **Purpose**: Build custom Ubuntu Live ISO with minimal system + desktop environment
- **License**: MIT

## Safety Assessment
✅ **Safe to use** - Open source, transparent build process
⚠️ **Security notes**: 
  - Default passwords (root/toor, ubuntu/ubuntu, ustandard/ustandard)
  - Auto-login enabled by default
  - Recommended for testing/development only without hardening

## Configuration Used
- **Ubuntu Version**: 25.04 "Plucky Puffin" (development/alpha)
- **Desktop**: GNOME Minimal (ubuntu-desktop-minimal)
- **Username**: myuser
- **Password**: changeme123
- **ISO Name**: CustomUbuntu-20250715.iso

## System Requirements Check
- Host OS: Zorin OS 17.3 (Ubuntu 22.04 based)
- Available RAM: 19GB of 28GB ✅
- Available Disk: 8.8GB ⚠️ (tight but workable)
- Required packages installed via apt

## Files Created
1. `/home/user1/uStandard/custom_config.sh` - Configuration variables
2. `/home/user1/uStandard/build_custom.sh` - Wrapper script with customizations
3. Modified `uStandard.sh` to use Ubuntu 25.04 "Plucky"

## Ubuntu Version Options Configured
- noble (24.04 LTS) - Stable, long-term support until 2029
- oracular (24.10) - Latest stable release
- plucky (25.04) - Development version (selected)

## Build Process Details
- Uses debootstrap to create base system
- Installs packages from official Ubuntu repositories
- Creates hybrid ISO with BIOS + UEFI support
- Build time: 30-60 minutes
- Output location: `/home/user1/uStandard/CustomUbuntu-[date].iso`

## Important Commands
```bash
# Navigate to directory
cd /home/user1/uStandard

# Run the build
./build_custom.sh

# Check available Ubuntu versions
curl -s http://archive.ubuntu.com/ubuntu/dists/ | grep -o '[^"/]*' | sort
```

## Customization Notes
- Desktop environments available: gnome, kde, xfce, mate, lxqt, none
- GNOME minimal uses ~1.2-1.5GB vs full GNOME at ~2.5-3GB
- XFCE recommended for low disk space (~800MB)
- Additional software options: office, multimedia, development, games, browsers

## Build Space Requirements
- Build workspace: ~2-3GB
- Final ISO: ~2-3GB  
- Temporary files: ~1-2GB
- Total needed: ~6-8GB minimum

## Security Hardening Needed
1. Change all default passwords
2. Disable auto-login if not needed
3. Consider disabling root login
4. Review installed packages
5. Update system after installation

## Troubleshooting
- If build fails due to space: Use XFCE instead of GNOME
- If packages fail to download: Check internet connection
- If sudo fails: Run directly in terminal, not through automation
- Development version (25.04) may have package availability issues

## Ubuntu 25.04 Compatibility Fixes Applied
**Issue**: Build failed with package errors:
- `policykit-1` - Package not available (obsoleted)
- `wireless-tools` - Package not available (deprecated)

**Solution Applied**:
1. Created fix script: `/home/user1/uStandard/fix_ubuntu_25.04.sh`
2. Replaced deprecated packages:
   - `policykit-1` → `polkitd pkexec` (new PolicyKit implementation)
   - `wireless-tools` → removed (deprecated, functionality in `iw`)
3. Added modern replacements:
   - Added `iw` package for wireless configuration
   - Already had `iwd` (Intel Wireless Daemon) for modern WiFi

**Package Changes in uStandard.sh**:
```bash
# Line 223 - Network packages
network-manager iw wpasupplicant bluez rfkill iwd

# Line 241 - Desktop infrastructure
dbus-x11 polkitd pkexec udisks2 upower gvfs gvfs-backends libnotify-bin dconf-gsettings-backend
```

**Why These Changes**:
- Ubuntu 25.04 modernized PolicyKit to separate daemon (polkitd) and execution tool (pkexec)
- Wireless-tools is legacy, replaced by `iw` (nl80211 based) and `iwd` (modern WiFi daemon)
- These are upstream Ubuntu/Debian changes, not specific to this project

**Build Status**: Ready to retry with fixed packages
**Script Backup**: Original saved as `uStandard.sh.backup`
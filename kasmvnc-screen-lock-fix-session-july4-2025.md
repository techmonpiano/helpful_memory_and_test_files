# KasmVNC Screen Lock Fix Session - July 4, 2025

## Session Overview
This memory bank documents the investigation and solution for the GNOME lock screen password input issue in KasmVNC, where users cannot type passwords when the screen locks via GDM.

## The Problem
- **Issue**: When GNOME screen locks in a KasmVNC session, users cannot type their password
- **Symptoms**: 
  - Password field constantly refreshes
  - Only 1-2 characters can be typed before field clears
  - "Authentication error" messages appear
  - Error: "JS ERROR: Failed to open reauthentification channel: Gio.DBusError:org.freedesktop.DBUS.Error.AccessDenied: No session available"
- **Root Cause**: Known issue with VNC sessions and GNOME/GDM lock screen authentication

## Solutions Discovered

### 1. Primary Solution: Disable Screen Lock in xstartup (Recommended)
Add these lines to `~/.vnc/xstartup` BEFORE starting gnome-session:

```bash
# Disable screen lock and screensaver
gsettings set org.gnome.desktop.screensaver lock-enabled false
gsettings set org.gnome.desktop.screensaver idle-activation-enabled false
gsettings set org.gnome.desktop.session idle-delay 0
```

**Benefits**:
- Only affects VNC sessions, not physical login
- Maintains security for physical access
- No system-wide changes needed
- Clean, permanent solution

### 2. Emergency Workaround: SSH Unlock
If screen is already locked:
```bash
ssh user@machine
loginctl unlock-session
```

### 3. Alternative: Manual Disable via GUI
Within VNC session:
- Settings → Privacy → Screen Lock
- Turn off "Automatic Screen Lock"
- Turn off "Lock Screen on Suspend"

### 4. System-wide Disable (Not Recommended)
Create `/etc/dconf/db/local.d/00-screensaver`:
```ini
[org/gnome/desktop/screensaver]
lock-enabled=false
idle-activation-enabled=false

[org/gnome/desktop/session]
idle-delay=uint32 0
```
Then run: `sudo dconf update`

**Warning**: This affects ALL sessions including physical login!

## Complete xstartup Configuration
Here's the full xstartup file with screen lock disabled:

```bash
#!/bin/sh
unset SESSION_MANAGER
unset DBUS_SESSION_BUS_ADDRESS
export XKL_XMODMAP_DISABLE=1
export XDG_CURRENT_DESKTOP=zorin:GNOME
export XDG_SESSION_DESKTOP=zorin
export XDG_SESSION_TYPE=x11
export DISPLAY=:3

# Create runtime directory
export XDG_RUNTIME_DIR=/tmp/runtime-user1
mkdir -p $XDG_RUNTIME_DIR
chmod 700 $XDG_RUNTIME_DIR

[ -r $HOME/.Xresources ] && xrdb $HOME/.Xresources
xsetroot -solid grey
vncconfig -iconic &

# Disable screen lock and screensaver
gsettings set org.gnome.desktop.screensaver lock-enabled false
gsettings set org.gnome.desktop.screensaver idle-activation-enabled false
gsettings set org.gnome.desktop.session idle-delay 0

# Start Zorin desktop session
exec dbus-launch --exit-with-session gnome-session --session=zorin
```

## Important Notes

1. **Session Isolation**: The gsettings commands in xstartup only affect the VNC session, not the physical GNOME session
2. **Verification**: You can verify settings are different between sessions:
   ```bash
   # Check VNC session
   DISPLAY=:3 gsettings get org.gnome.desktop.screensaver lock-enabled
   
   # Check physical session
   DISPLAY=:0 gsettings get org.gnome.desktop.screensaver lock-enabled
   ```

## Tasks Remaining on Correct Machine (shawnbeelinkzorin)

### 1. Update xstartup file
- **Location**: `/home/user1/.vnc/xstartup`
- **Action**: Add the gsettings commands to disable screen lock
- **Insert Location**: After the vncconfig line, before exec dbus-launch

### 2. Update the documentation file
- **File**: `kasmvnc-zorin-ubuntu-setup-session-july2025.md`
- **Action**: Append new section about screen lock fix
- **Content**: Include problem description, solutions, and the updated xstartup

### 3. Update install scripts
The following install scripts need the screen lock fix added to their xstartup generation:
- `kasmvnc-auto-install-ubuntu-focal.sh`
- `kasmvnc-auto-install-ubuntu-noble.sh`
- Any other KasmVNC install scripts

**Changes needed**:
Add after line 190 (vncconfig -iconic &) in the xstartup creation section:
```bash
# Disable screen lock and screensaver for VNC session
gsettings set org.gnome.desktop.screensaver lock-enabled false
gsettings set org.gnome.desktop.screensaver idle-activation-enabled false
gsettings set org.gnome.desktop.session idle-delay 0
```

### 4. Test the changes
1. Restart KasmVNC service: `sudo systemctl restart kasmvnc@user1.service`
2. Connect to VNC session
3. Verify screen lock is disabled in Settings
4. Let session idle to confirm no lock screen appears

## Research Sources
- Multiple Stack Exchange and forum posts confirm this is a widespread VNC/GNOME issue
- Red Hat Bug #1827469 tracks this problem
- Affects TigerVNC, KasmVNC, and other VNC implementations
- Issue persists in GNOME 3.36 and later versions

## Connection Details for shawnbeelinkzorin
- **URL**: https://100.94.240.101:8446
- **User**: vncuser1
- **Display**: :3
- **Service**: kasmvnc@user1.service

---
*Memory bank created July 4, 2025 to continue work on correct machine*
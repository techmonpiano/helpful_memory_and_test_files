# KasmVNC Zorin/Ubuntu Setup Session - July 4, 2025

## Overview
Complete troubleshooting session for setting up KasmVNC on Zorin OS (Ubuntu-based) with full desktop functionality including panels, menus, and right-click context menus.

## Initial Problem
- KasmVNC service was installed and running but showed "Oh no something has gone wrong" GNOME error
- Black screen or minimal desktop with only VNC clipboard options visible
- Missing desktop panels, application menus, and right-click functionality

## System Information
- **OS**: Zorin OS (Ubuntu-based)
- **KasmVNC Version**: Running on port 8446
- **Service**: kasmvnc@user1.service
- **VNC Display**: :3
- **PID File Issue**: Initially expected localhost:3.pid but created shawnbeelinkzorin:3.pid

## Troubleshooting Steps Attempted

### 1. Initial Service Status Check
```bash
sudo systemctl status kasmvnc@user1.service
```
- Service showed "activating" state despite running processes
- Root cause: Incorrect PID file path in systemd service

### 2. PID File Fix
**Problem**: Service expected `/home/user1/.vnc/localhost:3.pid` but actual file was `/home/user1/.vnc/shawnbeelinkzorin:3.pid`

**Solution**:
```bash
sudo sed -i 's/PIDFile=\/home\/%i\/.vnc\/localhost:3.pid/PIDFile=\/home\/%i\/.vnc\/shawnbeelinkzorin:3.pid/' /etc/systemd/system/kasmvnc@.service
sudo systemctl daemon-reload
sudo systemctl restart kasmvnc@user1.service
```

### 3. Desktop Environment Fixes (Multiple Attempts)

#### Attempt 1: Environment Variables Fix
Added missing environment variables to `~/.vnc/xstartup`:
- `XDG_RUNTIME_DIR=/tmp/runtime-user1`
- `XDG_SESSION_CLASS=user`
- `XDG_SESSION_ID=c1`

**Result**: Still showed GNOME error screen

#### Attempt 2: GNOME Flashback Configuration
Tried GNOME Flashback session configuration:
```bash
export XDG_CURRENT_DESKTOP="GNOME-Flashback:GNOME"
export XDG_MENU_PREFIX="gnome-flashback-"
gnome-session --session=gnome-flashback-metacity
```

**Result**: Package not installed on Zorin

#### Attempt 3: Individual Component Approach
Started individual desktop components:
```bash
metacity &
gnome-panel &
nautilus &
gnome-terminal &
```

**Result**: Nautilus worked but no panels or right-click menus

#### Attempt 4: Enhanced Component Mode
Added `gnome-settings-daemon` and proper startup sequence:
```bash
metacity &
gnome-settings-daemon &
gnome-panel &
nautilus &
```

**Result**: Still missing full desktop functionality

### 4. **FINAL WORKING SOLUTION: Zorin-Specific Session**

**Key Discovery**: Zorin OS requires its own session configuration, not generic Ubuntu or GNOME Flashback.

**Working xstartup Configuration**:
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

# Start Zorin desktop session
exec dbus-launch --exit-with-session gnome-session --session=zorin
```

**Result**: ✅ **COMPLETE SUCCESS** - Full Zorin desktop with panels, menus, right-click functionality

## Authorization/Keyring Issue

### Problem
Upon successful desktop login, Ubuntu keyring prompts for password to unlock stored credentials.

### Solutions

#### Option 1: Enter Password (Temporary)
- Enter user account password when prompted
- Unlocks keyring for current session only

#### Option 2: Disable Keyring Password (Permanent - Global)
1. Open "Passwords and Keys" application
2. Find "Login" keyring
3. Right-click → "Change Password"
4. Enter current password
5. Leave new password **blank**
6. Confirm (warns about unencrypted storage)

**Impact**: Affects ALL login methods (physical, VNC, SSH)

#### Option 3: Session-Specific Disable (VNC Only)
Add to xstartup file:
```bash
export GNOME_KEYRING_CONTROL=""
export SSH_AUTH_SOCK=""
```

**Impact**: Only affects VNC sessions, keeps security for physical login

## Key Lessons Learned

1. **OS-Specific Sessions Matter**: Generic Ubuntu/GNOME configurations don't work on Zorin - need `--session=zorin`

2. **PID File Paths**: Always check actual PID file naming vs. systemd service expectations

3. **Environment Variables**: Critical for proper desktop initialization:
   - `XDG_CURRENT_DESKTOP=zorin:GNOME`
   - `XDG_SESSION_DESKTOP=zorin`
   - `XDG_RUNTIME_DIR` creation and permissions

4. **Complete Session vs. Components**: Individual component launching (metacity, gnome-panel, etc.) doesn't provide full desktop integration - need proper session manager

## Research Sources
- KasmVNC GitHub Issues #264 (Black/Blank Screen Solutions)
- Ubuntu Forums: GNOME panel and menu bar issues
- VNC-specific desktop environment configuration guides
- Ubuntu keyring management documentation

## Final Working Configuration Files

### `/home/user1/.vnc/xstartup` (Final Version)
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

# Start Zorin desktop session
exec dbus-launch --exit-with-session gnome-session --session=zorin
```

### Systemd Service File Fix
Path: `/etc/systemd/system/kasmvnc@.service`
Change: `PIDFile=/home/%i/.vnc/localhost:3.pid` → `PIDFile=/home/%i/.vnc/shawnbeelinkzorin:3.pid`

## Connection Information
- **URL**: https://100.94.240.101:8446
- **User**: vncuser1
- **Display**: :3
- **Service**: kasmvnc@user1.service

## Status: ✅ FULLY FUNCTIONAL
- Complete Zorin desktop environment
- Taskbar/panels working
- Application menus accessible
- Right-click context menus functional
- File manager (Nautilus) integrated
- Terminal access available
- All desktop functionality restored

## Screen Lock Fix - Password Input Issue

### Problem Identified
After successful desktop setup, users encountered an issue where the GNOME screen lock prevented password input in VNC sessions:
- Password field constantly refreshes
- Only 1-2 characters can be typed before field clears
- "Authentication error" messages appear
- Error: "JS ERROR: Failed to open reauthentification channel: Gio.DBusError:org.freedesktop.DBUS.Error.AccessDenied: No session available"

### Root Cause
This is a known issue with VNC sessions and GNOME/GDM lock screen authentication that affects TigerVNC, KasmVNC, and other VNC implementations in GNOME 3.36 and later versions.

### Solution Implemented
Added screen lock disable commands to the xstartup file to prevent the lock screen from appearing in VNC sessions while maintaining security for physical login.

**Updated xstartup Configuration**:
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

### Key Benefits
- Only affects VNC sessions, not physical login
- Maintains security for physical access
- No system-wide changes needed
- Clean, permanent solution

### Emergency Workaround
If screen is already locked, unlock via SSH:
```bash
ssh user@machine
loginctl unlock-session
```

---
*Session completed July 4, 2025 - Full desktop environment successfully configured*
*Screen lock fix implemented July 4, 2025 - VNC password input issue resolved*
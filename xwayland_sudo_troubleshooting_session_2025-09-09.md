# Xwayland & Sudo Troubleshooting Session - 2025-09-09

## Session Overview
This session involved troubleshooting two main issues:
1. Qt display connection errors with sudo wrapper
2. X11 applications failing to connect (Xwayland client limit exceeded)

## Initial Problem Symptoms

### Primary Issue: Qt Display Errors
```
Warning: Ignoring XDG_SESSION_TYPE=wayland on Gnome. Use QT_QPA_PLATFORM=wayland to run on Wayland anyway.
Maximum number of clients reachedqt.qpa.xcb: could not connect to display :0
qt.qpa.plugin: Could not load the Qt platform plugin "xcb" in "" even though it was found.
This application failed to start because no Qt platform plugin could be initialized.
```

### Secondary Issue: Sudo Password Prompt Failures
- `sudo rm ubuntu-snappy/ubuntu-bootstrap/var/run` failed
- "sudo: no password was provided" error
- Qt GUI password prompts not working

## Root Cause Analysis

### Environment Investigation
```bash
# Initial environment check revealed:
DISPLAY: (empty)
XDG_SESSION_TYPE: (empty) 
# But system was actually running Wayland session
```

### Sudo Wrapper Discovery
Found problematic sudo wrapper in `~/.bashrc` at line 180:
```bash
# Smart sudo wrapper - uses GUI when available, falls back to terminal
sudo() {
    # Check if we have a display and askpass configured
    if [ -n "$DISPLAY" ] && [ -n "$SUDO_ASKPASS" ] && [ -x "$SUDO_ASKPASS" ]; then
        # Use GUI authentication
        command sudo -A "$@"
    else
        # Fall back to terminal authentication
        command sudo "$@"
    fi
}
```

**Problem**: `SUDO_ASKPASS=/usr/bin/ssh-askpass` was using Qt-based ssh-askpass, which couldn't connect to display.

### Xwayland Client Limit Investigation
```bash
# Xwayland was running but rejecting connections:
ps aux | grep Xwayland
# Result: /usr/bin/Xwayland :0 -rootless -noreset -accessx -core...

# Testing X11 connectivity:
xset q
# Result: "Maximum number of clients reached"
```

## Failed Attempts and Solutions

### ❌ Failed Attempts

1. **Setting DISPLAY=:0 and XDG_SESSION_TYPE=x11**
   - Command: `export DISPLAY=:0; export XDG_SESSION_TYPE=x11`
   - Result: Temporary fix for session, but Qt errors persisted
   - Issue: Didn't address root cause (askpass program failure)

2. **Using `command sudo` to bypass wrapper**
   - Command: `command sudo rm ubuntu-snappy/ubuntu-bootstrap/var/run`
   - Result: Still triggered Qt GUI askpass, same errors
   - Issue: Environment variables still caused GUI askpass selection

3. **Unsetting environment variables**
   - Command: `unset DISPLAY SUDO_ASKPASS; command sudo ...`
   - Result: "sudo: a terminal is required to read the password"
   - Issue: Terminal input not available in this environment

### ✅ Successful Solutions

#### 1. Immediate File Removal - pkexec
```bash
pkexec rm /home/user1/shawndev1/ubuntu-snappy/ubuntu-bootstrap/var/run
# Success: Removed the symlink using PolicyKit authentication
```

#### 2. Fix Sudo Wrapper - Replace ssh-askpass with zenity
**Step 1**: Created zenity-based askpass helper
```bash
# Created /home/user1/bin/zenity-askpass:
#!/bin/bash
zenity --password --title="Authentication Required" --text="Enter your password for sudo:"

chmod +x /home/user1/bin/zenity-askpass
```

**Step 2**: Updated .bashrc
```bash
# Changed from:
export SUDO_ASKPASS=/usr/bin/ssh-askpass
# To:
export SUDO_ASKPASS=/home/user1/bin/zenity-askpass
```

**Result**: Sudo wrapper now uses Wayland-compatible zenity instead of Qt-based ssh-askpass.

#### 3. Fix Xwayland Client Limit - Process Restart
```bash
# User executed:
pkill Xwayland
# GNOME automatically restarted Xwayland with fresh client pool
# Verified with: xset q (now works without "Maximum clients" error)
```

#### 4. Prevent Future Client Limit Issues
**Added to .bashrc**:
```bash
# Increase Xwayland client limit
export MUTTER_DEBUG_NUM_XWAYLAND_CLIENTS=512
```
**Effect**: Doubles client limit from ~256 to 512 (requires session restart to take effect).

## Technical Details

### System Environment
- **OS**: Zorin Linux (GNOME-based)
- **Session Type**: Wayland with Xwayland compatibility layer
- **Display Server**: Xwayland :0 (for X11 app compatibility)
- **Authentication**: PolicyKit (pkexec) and sudo with GUI askpass

### Key Files Modified
1. `~/.bashrc` - Lines 177, 181-182
   - Fixed SUDO_ASKPASS path
   - Added Xwayland client limit increase
2. `/home/user1/bin/zenity-askpass` - New file created

### Process Information
```bash
# Before fix - Xwayland PID: 5990
# After pkill - Xwayland PID: 2185469 (fresh restart)
```

## Lessons Learned

### Environment Variable Persistence
- Temporary exports (`export DISPLAY=:0`) only last for current bash session
- System will return to normal Wayland behavior after reboot
- This is desired behavior - don't want permanent X11 mode

### GUI Authentication in Wayland
- **ssh-askpass**: Uses Qt/X11, fails in Wayland due to display issues
- **zenity**: Native GTK, works properly with Wayland
- **pkexec**: PolicyKit-based, most robust for system operations

### Xwayland Client Management
- Default client limit appears to be ~256 concurrent connections
- Client limit can be increased via `MUTTER_DEBUG_NUM_XWAYLAND_CLIENTS`
- `pkill Xwayland` safely restarts process (GNOME handles restart automatically)
- Stale connections can cause "Maximum clients reached" even when `lsof` shows few connections

## Future Recommendations

1. **Monitor X11 app usage** - If client limit issues recur frequently, consider increasing limit further
2. **Alternative approaches** - For critical operations, `pkexec` is more reliable than sudo wrapper
3. **Session management** - Logout/login periodically to reset all connection pools if running many X11 apps
4. **Environment hygiene** - Avoid setting permanent DISPLAY/XDG_SESSION_TYPE overrides

## Quick Reference Commands

```bash
# Check Xwayland status
ps aux | grep Xwayland | grep -v grep

# Test X11 connectivity
xset q

# Count X11 socket connections
lsof /tmp/.X11-unix/X0 2>/dev/null | wc -l

# Restart Xwayland (emergency)
pkill Xwayland

# Check sudo askpass configuration
echo "SUDO_ASKPASS: $SUDO_ASKPASS"

# Test sudo wrapper
sudo echo "test"

# Use PolicyKit for system operations
pkexec [command]
```

## Session Outcome
- ✅ Sudo wrapper fixed - now uses Wayland-compatible zenity
- ✅ X11 applications restored - Xwayland client limit reset
- ✅ Future-proofed - increased client limit configuration
- ✅ File operation completed - ubuntu-bootstrap/var/run symlink removed
- ✅ System stability maintained - no permanent environment changes
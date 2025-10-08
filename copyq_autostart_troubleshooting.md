# CopyQ Autostart Troubleshooting Guide

## Problem
CopyQ autostart entry was failing to start properly, showing D-Bus integration issues and clipboard access timeouts.

## Symptoms Found in Logs
```bash
# Check logs with:
journalctl --since "today" | grep -i copyq
```

**Key issues identified:**
- Multiple instances: "CopyQ server is already running"
- D-Bus menu warnings: "QVariantMap DBusMenuExporterDBus::getProperties(int, const QStringList&) const: Condition failed: action"
- Clipboard access timeouts: "ELAPSED 10000 ms accessing hasText" and "Clipboard data expired, refusing to access old data"

## Solution Applied

### 1. Increased Autostart Delay
**File:** `/home/user1/.config/autostart/copyq.desktop`
**Change:** 
```diff
- X-GNOME-Autostart-Delay=3
+ X-GNOME-Autostart-Delay=5
```
**Reason:** Gives desktop environment more time to fully load before starting CopyQ

### 2. Added Environment Variable to Suppress D-Bus Warnings
**Change:**
```diff
- Exec="/usr/bin/copyq"
+ Exec=env QT_LOGGING_RULES="*.debug=false" "/usr/bin/copyq"
```
**Reason:** Suppresses cosmetic Qt D-Bus integration warnings that don't affect functionality

## Final Working Configuration
```ini
[Desktop Entry]
Name=CopyQ
Icon=copyq
GenericName=Clipboard Manager
# Workaround / fix for issue #1526 that prevents a proper autostart of the tray icon in GNOME
X-GNOME-Autostart-Delay=5
# The rest is taken from Klipper application.
Type=Application
Terminal=false
X-KDE-autostart-after=panel
X-KDE-StartupNotify=false
X-KDE-UniqueApplet=true
Categories=Qt;KDE;Utility;
# ... (localized names and descriptions) ...
Exec=env QT_LOGGING_RULES="*.debug=false" "/usr/bin/copyq"
Hidden=false
X-GNOME-Autostart-enabled=true
```

## Testing the Fix
```bash
# Kill existing CopyQ instance
killall copyq

# Test autostart entry manually
desktop-file-validate ~/.config/autostart/copyq.desktop

# Restart CopyQ
copyq

# Or log out and back in to test full autostart
```

## Additional Notes
- The D-Bus warnings are cosmetic Qt/GNOME integration issues and don't prevent CopyQ from functioning
- CopyQ was actually starting successfully but having clipboard access timing issues
- The timeout warnings suggest desktop environment permission or timing conflicts
- The `X-GNOME-Autostart-Delay` parameter is specifically designed for this type of issue

## Alternative Solutions (if above doesn't work)
1. **Use systemd user service instead of autostart:**
   ```bash
   systemctl --user enable copyq.service
   ```

2. **Add to shell startup script:**
   ```bash
   echo "(sleep 10; copyq) &" >> ~/.bashrc
   ```

3. **Check CopyQ preferences:**
   - Open CopyQ → Preferences → General → "Autostart"
   - Ensure "Start the server on system startup" is checked

## Date Fixed
July 15, 2025

## System Info
- OS: Linux 6.8.0-60-generic (Zorin/GNOME)
- CopyQ: Installed via package manager
- Desktop Environment: GNOME with autostart support
# Gnome Settings Restore and Extension Troubleshooting Guide
*July 2025 - KasmVNC Installation Impact Resolution*

## Issue Summary
After installing KasmVNC, Gnome desktop settings were reset to defaults. Extensions and custom desktop layout were lost despite successful dconf database restoration from Timeshift backup.

## Root Cause Discovery
The primary issue was **`disable-user-extensions` was set to `true`**, which globally disabled all user extensions regardless of the enabled-extensions list in dconf.

## Complete Resolution Steps

### 1. Restore Gnome Settings from Timeshift Backup
```bash
# Backup current settings first
mkdir -p ~/gnome-backup-current
cp -r ~/.config/dconf ~/gnome-backup-current/ 2>/dev/null || echo "No dconf directory found"
cp -r ~/.local/share/gnome-shell ~/gnome-backup-current/ 2>/dev/null || echo "No gnome-shell directory found"

# Restore from Timeshift backup
BACKUP_PATH="/run/timeshift/backup/timeshift-btrfs/snapshots/2025-05-30_13-22-15/@home/user1"

# Core Gnome settings (dconf database)
cp -r $BACKUP_PATH/.config/dconf ~/.config/

# Gnome extensions
rm -rf ~/.local/share/gnome-shell
cp -r $BACKUP_PATH/.local/share/gnome-shell ~/.local/share/

# GTK and session configs
cp -r $BACKUP_PATH/.config/gtk-3.0 ~/.config/ 2>/dev/null || echo "No gtk-3.0 in backup"
cp -r $BACKUP_PATH/.config/gtk-4.0 ~/.config/ 2>/dev/null || echo "No gtk-4.0 in backup"
cp -r $BACKUP_PATH/.config/gnome-session ~/.config/ 2>/dev/null || echo "No gnome-session in backup"
cp -r $BACKUP_PATH/.config/gnome-control-center ~/.config/ 2>/dev/null || echo "No gnome-control-center in backup"
cp -r $BACKUP_PATH/.config/autostart ~/.config/ 2>/dev/null || echo "No autostart in backup"
cp -r $BACKUP_PATH/.config/nautilus ~/.config/ 2>/dev/null || echo "No nautilus in backup"
cp -r $BACKUP_PATH/.gnome ~/. 2>/dev/null || echo "No .gnome directory in backup"
```

### 2. Key Diagnostic Commands
```bash
# Check enabled extensions
gnome-extensions list --enabled

# Check dconf enabled-extensions list
dconf read /org/gnome/shell/enabled-extensions

# CRITICAL: Check if user extensions are globally disabled
gsettings get org.gnome.shell disable-user-extensions
```

### 3. Fix Global Extension Disable Issue
```bash
# Enable user extensions globally (THIS WAS THE KEY FIX)
gsettings set org.gnome.shell disable-user-extensions false
```

### 4. Alternative Extension Management
```bash
# If needed, manually set enabled extensions via dconf
dconf write /org/gnome/shell/enabled-extensions "['extension1@example.com', 'extension2@example.com']"

# Enable specific extensions manually
gnome-extensions enable extension-name@domain.com
```

### 5. Gnome Shell Restart Methods

**For X11 Sessions:**
- Alt+F2 → type "r" → Enter

**For Wayland Sessions:**
- Alt+F2 + "r" does NOT work in Wayland
- Use: `killall -3 gnome-shell` (but this disconnects active sessions/terminals)
- Alternative: Logout and login
- Alternative: `sudo systemctl restart gdm3` (full session restart)

## Common Gnome Extension Issues After Restore

1. **Global Extensions Disabled**: `disable-user-extensions=true` (most common)
2. **Missing Extension Packages**: Install `gnome-shell-extensions`
3. **Extension Compatibility**: Extensions may not work with newer Gnome versions
4. **Corrupted dconf Keys**: May need to reset extension-specific dconf keys
5. **Session Cache**: Sometimes requires complete logout/login

## Key Files and Directories Restored

### Core Settings
- `~/.config/dconf/user` - All Gnome desktop settings, preferences, keybindings

### Extensions
- `~/.local/share/gnome-shell/extensions/` - All installed extensions

### Theme and UI
- `~/.config/gtk-3.0/` and `~/.config/gtk-4.0/` - GTK theme settings
- `~/.config/gnome-session/` - Session configuration
- `~/.config/gnome-control-center/` - Control center settings

### Applications
- `~/.config/nautilus/` - File manager preferences
- `~/.config/autostart/` - Startup applications

## Verification Steps
```bash
# Verify extensions are enabled
gnome-extensions list --enabled

# Check global extension setting
gsettings get org.gnome.shell disable-user-extensions

# Should return: false
```

## Prevention for Future KasmVNC Installations
- Backup dconf settings before VNC installation: `dconf dump / > gnome-backup.dconf`
- Check `disable-user-extensions` setting after any system modifications
- Consider using isolated VNC user account to prevent main user impact

## Success Indicators
- Extensions appear in top bar (taskbar, menu, indicators)
- Custom desktop layout restored
- Themes and custom settings applied
- Startup applications working as before

---

## KasmVNC User Management and Multiple Sessions

### How KasmVNC Handles Users
**KasmVNC uses existing OS users** - it does NOT create new OS users during installation.

#### User Types:
1. **OS User**: Your existing system user (user1) who runs `vncserver`
2. **KasmVNC User**: Web authentication credentials (like "vncuser1") for browser access

#### Session Context:
- The desktop session inside VNC runs **as your existing OS user** with all your files, permissions, and settings
- KasmVNC **shares the same user environment** as your main desktop session
- Changes to global settings like `disable-user-extensions` affect both main desktop and VNC sessions

### Multiple Concurrent Sessions

#### Session Independence:
- **Main desktop**: Wayland display server (your physical session)
- **VNC session**: X11 display server (virtual session accessible via browser)
- **Both run simultaneously** without interfering with each other

#### What Works:
- ✅ **No session conflicts**: VNC won't kick out your existing Wayland session
- ✅ **Independent displays**: Separate virtual display (:2) for VNC
- ✅ **Same user permissions**: Access to all your files and settings
- ✅ **Resource isolation**: Different running processes between sessions

## Application Lock Conflicts in Multiple Sessions

### Browser Applications - MAJOR ISSUE:
Modern browsers use **lock files** to prevent multiple instances from accessing the same user profile simultaneously.

#### Firefox Conflicts:
```bash
# Error you'll see:
"Firefox is already running, but is not responding"

# Solutions:
firefox -no-remote -P "VNC-Profile"                    # Use separate profile
MOZ_NO_REMOTE=1 firefox                                # Environment variable
firefox -CreateProfile "VNC /home/user1/.mozilla/firefox-vnc"  # Create VNC profile
```

#### Chrome/Chromium Conflicts:
```bash
# Error you'll see:
"Chrome is already running"

# Solutions:
google-chrome --user-data-dir=/home/user1/.config/google-chrome-vnc  # Separate data dir
google-chrome --incognito                               # Incognito mode (less ideal)
```

### Other Applications with Potential Conflicts:
- **Email clients** (Thunderbird, Evolution) - lock file issues
- **Code editors** (VSCode) - may detect multiple sessions  
- **Some proprietary apps** - may prevent multiple instances

### Applications That Usually Work Fine:
- ✅ **Terminal applications** - no conflicts
- ✅ **Text editors** (nano, gedit) - typically OK
- ✅ **File managers** - usually work
- ✅ **Simple utilities** - generally no issues

### Best Practice Recommendations:

#### 1. Browser Strategy:
- **Different browsers**: Keep Firefox on main desktop, use Chrome in VNC
- **Dedicated profiles**: Set up separate browser profiles for VNC
- **Lightweight alternatives**: Use different browsers in VNC (e.g., Midori)

#### 2. Application Planning:
- **Web-based alternatives**: Use web apps instead of desktop apps when possible
- **Profile separation**: Create separate profiles for apps that support it
- **Alternative applications**: Use different but similar apps in each session

#### 3. Environment Variables:
```bash
# For applications that support it
MOZ_NO_REMOTE=1          # Firefox
CHROME_USER_DATA_DIR=    # Chrome custom data directory
```

### Workaround Summary:
While KasmVNC sessions work great for most applications, **plan around browser and application lock conflicts**. The most common solution is using different applications or separate profiles for conflicting software.

## KasmVNC Auto-Start Configuration

### Current Status: Manual Start Only
By default, KasmVNC does **not** auto-start on system reboot. You must manually run `vncserver` after each restart.

### Check for Existing Services
Before setting up auto-start, verify no conflicting services exist:
```bash
# Check for existing VNC/Kasm services
systemctl --user list-unit-files | grep -i vnc
systemctl list-unit-files | grep -i vnc
systemctl --user list-unit-files | grep -i kasm
systemctl list-unit-files | grep -i kasm
ls ~/.config/autostart/ | grep -i vnc
find /etc/systemd/system/ -name "*vnc*" -o -name "*kasm*"
```

### Auto-Start Method Options

#### Method 1: Systemd User Service (Recommended)
**Best for**: VNC available when user is logged in
```bash
# Create user systemd directory
mkdir -p ~/.config/systemd/user

# Create KasmVNC service file
cat > ~/.config/systemd/user/kasmvnc.service << 'EOF'
[Unit]
Description=KasmVNC Server
After=graphical-session.target

[Service]
Type=forking
ExecStart=/usr/bin/vncserver
ExecStop=/usr/bin/vncserver -kill :2
Restart=on-failure
RestartSec=5

[Install]
WantedBy=default.target
EOF

# Enable the service
systemctl --user enable kasmvnc.service

# Enable lingering (allows user services to start without login)
sudo loginctl enable-linger $USER

# Start immediately (optional)
systemctl --user start kasmvnc.service
```

#### Method 2: System-wide Service
**Best for**: Headless operation, VNC always available regardless of user login
```bash
# Create system service file (requires sudo)
sudo tee /etc/systemd/system/kasmvnc@.service << 'EOF'
[Unit]
Description=KasmVNC Server for %i
After=multi-user.target

[Service]
Type=forking
User=%i
ExecStart=/usr/bin/vncserver
ExecStop=/usr/bin/vncserver -kill :2
Restart=on-failure

[Install]
WantedBy=multi-user.target
EOF

# Enable for your user
sudo systemctl enable kasmvnc@user1.service

# Start immediately (optional)
sudo systemctl start kasmvnc@user1.service
```

#### Method 3: Desktop Autostart
**Best for**: GUI-dependent operation, only when desktop session is active
```bash
mkdir -p ~/.config/autostart
cat > ~/.config/autostart/kasmvnc.desktop << 'EOF'
[Desktop Entry]
Type=Application
Name=KasmVNC Server
Exec=/usr/bin/vncserver
Hidden=false
X-GNOME-Autostart-enabled=true
EOF
```

### Service Management Commands

#### For User Service (Method 1):
```bash
# Check status
systemctl --user status kasmvnc.service

# Start/stop/restart
systemctl --user start kasmvnc.service
systemctl --user stop kasmvnc.service
systemctl --user restart kasmvnc.service

# Enable/disable auto-start
systemctl --user enable kasmvnc.service
systemctl --user disable kasmvnc.service

# View logs
journalctl --user -u kasmvnc.service -f
```

#### For System Service (Method 2):
```bash
# Check status
sudo systemctl status kasmvnc@user1.service

# Start/stop/restart
sudo systemctl start kasmvnc@user1.service
sudo systemctl stop kasmvnc@user1.service
sudo systemctl restart kasmvnc@user1.service

# Enable/disable auto-start
sudo systemctl enable kasmvnc@user1.service
sudo systemctl disable kasmvnc@user1.service

# View logs
journalctl -u kasmvnc@user1.service -f
```

### Method Comparison

| Method | Starts When | Requires Login | Root Access | Best For |
|--------|-------------|----------------|-------------|----------|
| User Service | User logs in | Yes* | No | Desktop users |
| System Service | System boots | No | Yes (setup) | Headless/servers |
| Autostart | GUI session starts | Yes | No | GUI-only use |

*With `enable-linger`, user services can start without login

### Troubleshooting Auto-Start

#### Common Issues:
1. **Service fails to start**: Check logs with `journalctl`
2. **Wrong display number**: Update ExecStop to match actual display (`:1`, `:2`, etc.)
3. **Permission issues**: Ensure user has access to VNC commands
4. **X11 conflicts**: May need to clear lock files before starting

#### Verification Steps:
```bash
# After reboot, check if VNC is running
vncserver -list
netstat -tulpn | grep 8445
ps aux | grep vnc
```

### Recommendations:
- **Method 1 (User Service)**: Most common choice for desktop users
- **Method 2 (System Service)**: Best for remote-only access scenarios  
- **Method 3 (Autostart)**: Simplest but least reliable

Choose based on your usage pattern and whether you need VNC available before login.

---
*Resolution completed: July 2025*
*KasmVNC successfully installed without persistent Gnome impact*
*Multiple session compatibility documented*
*Auto-start configuration options documented*
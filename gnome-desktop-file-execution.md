# GNOME Shell / Nautilus Desktop File Execution

## Issue: .desktop Files Open in Text Editor Instead of Executing

### Environment
- **Desktop Environment**: GNOME Shell (Zorin OS, Ubuntu, Fedora, etc.)
- **File Manager**: Nautilus
- **GNOME Version**: 43+ (newer security restrictions)

### Problem
Double-clicking `.desktop` files in arbitrary folders opens them in a text editor instead of executing them, even when:
- File has executable permissions (`chmod +x`)
- File is marked as trusted (`gio set metadata::trusted true`)
- File syntax is valid

### Root Cause
**GNOME 43+ security policy**: `.desktop` files can only be executed from specific trusted locations:

1. **User Desktop**: `~/Desktop/`
2. **User Applications**: `~/.local/share/applications/`
3. **System Applications**: `/usr/share/applications/`
4. **Other XDG directories**: Defined in `$XDG_DATA_DIRS`

Files in arbitrary directories (like project folders) will **always** open in text editor for security reasons.

### Solutions

#### Solution 1: Install to Desktop (User-Friendly)
```bash
# Copy to Desktop
cp MyApp.desktop ~/Desktop/
chmod +x ~/Desktop/MyApp.desktop
gio set ~/Desktop/MyApp.desktop metadata::trusted true
```

**Pros**: Most visible, easy for end users
**Cons**: Clutters desktop

#### Solution 2: Install to Application Menu
```bash
# Copy to user applications directory
cp MyApp.desktop ~/.local/share/applications/
chmod +x ~/.local/share/applications/MyApp.desktop

# Update desktop database (optional but recommended)
update-desktop-database ~/.local/share/applications/
```

**Pros**: Appears in application menu/launcher, clean
**Cons**: Less discoverable for users

#### Solution 3: Use Shell Script Instead
```bash
# Instead of .desktop file, use .sh script
chmod +x launch_app.sh
# Double-click works directly
```

**Pros**: No location restrictions, portable
**Cons**: No icon in file manager, less "app-like"

#### Solution 4: Force Nautilus to Launch Executable Text Files (Not Recommended for Distribution)
```bash
# Set Nautilus to launch .desktop files from any location
dconf write /org/gnome/nautilus/preferences/executable-text-activation "'launch'"

# Alternative using gsettings
gsettings set org.gnome.nautilus.preferences executable-text-activation 'launch'

# Restart Nautilus for changes to take effect
nautilus -q
```

**Pros**: .desktop files work from any location, no need to move files
**Cons**:
- Security risk (disables GNOME's safety feature)
- Only affects your machine, not other users
- Not suitable for distributed applications
- Still requires file to be executable and trusted

**Security Warning**: This removes GNOME's protection against accidental execution of malicious .desktop files. Only use on trusted systems.

**When to use**: Development/testing only, not for production distributions

### Verification Commands

Check if file is trusted:
```bash
gio info MyApp.desktop | grep "metadata::trusted"
```

Check executable permissions:
```bash
ls -l MyApp.desktop  # Should show -rwxr-xr-x
```

Check GNOME Nautilus settings:
```bash
# Using gsettings
gsettings get org.gnome.nautilus.preferences executable-text-activation

# Using dconf (alternative method)
dconf read /org/gnome/nautilus/preferences/executable-text-activation

# Possible values: 'launch', 'ask', 'display'
# Note: Setting still exists in GNOME 43+ but has more restrictions
# Default in GNOME 43+: not set (uses hardcoded trusted-location-only behavior)
```

**Important**: Even with `executable-text-activation` set to `'launch'`, GNOME 43+ still restricts .desktop files to trusted locations by default. The setting only affects execution behavior within those restrictions.

### Best Practice for Distributable Apps

**Setup Script Approach** (Recommended):
```bash
#!/bin/bash
# SETUP_DESKTOP_LAUNCHER.sh

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DESKTOP_FILE="$SCRIPT_DIR/MyApp.desktop"
DESKTOP_DIR="$HOME/Desktop"

# Copy to Desktop
cp "$DESKTOP_FILE" "$DESKTOP_DIR/"
chmod +x "$DESKTOP_DIR/MyApp.desktop"
gio set "$DESKTOP_DIR/MyApp.desktop" metadata::trusted true

echo "Desktop launcher installed!"
```

### Desktop File Requirements for GNOME

**Use Absolute Paths** (critical for portability):
```ini
[Desktop Entry]
Version=1.0
Type=Application
Name=My Application
Exec=/absolute/path/to/launcher.sh
Path=/absolute/path/to/app/directory
Icon=/absolute/path/to/icon.png
Terminal=false
Categories=Utility;
```

**Why absolute paths?**
- Relative paths fail when .desktop file is moved/copied
- `%p` (path substitution) not reliable across all file managers
- Absolute paths work from any location

### Icon Cache Updates (Cross-Desktop Compatibility)

```bash
# GTK/GNOME apps
gtk-update-icon-cache -f ~/.icons/hicolor/

# Cross-desktop standard (KDE, XFCE, etc.)
xdg-icon-resource forceupdate
```

### Related Commands

**Set file as trusted**:
```bash
gio set file.desktop metadata::trusted true
```

**Check file metadata**:
```bash
gio info file.desktop
```

**Update desktop database**:
```bash
update-desktop-database ~/.local/share/applications/
```

**Install icon system-wide**:
```bash
xdg-icon-resource install --size 48 myicon.png myapp
```

### Security Context

This restriction was introduced to prevent:
- Accidental execution of malicious .desktop files
- Social engineering attacks (fake app launchers)
- Execution of untrusted downloaded files

Files must be explicitly placed in trusted locations by the user to execute.

### Workarounds for Development

**Option A: Use Shell Scripts** (Recommended)
During development, use shell scripts (`.sh`) instead of `.desktop` files for testing:
- No location restrictions
- Faster iteration
- Same functionality for launching apps
- Reserve `.desktop` files for final installation/distribution

**Option B: Configure Nautilus for Development**
For development on your local machine:
```bash
# Allow launching .desktop files from any location
dconf write /org/gnome/nautilus/preferences/executable-text-activation "'launch'"
nautilus -q  # Restart Nautilus

# Revert to default after development:
dconf reset /org/gnome/nautilus/preferences/executable-text-activation
```

**Note**: Option B is only for your development machine. End users would still need proper installation.

### Distribution Checklist

When distributing an app with .desktop launcher:

- [ ] Provide `SETUP_DESKTOP_LAUNCHER.sh` installation script
- [ ] Use absolute paths in .desktop file
- [ ] Include both .desktop and .sh launchers (flexibility)
- [ ] Document where .desktop file should be placed
- [ ] Set executable permissions in setup script
- [ ] Set trusted flag in setup script
- [ ] Update icon cache if custom icons used
- [ ] Test on fresh GNOME installation

### References

- FreeDesktop.org Desktop Entry Specification
- GNOME Security Policy (GNOME 43+)
- XDG Base Directory Specification
- Icon Theme Specification

---

**Last Updated**: October 2025
**GNOME Version**: 43+
**Tested On**: Zorin OS, Ubuntu 22.04+, Fedora 38+

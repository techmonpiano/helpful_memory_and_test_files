# TigerVNC Installation & Optimization Session

**Date**: September 23, 2025
**System**: Ubuntu 25.04 (Plucky Puffin) x86_64
**Hardware**: 16 CPU cores, 13GB RAM
**User**: user1
**Hostname**: ubuntu1-ash2-vm.tail1da69.ts.net

## Session Overview
Complete installation and optimization of TigerVNC server with maximum performance settings, including GPT-5 consultation via Tess MCP for validation and enhancement of the implementation plan.

## System Analysis (Initial State)
- **OS**: Ubuntu 25.04 (Plucky Puffin) x86_64
- **Hardware**: 16 CPU cores, 13GB RAM
- **VNC Software**: None installed initially
- **Desktop Environment**: XFCE4 already present with extensive plugins
- **Available Package**: TigerVNC 1.14.1 from Ubuntu repos

## GPT-5 Consultation Results
Used Tess MCP agent (ID 3176) to validate the installation plan. GPT-5 **agreed with the overall approach** and provided key refinements:

### GPT-5 Approved Plan Elements:
- TigerVNC + XFCE4 combination
- Performance optimizations (compositing disabled, etc.)
- Tight encoding with JPEG compression
- 24-bit color depth
- Systemd integration

### GPT-5 Enhanced Recommendations:
- **Specific xstartup script**: Remove `&` from `exec startxfce4`
- **XFCE optimizations**: Disable compositor, shadows, desktop icons
- **Network tuning**: TCP buffer size increases
- **Service configuration**: Remove problematic User/PAMName settings
- **Quality settings**: JPEG quality 7, compression level 3 (though not supported in this version)

## Complete Installation Process

### 1. Package Installation
```bash
# User ran manually:
sudo apt install -y tigervnc-standalone-server tigervnc-common tigervnc-tools
```

### 2. VNC Configuration Directory & Script
**Created**: `~/.vnc/xstartup`
```bash
#!/bin/sh
unset SESSION_MANAGER
unset DBUS_SESSION_BUS_ADDRESS
exec startxfce4
```
**Permission**: `chmod +x ~/.vnc/xstartup`

### 3. VNC Password Setup
User configured manually using `vncpasswd`

### 4. XFCE4 Performance Optimizations
**Modified**: `~/.config/xfce4/xfconf/xfce-perchannel-xml/xfwm4.xml`
- `use_compositing`: `true` → `false`
- `cycle_preview`: `true` → `false`
- `show_dock_shadow`: `true` → `false`
- `show_frame_shadow`: `true` → `false`

**Modified**: `~/.config/xfce4/xfconf/xfce-perchannel-xml/xfce4-desktop.xml`
- Disabled desktop icons (show-home, show-filesystem, show-removable, show-trash: `false`)
- Set solid dark gray background (rgba: 0.2, 0.2, 0.2, 1.0)
- Disabled desktop menu

## Systemd Service Configuration

### Failed Attempts & Troubleshooting

#### Attempt 1: Template Service (FAILED)
**File**: `~/.config/systemd/user/vncserver@:1.service`
**Issue**: Systemd interpreted `:%i` as `::1` instead of `:1`
**Error**: `vncserver: Option ::1: Unrecognized!`

#### Attempt 2: Fixed Template Service (FAILED)
**Issue**: GROUP permission errors
**Error**: `Failed to determine supplementary groups: Operation not permitted`
**Root Cause**: `User=%u` and `PAMName=login` settings incompatible with user services

#### Successful Solution: Simple Service File
**File**: `~/.config/systemd/user/vncserver.service`
```ini
[Unit]
Description=TigerVNC server
After=syslog.target network.target

[Service]
Type=forking
ExecStart=/usr/bin/vncserver :1 -geometry 1920x1080 -depth 24 -dpi 96 -localhost no
ExecStop=/usr/bin/vncserver -kill :1
PIDFile=/home/user1/.vnc/ubuntu1-ash2-vm.tail1da69.ts.net:1.pid
Restart=on-failure
RestartSec=5

[Install]
WantedBy=default.target
```

### VNC Server Parameter Evolution

#### Initial Attempt (FAILED)
```bash
vncserver :1 -geometry 1920x1080 -depth 24 -localhost -dpi 96 -quality 7 -compresslevel 3
```
**Issue**: `Unrecognized option: -quality` in TigerVNC 1.14.1

#### Working Configuration
```bash
vncserver :1 -geometry 1920x1080 -depth 24 -dpi 96 -localhost no
```

#### Early Session Exit Issue (SOLVED)
**Problem**: "Session startup via xstartup cleanly exited too early (< 3 seconds)"
**Root Cause**: `exec startxfce4 &` (with ampersand)
**Solution**: Changed to `exec startxfce4` (removed ampersand)

## Network Configuration Changes

### Initial Setup: Localhost Only
- **Security**: `-localhost` flag enabled
- **Access**: Only via SSH tunnel
- **Listening**: 127.0.0.1:5901, ::1:5901

### Final Setup: External Access
- **Security**: `-localhost no` flag
- **Access**: Direct connection allowed
- **Listening**: 0.0.0.0:5901, :::5901

## Auto-Start Configuration

### Initial Problem
**Issue**: VNC service only started when user logged in (SSH session)
**Root Cause**: `Linger=no` for user1
**Detection**: `loginctl show-user user1` revealed lingering disabled

### Solution Applied
```bash
# User ran manually:
sudo loginctl enable-linger user1
```
**Result**: Service now starts at boot without requiring user login
**Verification**: `/var/lib/systemd/linger/user1` file exists

## Network Manager Assessment
- **Status**: Healthy, using netplan.io as configuration layer
- **Renderer**: NetworkManager
- **Primary Interface**: eth0 via DHCP
- **Additional**: Tailscale VPN active
- **Wi-Fi**: Hardware missing (normal for VM/server)
- **Configuration Files**:
  - `/etc/netplan/01-network-manager-all.yaml`: Standard NM delegation
  - `/etc/netplan/50-cloud-init.yaml`: Standard DHCP config

## System Performance Recommendations (Not Applied - Requires Sudo)
```bash
# Network optimizations for /etc/sysctl.conf
net.core.rmem_max=8388608
net.core.wmem_max=8388608
```

## Final Working Configuration

### VNC Server Status
- **Display**: :1
- **Port**: 5901
- **Security**: VncAuth + TLSVnc
- **Access**: External (0.0.0.0:5901)
- **Auto-start**: Enabled (lingering)
- **Resolution**: 1920x1080 @ 96 DPI
- **Color Depth**: 24-bit
- **Memory Usage**: ~195-334MB

### Service Management Commands
```bash
# Status
systemctl --user status vncserver.service

# Control
systemctl --user start/stop/restart vncserver.service

# Manual operation
vncserver :1 -geometry 1920x1080 -depth 24 -dpi 96 -localhost no
vncserver -kill :1
vncserver -list
```

### Connection Methods
- **Direct**: `ubuntu1-ash2-vm.tail1da69.ts.net:5901`
- **VNC Display**: `ubuntu1-ash2-vm.tail1da69.ts.net:1`
- **SSH Tunnel**: `ssh -L 5901:localhost:5901 user1@server` (if localhost-only)

## Key Troubleshooting Insights

### TigerVNC 1.14.1 Specific Issues
1. **Quality/compression parameters not supported** in command line
2. **Default security** includes both VncAuth and TLSVnc
3. **Localhost binding** requires explicit `-localhost no` to disable
4. **PID file location** includes full hostname in filename

### Systemd User Service Gotchas
1. **Template services** can have parameter substitution issues
2. **User/PAMName settings** cause permission errors in user services
3. **Lingering requirement** for boot-time startup
4. **Dependencies** on network.target important for VNC

### XFCE4 Optimization Keys
1. **Compositing must be disabled** for VNC performance
2. **Desktop icons/shadows** create unnecessary overhead
3. **Configuration location**: `~/.config/xfce4/xfconf/xfce-perchannel-xml/`
4. **Solid backgrounds** perform better than images

## Session Validation & Testing
- ✅ Service auto-starts after reboot
- ✅ VNC accessible externally on port 5901
- ✅ XFCE4 desktop fully functional
- ✅ Performance optimizations applied
- ✅ Lingering enabled for boot-time startup
- ✅ No errors in service logs

## Files Created/Modified
- `~/.vnc/xstartup` (created)
- `~/.config/systemd/user/vncserver.service` (created)
- `~/.config/xfce4/xfconf/xfce-perchannel-xml/xfwm4.xml` (modified)
- `~/.config/xfce4/xfconf/xfce-perchannel-xml/xfce4-desktop.xml` (modified)
- `/var/lib/systemd/linger/user1` (created via loginctl)

## Recommendations for Future Sessions
1. **Always check TigerVNC version** before using quality/compression flags
2. **Test xstartup script manually** before systemd integration
3. **Enable lingering early** if boot-time startup required
4. **Use simple service files** over templates for single-instance services
5. **Verify network listening** with netstat after configuration changes
6. **Consider security implications** when enabling external access

## VNC Display Environment Issues & Solutions

### Common Problem: GUI Applications Failing in VNC
**Issue**: Applications like Vivaldi browser work from VM console but fail when launched through VNC session.

### Root Cause Analysis
**Display Environment Variable Mismatch:**
- **VM Console**: Uses physical display (`:0` or direct framebuffer)
- **VNC Session**: Uses virtual display (`:1`)

When launching GUI applications in VNC context, the system may default to display `:0` which doesn't exist in the VNC environment.

### VNC Environment Discovery
```bash
ps aux | grep vnc
```

**Typical Output:**
```bash
user1  3498  /usr/bin/perl /usr/bin/vncserver :1 -geometry 1920x1080 -depth 24 -dpi 96 -localhost no
user1  3499  /usr/bin/Xtigervnc :1 -localhost=0 -desktop ubuntu1-ash2-vm.tail1da69.ts.net:1 (user1) -rfbport 5901
```

**Key Finding:** VNC server running on display `:1`

### Solution Methods

#### Immediate Fix for Individual Applications
```bash
DISPLAY=:1 vivaldi-stable --no-sandbox --disable-gpu
```

**Browser-Specific Flags:**
- `--no-sandbox`: Disables Chrome sandboxing for VNC compatibility
- `--disable-gpu`: Prevents GPU acceleration conflicts in VNC environment

#### Permanent System-Wide Fix
**Modify**: `~/.bashrc`
**Add to end of file:**
```bash
# Set DISPLAY for VNC session
export DISPLAY=:1
```

**Activation:**
```bash
source ~/.bashrc
# OR restart terminal session
```

#### Benefits of Permanent Fix
1. **Automatic Resolution**: GUI applications launch without manual DISPLAY specification
2. **User Experience**: Seamless operation in VNC environment
3. **Consistency**: All applications use correct display by default

### VNC vs Console Environment Comparison

| Aspect | VM Console | VNC Session |
|--------|------------|-------------|
| Display Variable | `:0` or direct | `:1` (or higher) |
| GPU Access | Full hardware | Software/limited |
| Performance | Native | Network dependent |
| Remote Access | No | Yes |
| Multi-session | No | Yes (multiple displays) |

### Troubleshooting Commands
```bash
# Check current display
echo $DISPLAY

# List VNC processes
ps aux | grep vnc

# Test VNC display
DISPLAY=:1 xrandr

# Launch app with specific display
DISPLAY=:1 application-name

# Check VNC server status
vncserver -list
```

### Common GUI Application Launch Patterns
```bash
# Web browsers
DISPLAY=:1 firefox --no-sandbox
DISPLAY=:1 chromium-browser --no-sandbox --disable-gpu
DISPLAY=:1 vivaldi-stable --no-sandbox --disable-gpu

# Development tools
DISPLAY=:1 code
DISPLAY=:1 gedit

# System tools
DISPLAY=:1 nautilus
DISPLAY=:1 gnome-terminal
```

**Total Session Duration**: ~30 minutes
**Final Status**: Complete success with optimized performance configuration and VNC display troubleshooting solutions
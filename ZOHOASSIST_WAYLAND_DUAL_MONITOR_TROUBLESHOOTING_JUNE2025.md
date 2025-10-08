# ZohoAssist Wayland Dual Monitor Troubleshooting Session
## Date: June 20, 2025

### Original Problem Report
User encountered errors when running `chmod +x Connect && ./Connect` for ZohoAssist:
```
cp: cannot stat 'C*'$'\234'':'$'\256\177''/zohojoin.desktop': No such file or directory

(ZohoAssist:105365): Gdk-CRITICAL **: 09:46:22.980: gdk_monitor_get_geometry: assertion 'GDK_IS_MONITOR (monitor)' failed
Gdk-Message: 09:47:21.748: Window 0x5bc43cdc0a30 is a temporary window without parent, application will not be able to position it on screen.

(ZohoAssist:105365): Gdk-CRITICAL **: 09:47:21.759: gdk_wayland_window_handle_configure_popup: assertion 'impl->transient_for' failed
```

### System Configuration
- **OS**: Linux (Zorin/Ubuntu-based)
- **Display Server**: Wayland
- **Monitor Setup**: Dual monitor (ViewSonic + Lenovo)
- **ZohoAssist**: Remote desktop session

### Key Findings from Research

#### 1. ZohoAssist Wayland Compatibility Status
- ✅ **Working**: User confirmed system prompts for display sharing permissions
- ✅ **Normal Behavior**: Permission prompts indicate proper Wayland security integration
- ⚠️ **Limited**: Dual monitor spanning acknowledged as "in pipeline" by Zoho

#### 2. Error Analysis
**Connect Script Error**: `cp: cannot stat 'C*'$'\234'':'$'\256\177''/zohojoin.desktop'`
- Corrupted filename with non-printable characters
- Likely installation/dependency issue, not functional blocker

**Gdk-CRITICAL Errors**: `gdk_monitor_get_geometry` warnings
- Known GTK/Wayland compatibility issue (Bug #793618)
- Common with dual monitor setups on Wayland
- Non-fatal warnings, not functional errors

#### 3. Monitor Selection Behavior
**Observed Pattern**:
- ViewSonic: Selectable individually ✅
- Lenovo: Only selectable after choosing ViewSonic ❌

**Root Cause**: Wayland compositor-determined monitor hierarchy
- Wayland lacks X11's flexible "primary monitor" concept
- Display enumeration order controlled by compositor
- ZohoAssist follows system hierarchy rather than offering free selection

### Technical Background from Research

#### GTK/Wayland Known Issues
- **Bug #793618**: "gdk_monitor_get_geometry should take WL_OUTPUT_TRANSFORM_* into account"
- Users report gdk_monitor geometry functions returning 0 values on Wayland
- Fundamental compatibility issues between X11-based applications and Wayland

#### Wayland Multi-Monitor Limitations
From Linux documentation:
- "Unlike changing the primary monitor in X, Wayland does not have the concept of a primary display"
- "Primary monitor must be implemented by the compositor"
- "Methods and tools used to set the primary display differ between Wayland implementations"

#### ZohoAssist Multi-Monitor Status
- Recent Wayland compatibility added
- "Allows you to view multiple monitors on a single screen only"
- "Spanning across multiple monitors is a part of our pipeline"

### Potential Solutions for Monitor Selection Issue

#### 1. System-Level Changes
- **Set Lenovo as Primary**: Change primary display in desktop environment settings
- **Tools by DE**:
  - KDE: `kscreen-doctor` command
  - GNOME: `gnome-randr` tool

#### 2. Physical Workarounds
- **Swap Connections**: Switch which monitor connects to which graphics port
- **Connection Order**: Try different cable connection sequence

#### 3. Compositor-Specific Tools
Depending on desktop environment:
- **KDE/KWin**: `kscreen-doctor --output <display> --primary`
- **GNOME/Mutter**: `gnome-randr --primary <display>`

#### 4. Alternative Approaches
- **Single Monitor Mode**: Use ViewSonic alone for stable connection
- **Both Monitors**: Accept ViewSonic+Lenovo selection when Lenovo access needed

### Search Results Summary

#### ZohoAssist Research
- "Zoho Assist makes remote support easy on Linux Wayland devices"
- Multi-monitor support exists but with limitations
- Black screen errors and connection failures reported by some users
- Wayland compatibility recently improved but still developing

#### Linux Wayland Multi-Monitor Issues
- "Secondary monitor doesn't work with Wayland Session"
- "External monitor not detected under Wayland"
- Monitor order inconsistencies between sessions
- NVIDIA-specific complications in dual GPU setups

### Current Status Assessment
- **Functional**: ZohoAssist works with Wayland (permission prompts confirm)
- **Usable**: ViewSonic display accessible for remote sessions
- **Limited**: Lenovo display requires both monitors selected
- **Stable**: Errors are warnings, not blockers

### Recommended Next Steps

#### Immediate Actions
1. **Test Current Functionality**: Verify remote session works with ViewSonic
2. **Document Behavior**: Note which monitor provides best remote experience
3. **Monitor Updates**: Check ZohoAssist changelogs for dual monitor improvements

#### Future Troubleshooting
1. **Primary Display Change**: Test setting Lenovo as primary display
2. **Connection Swap**: Try different physical port connections
3. **Compositor Tools**: Investigate desktop-specific display management
4. **ZohoAssist Updates**: Monitor for improved multi-monitor support

### Additional Resources
- GTK Bug #793618: gdk_monitor_get_geometry Wayland issues
- ZohoAssist Help: Multi-monitor navigation documentation
- Linux Wayland Display Management: Compositor-specific tools and commands

---
**Session Notes**: User successfully proceeded with dual monitor selection despite warnings. Core functionality appears intact with Wayland security integration working properly. Monitor selection hierarchy follows Wayland compositor behavior rather than application-level choice.
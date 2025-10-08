# Claude Desktop Multiple Instances Implementation - Session Memory

**Date:** September 5, 2025  
**System:** Ubuntu/Debian (Zorin OS 17.3)  
**Claude Desktop Version:** 0.9.2  

## Session Overview

Successfully implemented multiple simultaneous Claude Desktop instances on Ubuntu system using Electron's `--user-data-dir` and `--no-single-instance-lock` flags. This enables running separate Claude sessions with independent configurations and MCP server setups.

## Initial Problem

User wanted to run multiple Claude Desktop instances simultaneously on Debian/Ubuntu, similar to having multiple browser profiles. The standard Claude Desktop installation prevents multiple instances due to Electron's single-instance lock mechanism.

## Research Phase Findings

### Web-based Alternatives Investigation
- **Finding:** No direct web-based Claude Desktop equivalent with MCP support exists
- **Official Claude:** Web interface at claude.ai lacks MCP tool integration
- **Open Source Alternatives:** Options like Open WebUI, AnythingLLM exist but with limited MCP support
- **Conclusion:** Desktop application remains the only viable option for full MCP functionality

### Multiple Instance Feasibility
- **GitHub Projects Found:**
  - `claude-desktop-multi-instance` (macOS-focused but shows concept viability)
  - Various Linux installation projects for Claude Desktop
- **Technical Basis:** Electron applications can support multiple instances with proper configuration

## Implementation Process

### Phase 1: System Analysis
**Current Setup Discovered:**
- Claude Desktop installed at: `/usr/bin/claude-desktop`
- Configuration symlink: `~/.config/Claude -> /home/user1/shawndev1/claudia/claudia/.config/Claude`
- Active MCP configuration in: `/home/user1/.config/chromium/claude_desktop_config.json`
- Running processes using standard Electron with Wayland support

### Phase 2: Basic Testing
**Initial Attempts:**
```bash
# First attempt - basic user-data-dir
claude-desktop --user-data-dir=~/.config/Claude-Instance2 &
```
**Result:** ✅ **SUCCESS** - Second instance launched successfully

**Key Discovery:** Basic `--user-data-dir` separation worked immediately, indicating the system supported multiple instances.

### Phase 3: Critical Issue - Single Instance Lock
**Problem Encountered:** When trying to launch third instance and creating launcher scripts, instances would timeout or fail to launch properly.

**Root Cause Identified:** Electron's default single-instance lock mechanism prevents multiple instances even with different user data directories.

**Failed Attempts:**
```bash
# Without single-instance lock flag - would hang/timeout
claude-desktop --user-data-dir="$HOME/.config/Claude-Main" "$@"
```

**Successful Solution:**
```bash
# Added --no-single-instance-lock flag
claude-desktop --user-data-dir="$HOME/.config/Claude-Main" --no-single-instance-lock "$@"
```

**Result:** ✅ **SUCCESS** - All three instances launched simultaneously

### Phase 4: Launcher Scripts Creation
**Created Scripts:**
- `/home/user1/bin/claude-main` - Main instance launcher
- `/home/user1/bin/claude-work` - Work instance launcher  
- `/home/user1/bin/claude-personal` - Personal instance launcher

**Key Configuration:**
```bash
#!/bin/bash
echo "Starting Claude Desktop - [Instance Name]..."
exec claude-desktop --user-data-dir="$HOME/.config/Claude-[Instance]" --no-single-instance-lock "$@"
```

### Phase 5: MCP Configuration Separation
**Strategy:** Created separate MCP configurations for different use cases:

**Main Instance** (`~/.config/Claude-Main/claude_desktop_config.json`):
- Full MCP suite: desktop-commander, context7-mcp, tess
- General purpose configuration

**Work Instance** (`~/.config/Claude-Work/claude_desktop_config.json`):
- Enhanced with Playwright for browser automation
- All main tools plus additional work-focused tools

**Personal Instance** (`~/.config/Claude-Personal/claude_desktop_config.json`):
- Minimal setup: desktop-commander, context7-mcp only
- Lighter configuration for experiments

### Phase 6: Desktop Integration
**Created Desktop Entries:**
- `claude-main.desktop`
- `claude-work.desktop`  
- `claude-personal.desktop`

**Features:**
- Unique names and descriptions
- Proper categorization (Office;Development)
- Icon integration using existing Claude Desktop icon

## Technical Details

### Directory Structure Created
```
~/.config/
├── Claude-Main/
│   └── claude_desktop_config.json
├── Claude-Work/
│   └── claude_desktop_config.json
├── Claude-Personal/
│   └── claude_desktop_config.json

~/bin/
├── claude-main*
├── claude-work*
└── claude-personal*

~/.local/share/applications/
├── claude-main.desktop
├── claude-work.desktop
└── claude-personal.desktop
```

### Critical Flags Required
- `--user-data-dir=[PATH]` - Separates data storage
- `--no-single-instance-lock` - **ESSENTIAL** - Allows multiple instances

### Process Verification
**Testing Command:**
```bash
ps aux | grep "claude-desktop" | grep -E "(Main|Work|Personal)" | wc -l
```
**Result:** 10 processes (indicating all 3 instances running with child processes)

## Troubleshooting Notes

### What Didn't Work
1. **Initial assumption:** Thought multiple instances would work immediately without flags
2. **Missing flag:** First launcher scripts without `--no-single-instance-lock` caused timeouts
3. **PATH issues:** Initially needed to ensure `~/bin` was in PATH for launcher scripts

### What Worked
1. **Electron flags:** `--no-single-instance-lock` was the key enabler
2. **User data separation:** `--user-data-dir` successfully isolated configurations
3. **MCP configuration:** Each instance properly loaded its own MCP server configuration
4. **Desktop integration:** Standard `.desktop` files worked perfectly

## Usage Instructions

### Command Line Launch
```bash
# Launch instances
claude-main      # Main instance with full MCP
claude-work      # Work instance with Playwright
claude-personal  # Personal instance minimal setup
```

### Desktop Launch
- Open applications menu
- Look for "Claude Desktop (Main/Work/Personal)"
- Click to launch specific instance

### Verification
```bash
# Check running instances
ps aux | grep claude-desktop | grep -E "(Main|Work|Personal)"

# Check MCP configurations
ls ~/.config/Claude-*/claude_desktop_config.json
```

## Benefits Achieved

1. **Separate Contexts:** Each instance maintains independent chat history
2. **Custom MCP Setups:** Different tool configurations per use case
3. **Project Isolation:** Work and personal projects don't mix
4. **Easy Access:** Desktop shortcuts and command-line launchers
5. **Resource Management:** Can run only needed instances

## Potential Enhancements

1. **Custom Icons:** Create distinct icons for each instance
2. **Startup Scripts:** Auto-launch specific instances on system boot
3. **Window Management:** Configure different window positions/sizes
4. **Additional Profiles:** Easy to create more specialized instances
5. **Backup Scripts:** Automate configuration backups

## Technical Notes for Future Reference

- **Electron Version:** 35.1.5 (from process info)
- **Platform:** Wayland support enabled
- **Configuration Format:** Standard Claude Desktop JSON format
- **MCP Servers:** All existing MCP tools work independently per instance

## Key Learnings

1. **Electron Behavior:** Single-instance lock is default, must be explicitly disabled
2. **User Data Isolation:** Complete separation includes crash handlers, network services, etc.
3. **MCP Independence:** Each instance loads MCP servers independently from its config
4. **Desktop Integration:** Standard Linux desktop entry format works seamlessly

This implementation provides a robust multi-instance Claude Desktop setup that can be easily extended or modified for different use cases.
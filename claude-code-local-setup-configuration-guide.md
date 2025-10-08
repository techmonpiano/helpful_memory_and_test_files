# Claude Code Local Setup & Configuration Guide

## Installation Summary

### Installation Type
- **Type**: Local Installation
- **Location**: `/home/user1/.claude/local/claude`
- **Installation Method**: `npx @anthropic-ai/claude-code@latest migrate-installer`
- **Advantage**: No global permissions needed, user-specific installation

## Configuration Files & Their Purposes

### 1. Claude Code Main Configuration
**File**: `/home/user1/.claude/settings.json`

**Purpose**: 
- Main user settings that can be shared/synced across machines
- Global permissions and tool configurations
- Standard directory access that would be consistent across setups

**Current Configuration**:
```json
{
  "permissions": {
    "additionalDirectories": [
      "/home/user1/.claude/projects"
    ],
    "allow": [
      "Docker", "Docker-compose", "Podman",
      "Git", "Git-add", "Git-commit", "Git-push", "Git-pull", 
      "Git-clone", "Git-fetch", "Git-checkout", "Git-branch", 
      "Git-merge", "Git-status", "Git-log", "Git-diff", "Git-show", 
      "Git-tag", "Git-stash", "Git-remote", "Git-config", "Git-init", 
      "Git-rebase", "Git-cherry-pick", "Git-revert", "Gh",
      "Npm", "Node", "Npx", "Yarn", "Pnpm",
      "Python", "Python3", "Pip", "Pip3", "Poetry",
      "Grep", "Rg", "Ripgrep", "Egrep", "Fgrep",
      "Find", "Fd", "Locate", "Which", "Whereis",
      "Cat", "Less", "More", "Head", "Tail", "Tee",
      "Ls", "Ll", "La", "Tree", "Du", "Df", "Stat",
      "Echo", "Printf", "Wc", "Sort", "Uniq", "Cut", "Awk", "Sed",
      "Curl", "Wget", "Ping", "Nslookup", "Dig",
      "Tar", "Gzip", "Gunzip", "Zip", "Unzip",
      "Chmod", "Chown", "Cp", "Mv", "Rm", "Mkdir", "Rmdir",
      "Ps", "Top", "Htop", "Kill", "Killall", "Jobs", "Nohup",
      "Make", "Cmake", "Gcc", "G++", "Clang",
      "Ssh", "Scp", "Rsync", "Tmux", "Screen",
      "Jq", "Yq", "Xmllint", "Base64", "Hexdump",
      "Timeout", "Sleep", "Date", "Uptime", "Whoami", "Id",
      "Systemctl", "Service", "Crontab",
      "Code", "Vim", "Nano", "Emacs", "Claude",
      // MCP Server Tools
      "mcp__desktop-commander__*",
      "mcp__context7__*",
      "mcp__tess__*",
      "mcp__playwright__*"
    ]
  },
  "model": "sonnet"
}
```

### 2. Claude Code Local Configuration
**File**: `/home/user1/.claude/settings.local.json`

**Purpose**:
- Machine-specific settings that shouldn't be shared
- Personal API keys, local paths unique to this machine
- Experimental settings for testing

**Current Configuration**:
```json
{
  "permissions": {
    "allow": [
      "Bash(gh repo view:*)",
      "Bash(chmod:*)",
      "Bash(python3:*)",
      "Bash(git add:*)",
      "Bash(git commit:*)",
      "Bash(git push:*)"
    ]
  },
  "enableAllProjectMcpServers": false
}
```

**Recommended Addition** (machine-specific directories):
```json
{
  "permissions": {
    "additionalDirectories": [
      "/home/user1/shawndev1"
    ],
    "allow": [
      "Bash(gh repo view:*)",
      "Bash(chmod:*)",
      "Bash(python3:*)",
      "Bash(git add:*)",
      "Bash(git commit:*)",
      "Bash(git push:*)"
    ]
  },
  "enableAllProjectMcpServers": false
}
```

## MCP Server Configuration

### Desktop Commander MCP Server
**Management**: Via MCP tools (`mcp__desktop-commander__get_config` / `mcp__desktop-commander__set_config_value`)

**Key Setting**: `allowedDirectories`

**Current Allowed Directories**:
- `/tmp` - Temporary files
- `/home/user1/shawndev1` - Primary development directory (recursive)
- `/home/user1/shawndev1/handy-expander` - Specific project
- `/home/user1/shawndev1/kilo-terminal` - Specific project  
- `/home/user1/shawndev1/ASAPWebNew` - Specific project
- `/home/user1/.config/kilo-terminal` - Configuration directory
- `/home/user1/.claude/projects` - Claude projects directory
- `/home/user1/.claude` - Claude configuration access

## Directory Structure & Usage

```
/home/user1/
├── .claude/                          # Claude Code installation & config
│   ├── settings.json                # Main configuration (shareable)
│   ├── settings.local.json          # Local-only configuration
│   ├── local/                       # Local installation directory
│   │   └── claude                   # Claude Code executable
│   ├── projects/                    # Dedicated Claude projects folder
│   ├── plugins/                     # Claude plugins
│   ├── shell-snapshots/            # Shell command history
│   ├── statsig/                     # Analytics data
│   └── todos/                       # Todo management
└── shawndev1/                       # Primary development workspace
    ├── helpful_memory_and_test_files/ # Reference files (like this one)
    ├── handy-expander/              # Text expander project
    ├── kilo-terminal/               # Terminal project
    ├── ASAPWebNew/                  # Web project
    └── [other projects...]          # Additional development projects
```

## Project Directory Recommendations

### Option 1: Dedicated Claude Projects (Recommended for organization)
**Location**: `/home/user1/.claude/projects/`
- **Pros**: Clean separation, easy to identify Claude-generated projects
- **Cons**: Separated from other development work

### Option 2: Integrated with Main Development (Recommended for workflow)
**Location**: `/home/user1/shawndev1/[project-name]`
- **Pros**: All development work in one place, easier context switching
- **Cons**: May clutter main development directory

### Hybrid Approach (Best of both worlds)
- Use `/home/user1/.claude/projects/` for experimental/learning projects
- Use `/home/user1/shawndev1/` for serious development projects
- Both locations have full access from Claude Code and MCP tools

## Configuration File Decision Matrix

| Setting Type | settings.json | settings.local.json |
|--------------|---------------|-------------------|
| Standard directories (like ~/.claude/projects) | ✅ Yes | ❌ No |
| Machine-specific paths (like /home/user1/shawndev1) | ❌ No | ✅ Yes |
| Common tools and commands | ✅ Yes | ❌ No |
| Personal API keys | ❌ No | ✅ Yes |
| Experimental settings | ❌ No | ✅ Yes |
| Team-shared configurations | ✅ Yes | ❌ No |

## Key Insights

1. **"Local Installation" vs "Local Settings"**: 
   - Local installation means Claude is installed per-user (vs system-wide)
   - Local settings means machine-specific configs that shouldn't be shared

2. **Dual Directory Access Control**:
   - Claude Code has `additionalDirectories` for its own file operations
   - Desktop Commander MCP has `allowedDirectories` for MCP tool operations
   - Both should include your project directories for full functionality

3. **Configuration Hierarchy**:
   - Settings are layered: global → user → project → local
   - Local settings override global settings
   - MCP server configs are separate from Claude Code configs

## Maintenance Commands

### View Current Claude Code Config
```bash
cat ~/.claude/settings.json
cat ~/.claude/settings.local.json
```

### View Desktop Commander MCP Config
Use Claude Code MCP tools:
```
mcp__desktop-commander__get_config
```

### Modify Desktop Commander Allowed Directories
```
mcp__desktop-commander__set_config_value
Key: allowedDirectories
Value: ["/path/to/directory"]
```

---
*Created: 2025-01-09*
*Purpose: Comprehensive reference for Claude Code local installation and configuration setup*
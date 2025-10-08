# MCP Server Connection Troubleshooting Guide

Date: 2025-07-11

## Issue Summary
Two MCP servers were failing to connect in Claude Code:
1. **Tess MCP Server** - Not appearing in MCP list (completely missing)
2. **Facebook Marketplace MCP Server** - Appearing in list but failing to start

## Root Causes

### 1. Tess MCP Server
- **Issue**: Server was enabled in `settings.local.json` but not properly configured in Claude Code's MCP system
- **Cause**: The server needed to be added with the proper API key configuration

### 2. Facebook Marketplace MCP Server
- **Issue**: Server was configured but failing on startup
- **Cause**: Requires Facebook authentication - expects session cookies at `~/.fb-marketplace-mcp/session.json`

## Solutions Applied

### Fixed Tess MCP Server
```bash
# Add Tess MCP server with API key
claude mcp add tess -s user -e "TESS_API_KEY=70709|bud2zaVgV3bAizp2MY96iD0TW2PKCwxFMLQKwv3a099e04ff" -- npx -y mcp-tess
```

Note: The pipe character in the API key causes display issues in `claude mcp get tess`, but functionality is not affected.

### Facebook Marketplace MCP Server Options

#### Option 1: Authenticate (if you need FB Marketplace functionality)
```bash
cd /home/user1/shawndev1/mcp-claudecode-quick-scripts/fb-marketplace-mcp-server
node setup.js
```
This will:
- Open a browser window
- Allow you to log into Facebook
- Save session cookies for future use

#### Option 2: Remove (if not needed)
```bash
claude mcp remove fb-marketplace -s user
```

## Verification Commands

Check all configured MCP servers:
```bash
claude mcp list
```

Check specific server configuration:
```bash
claude mcp get <server-name>
```

List available MCP tools in Claude Code:
```bash
# In Claude Code, check if tools are available
ListMcpResourcesTool
```

## Key Files and Locations

- **Claude Code settings**: `/home/user1/shawndev1/.claude/settings.local.json`
- **Facebook session cookies**: `~/.fb-marketplace-mcp/session.json`
- **Tess MCP setup script**: `/home/user1/shawndev1/mcp-claudecode-quick-scripts/add-tess-mcp.sh`
- **FB Marketplace server**: `/home/user1/shawndev1/mcp-claudecode-quick-scripts/fb-marketplace-mcp-server/`

## Working MCP Server List
After fixes, these servers should be configured:
- `desktop-commander`: npx -y @wonderwhy-er/desktop-commander@latest
- `context7`: npx -y @upstash/context7-mcp
- `tess`: npx -y mcp-tess (with API key)
- `fb-marketplace`: node /home/user1/shawndev1/mcp-claudecode-quick-scripts/fb-marketplace-mcp-server/index.js (requires auth)

## Troubleshooting Tips

1. **MCP Server Not Appearing**: Usually means it wasn't added to Claude Code properly
2. **MCP Server Appearing but Failing**: Usually means missing dependencies or authentication
3. **Environment Variables**: Use `-e "KEY=value"` format when adding servers
4. **Special Characters**: Pipe characters (|) in API keys may cause display issues but not functional problems
5. **Dependencies**: Always run `npm install` in the server directory before use

## Common MCP Commands

```bash
# Add a new MCP server
claude mcp add <name> -s user -e "ENV_VAR=value" -- <command> <args>

# Remove an MCP server
claude mcp remove <name> -s user

# List all servers
claude mcp list

# Get server details
claude mcp get <name>
```

## Notes
- The Facebook Marketplace MCP requires actual Facebook authentication due to anti-scraping measures
- Tess MCP requires a valid API key in the format "70709|<key>"
- All MCP servers run as subprocess when Claude Code starts
- Failed MCP servers don't prevent Claude Code from running but their tools won't be available
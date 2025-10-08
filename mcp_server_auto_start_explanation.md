# MCP Server Auto-Start Behavior

## Key Understanding: MCP Servers Are Auto-Started by Clients

**✅ CRITICAL INSIGHT**: MCP servers do NOT need to be manually started. The MCP client (like Claude Code) automatically manages the server lifecycle.

## How MCP Auto-Start Works

### 1. Client-Managed Lifecycle
- **Client auto-launches**: When Claude Code needs an MCP server, it runs the configured command
- **Server starts automatically**: The MCP server initializes and connects via stdio
- **Client communicates**: Requests are sent to the server through stdin/stdout
- **Server auto-terminates**: When the client is done, the server shuts down automatically

### 2. Configuration Structure
```json
{
  "playwright": {
    "disabled": false,
    "timeout": 120,
    "type": "stdio",           // ← Key: stdio communication type
    "command": "npx",
    "args": ["-y", "@playwright/mcp"],
    "env": {}
  }
}
```

### 3. Communication Types
- **`"type": "stdio"`**: Most common - client spawns process, communicates via stdin/stdout
- **`"type": "sse"`**: Server-sent events (requires manual server start)
- **`"type": "tcp"`**: TCP socket connection (requires manual server start)

## Practical Implications

### ❌ Don't Do This (Manual Start)
```bash
# DON'T manually start MCP servers for stdio type
npx -y @playwright/mcp  # This is handled automatically
```

### ✅ Do This Instead
1. Configure the MCP server in client settings
2. Restart the MCP client (Claude Code)
3. The server will auto-start when needed

## Example: Playwright MCP Setup

### Step 1: Add to MCP Settings
```json
"playwright": {
  "disabled": false,
  "timeout": 120,
  "type": "stdio",
  "command": "npx",
  "args": ["-y", "@playwright/mcp"],
  "env": {}
}
```

### Step 2: Restart Claude Code
The Playwright MCP server will automatically:
- Start when Claude Code needs web automation
- Connect via stdio communication
- Terminate when operations are complete

## Available Playwright MCP Packages

### Official Package (Recommended)
- **`@playwright/mcp`**: Official Playwright MCP tools
- **Published**: 2025-06-11 by playwright-bot
- **Features**: Full web automation, screenshots, page interaction

### Alternative Packages
- **`@executeautomation/playwright-mcp-server`**: Community version with additional features
- **`@cloudflare/playwright-mcp`**: Cloudflare's Playwright tools
- **`@s977121/playwright-mcp-server`**: Feature-rich community version

## Common Usage Examples

### Basic Commands (Auto-executed by Client)
```bash
# Client will auto-run these as needed:
npx -y @playwright/mcp                           # Default headed mode
npx -y @playwright/mcp --headless               # Headless mode
npx -y @playwright/mcp --browser chrome         # Specific browser
npx -y @playwright/mcp --viewport-size "1920,1080"  # Custom viewport
```

## Configuration Location
- **File**: `/home/user1/.var/app/com.visualstudio.code/config/Code/User/globalStorage/kilocode.kilo-code/settings/mcp_settings.json`
- **Scope**: Claude Code MCP server configurations

## Key Takeaway
**Never manually start MCP servers with `"type": "stdio"` - the client handles everything automatically.**
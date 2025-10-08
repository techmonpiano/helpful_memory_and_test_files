# Desktop Commander MCP Integration with OpenWebUI

**Date:** July 2, 2025  
**Session Summary:** Successfully integrated Desktop Commander MCP server with OpenWebUI using mcpo proxy

## Problem Statement

User had OpenWebUI installed via pip and Desktop Commander MCP installed via npx, wanted to add Desktop Commander as a tool in OpenWebUI.

## Solution Overview

OpenWebUI supports MCP servers through their MCP-to-OpenAPI proxy server (mcpo) which converts MCP servers to standard REST APIs.

## Implementation Steps

### 1. Environment Discovery
- **OpenWebUI Location:** `/home/user1/.local/bin/open-webui`
- **Desktop Commander MCP:** Installed via `npx @wonderwhy-er/desktop-commander`
- **Python Version:** 3.10.12 (mcpo requires 3.11+, solved using `uv`)

### 2. Install and Run MCP Proxy

```bash
# Install and run mcpo proxy with Desktop Commander
uvx mcpo --port 8001 --api-key "desktop-commander-key" -- npx @wonderwhy-er/desktop-commander
```

**Server Details:**
- **URL:** http://localhost:8001
- **API Documentation:** http://localhost:8001/docs
- **API Key:** desktop-commander-key
- **Status:** Successfully running and exposing 18 Desktop Commander tools

### 3. Available Tools via OpenAPI

All Desktop Commander MCP tools are now available as REST endpoints:

```bash
# Available endpoints
[
  "/create_directory",
  "/edit_block", 
  "/execute_command",
  "/force_terminate",
  "/get_config",
  "/get_file_info",
  "/kill_process",
  "/list_directory",
  "/list_processes", 
  "/list_sessions",
  "/move_file",
  "/read_file",
  "/read_multiple_files",
  "/read_output",
  "/search_code",
  "/search_files",
  "/set_config_value",
  "/write_file"
]
```

### 4. OpenWebUI Integration

**Add Tool Server:**
1. OpenWebUI → Settings → Tools
2. Click "+" to add tool server
3. URL: `http://localhost:8001`
4. API Key: `desktop-commander-key`
5. Save

### 5. Startup Script Created

**File:** `/home/user1/shawndev1/start-desktop-commander-mcp.sh`

```bash
#!/bin/bash

# Start Desktop Commander MCP via OpenAPI proxy for OpenWebUI integration
# This script runs the MCP-to-OpenAPI proxy server that exposes Desktop Commander tools

echo "Starting Desktop Commander MCP server for OpenWebUI..."
echo "Server will be available at: http://localhost:8001"
echo "OpenAPI docs will be available at: http://localhost:8001/docs"
echo ""
echo "Add this URL to OpenWebUI Tools settings: http://localhost:8001"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Start the proxy server with API key
uvx mcpo --port 8001 --api-key "desktop-commander-key" -- npx @wonderwhy-er/desktop-commander
```

**Make executable:** `chmod +x /home/user1/shawndev1/start-desktop-commander-mcp.sh`

## Troubleshooting Issue

**Problem:** OpenWebUI shows "desktop-commander - v0.2.3" but no individual tools listed

### Root Cause Analysis

1. **OpenAPI Schema Valid:** All 18 tools properly exposed with correct operationIds
2. **Server Running Correctly:** mcpo proxy successfully converts MCP to REST API
3. **Authentication Added:** API key authentication properly configured

### Troubleshooting Steps Required

#### 1. Update Tool Server Configuration
- Remove existing Desktop Commander tool server from OpenWebUI
- Re-add with API key: `desktop-commander-key`
- URL remains: `http://localhost:8001`

#### 2. Enable Function Calling
**Critical Requirements:**
- Use model that supports function calling (GPT-4o recommended)
- Enable Native Function Calling:
  - Chat window → ⚙️ Chat Controls → Advanced Params
  - Change Function Calling: "Default" → "Native"

#### 3. Manual Tool Activation
**Look for:**
- Tool indicator icon below input box
- "+" button in message input area (bottom left)
- Click "+" to manually toggle on Desktop Commander tools

#### 4. Global vs User Tools
- If added as Global Tool: must be explicitly activated per user
- Click ➕ button → manually toggle on specific tools

## Technical Details

### MCP-to-OpenAPI Proxy Benefits
- **Standard REST APIs:** No custom protocol needed
- **Automatic Documentation:** Built-in Swagger UI at `/docs`
- **Security:** HTTPS, API keys, standard auth methods
- **Compatibility:** Works with thousands of OpenAPI tools/SDKs

### OpenAPI Schema Structure
```json
{
  "info": {
    "title": "desktop-commander",
    "description": "desktop-commander MCP Server", 
    "version": "0.2.3"
  },
  "components": {
    "securitySchemes": {
      "HTTPBearer": {
        "type": "http",
        "scheme": "bearer"
      }
    }
  }
}
```

### Server Logs (Successful Startup)
```
2025-07-02 11:34:34,878 - INFO - Starting MCPO Server...
2025-07-02 11:34:34,878 - INFO -   Name: MCP OpenAPI Proxy
2025-07-02 11:34:34,878 - INFO -   Version: 1.0
2025-07-02 11:34:34,878 - INFO -   Port: 8001
2025-07-02 11:34:34,878 - INFO -   API Key: Provided
Loading server.ts
[desktop-commander] Initialized FilteredStdioServerTransport
Configuration loaded successfully
Server connected successfully
Generating tools list...
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8001
```

## Usage Instructions

### Starting the Server
```bash
/home/user1/shawndev1/start-desktop-commander-mcp.sh
```

### Testing Tools
Once properly configured, test with:
```
"Please read the file /home/user1/test.txt using the read_file tool"
```

### Available Functionality
- **File Operations:** read, write, edit, move files
- **Directory Operations:** list, create directories  
- **Code Search:** search through code with patterns
- **System Operations:** execute commands, manage processes
- **Configuration:** get/set desktop-commander config

## Key Insights

1. **MCP Proxy Solution:** mcpo successfully bridges MCP servers to OpenAPI standard
2. **Tool Visibility Issue:** Common in OpenWebUI - tools may not auto-display
3. **Manual Activation Required:** Tools often need manual enablement via UI
4. **Function Calling Critical:** Proper model selection and native function calling essential
5. **API Key Authentication:** Improves tool server recognition and security

## References

- **OpenWebUI MCP Documentation:** https://docs.openwebui.com/openapi-servers/mcp/
- **mcpo GitHub:** https://github.com/open-webui/mcpo
- **Desktop Commander MCP:** `@wonderwhy-er/desktop-commander`
- **OpenWebUI Tools FAQ:** https://docs.openwebui.com/openapi-servers/faq/

## Next Steps

1. Update OpenWebUI tool server configuration with API key
2. Switch to GPT-4o or compatible model
3. Enable native function calling
4. Manually activate tools via + button
5. Test with simple file operation commands

## Status

✅ **MCP Proxy Server:** Running successfully on port 8001  
✅ **OpenAPI Schema:** All 18 tools properly exposed  
✅ **Authentication:** API key configured  
⏳ **OpenWebUI Integration:** Requires manual tool activation  
📝 **Documentation:** Complete reference saved to this file

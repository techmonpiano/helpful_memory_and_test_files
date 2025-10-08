# Universal LLM SSH Session Guide with Real-time Logging & GUI Integration

**Purpose**: Step-by-step guide for any LLM with MCP support to establish persistent SSH sessions with real-time logging and GUI log file viewing

**Target**: AI assistants working with remote server management (Claude Desktop, ChatGPT Desktop, Gemini Desktop, etc.)

**Features**: 
- ✅ **Universal LLM Support** - Works with any MCP-enabled AI desktop application
- ✅ **Real-time Logging** - No buffering issues with `tee` method
- ✅ **GUI Log Viewing** - Smart fallback strategy for opening log files
- ✅ **Cross-Platform** - Works on any Linux distribution with any desktop environment

---

## 🔧 Configuration Variables

Set these variables based on your target server:

```bash
# SSH Connection Parameters (CUSTOMIZE THESE)
SSH_USER="user1"                                    # SSH username
SSH_SERVER="SSH_SERVER_HOSTNAME_OR_IP_HERE"            # Server hostname/IP
SSH_PORT="PORT_HERE"                                       # SSH port (default: 22)
LOG_PREFIX="ssh_session"                           # Log file prefix
LOG_DIR="/tmp"                                     # Log directory on remote server
```

---

## 📋 Step-by-Step Session Establishment

### **Step 1: Build SSH Connection Command**
```bash
# Dynamic SSH command construction
SSH_COMMAND="ssh -T"
if [ "$SSH_PORT" != "22" ]; then
    SSH_COMMAND="$SSH_COMMAND -p $SSH_PORT"
fi
SSH_COMMAND="$SSH_COMMAND $SSH_USER@$SSH_SERVER"

# Example result: "ssh -T user1@runtipi1.tail1da69.ts.net"
# Or with custom port: "ssh -T -p 2022 user@server.com"
```

### **Step 2: LLM MCP Tools - Start Bash Process**
```javascript
// Start a bash process first for logging setup (works with any LLM MCP implementation)
start_process("bash", timeout_ms=5000)
```

**Expected Response**:
- Process ID (PID) - SAVE THIS NUMBER

### **Step 3: Setup Real-time Logging**
```javascript
// Setup real-time logging using tee (WORKS IMMEDIATELY - NO BUFFERING!)
LOG_TIMESTAMP = new Date().toISOString().replace(/[:-]/g, '').replace('T', '_').split('.')[0]
LOG_FILENAME = "/tmp/ssh_session_" + LOG_TIMESTAMP + ".log"

// Redirect output to tee for real-time logging
interact_with_process(PID, "exec > >(tee -a " + LOG_FILENAME + ") 2>&1", timeout_ms=3000)
```

**Expected Response**:
- No output (normal for exec command)

### **Step 4: Start SSH Connection**
```javascript
// Now start SSH with logging already active
SSH_COMMAND = "echo 'Starting SSH session - $(date)' && ssh -T " + SSH_USER + "@" + SSH_SERVER
if (SSH_PORT !== "22") {
    SSH_COMMAND = "echo 'Starting SSH session - $(date)' && ssh -T -p " + SSH_PORT + " " + SSH_USER + "@" + SSH_SERVER
}

interact_with_process(PID, SSH_COMMAND, timeout_ms=10000)
```

**Expected Response**:
- Timestamp message
- SSH connection established
- Linux system information

### **Step 5: Test Session and Logging**
```javascript
// Verify everything works
interact_with_process(PID, "echo 'Session ready - $(date)' && pwd && hostname", timeout_ms=5000)

// Check log file is being written locally  
// (Run this in a separate LLM MCP tool call)
list_directory("/tmp")  // Look for ssh_session_*.log files
read_file("/tmp/ssh_session_TIMESTAMP.log")  // Verify real-time content
```
---

## 🎯 Complete LLM Implementation Example

```javascript
// Variables (customize for your target)
const SSH_USER = "user1";
const SSH_SERVER = "runtipi1.tail1da69.ts.net"; 
const SSH_PORT = "22";  // or custom port like "2022"

// Step 1: Start bash process for logging setup
const result = start_process("bash", timeout_ms=5000);
const PID = result.pid;  // SAVE THE RETURNED PID!

// Step 2: Setup real-time logging with tee (NO BUFFERING ISSUES!)
const timestamp = new Date().toISOString().replace(/[:-]/g, '').replace('T', '_').split('.')[0];
const logFile = `/tmp/ssh_session_${timestamp}.log`;
interact_with_process(PID, `exec > >(tee -a ${logFile}) 2>&1`, timeout_ms=3000);

// Step 3: Start SSH connection (logging is already active)
let sshCommand = `echo 'Starting SSH session - $(date)' && ssh -T`;
if (SSH_PORT !== "22") {
    sshCommand += ` -p ${SSH_PORT}`;
}
sshCommand += ` ${SSH_USER}@${SSH_SERVER}`;
interact_with_process(PID, sshCommand, timeout_ms=10000);

// Step 4: Test session  
interact_with_process(PID, "echo 'Session ready - $(date)' && pwd && hostname", timeout_ms=5000);

// Step 5: Verify logging (separate calls)
list_directory("/tmp");  // Look for the log file
read_file(logFile);      // Check real-time content

// Ready for work!
console.log(`SSH session established with PID ${PID}`);
console.log(`Real-time logging to LOCAL file: ${logFile}`);
```

---

## 🔄 Session Management During Work

### **Execute Commands**:
```javascript
// Basic command execution
interact_with_process(PID, "your_command_here", timeout_ms=8000);

// Long-running commands
interact_with_process(PID, "long_running_command", timeout_ms=30000);

// Check command output if needed
read_process_output(PID, timeout_ms=5000);
```

### **Monitor Session Health**:
```javascript
// Check session status periodically
list_sessions();  // Look for your PID and "Blocked" status

// If session becomes unresponsive
force_terminate(PID);  // Last resort only
```
---

## 📊 Real-time Log Monitoring

### **On Remote Server** (if you have another connection):
```bash
# Watch log in real-time
tail -f /tmp/ssh_session_YYYYMMDD_HHMMSS.log

# With timestamps
tail -f /tmp/ssh_session_YYYYMMDD_HHMMSS.log | while read line; do echo "$(date '+%H:%M:%S') $line"; done

# Monitor log size
watch -n 5 'ls -lh /tmp/ssh_session_*.log'
```

### **Log File Management**:
```javascript
// Check log file on remote server
interact_with_process(PID, "ls -lh /tmp/ssh_session_*.log", timeout_ms=5000);

// View recent log entries
interact_with_process(PID, "tail -20 /tmp/ssh_session_*.log", timeout_ms=5000);

// Clean up old logs when done
interact_with_process(PID, "rm /tmp/ssh_session_*.log", timeout_ms=5000);
```

---

## 🛡️ Best Practices & Safety

### **Connection Best Practices**:
1. **Always save the PID** returned from start_process()
2. **Use appropriate timeouts** (10s for connection, 5-8s for commands)
3. **Verify connection** before proceeding with work
4. **Monitor session health** with list_sessions()
5. **Use Universal Environment Runner** for reliable GUI application launching

### **Security Considerations**:
- Use key-based authentication (no passwords in commands)
- Terminate sessions when work complete: `force_terminate(PID)`
- Avoid exposing sensitive data in log files
- Clean up log files after work completion

### **Error Handling**:
```javascript
// If connection fails
if (start_process_result.error) {
    console.log("Connection failed - check server, user, port");
    // Try again with different parameters
}

// If session becomes unresponsive
list_sessions(); // Check if PID still exists
if (session_blocked_too_long) {
    force_terminate(PID);
    // Re-establish connection
}
```
---

## 🎯 Quick Reference Template

```javascript
// TEMPLATE - Replace variables with your values
const SSH_USER = "YOUR_USERNAME";
const SSH_SERVER = "YOUR_SERVER.domain.com";
const SSH_PORT = "22";  // or custom port

// 1. Start bash process
const result = start_process("bash", timeout_ms=5000);
const PID = result.pid;  // SAVE THIS

// 2. Setup real-time logging (tee method - NO BUFFERING!)
const logFile = `/tmp/ssh_session_${Date.now()}.log`;
interact_with_process(PID, `exec > >(tee -a ${logFile}) 2>&1`, timeout_ms=3000);

// 3. Connect to SSH
const sshCmd = `echo 'Starting SSH - $(date)' && ssh -T${SSH_PORT !== "22" ? ` -p ${SSH_PORT}` : ""} ${SSH_USER}@${SSH_SERVER}`;
interact_with_process(PID, sshCmd, timeout_ms=10000);

// 4. Test and verify
interact_with_process(PID, "echo 'Ready!' && pwd && hostname", timeout_ms=5000);

// Log file location: logFile (on LOCAL machine in /tmp/)
```

## 🚀 Why This Method Works (tee vs script)

### **❌ Previous Issues with `script` command:**
- Heavy buffering caused empty log files during active sessions
- Content only appeared after session ended or long delays
- Made real-time monitoring impossible
- Unreliable for active session logging

### **✅ Advantages of `exec > >(tee -a ...)` method:**
- **Real-time logging**: Content appears immediately in log file
- **No buffering issues**: Each command output is written instantly  
- **Local logging**: Files are on your local machine, not remote server
- **Reliable**: Works consistently across different systems
- **Concurrent access**: Can read log file while session is active

### **How it works:**
1. `exec > >(tee -a logfile.log) 2>&1` redirects stdout and stderr
2. `tee` writes to both terminal and log file simultaneously  
3. No intermediate script process to cause buffering
4. Immediate file writes allow real-time monitoring

---

## 📝 Session Termination

```javascript
// When work is complete
interact_with_process(PID, "exit", timeout_ms=3000);  // Exit script logging
interact_with_process(PID, "exit", timeout_ms=3000);  // Exit SSH session
force_terminate(PID);  // Ensure cleanup

// Or force termination
force_terminate(PID);
```

---

## 🔧 Variable Configuration Examples

### **Standard SSH (port 22)**:
```javascript
const SSH_USER = "user1";
const SSH_SERVER = "myserver.example.com";
const SSH_PORT = "22";
```

### **Custom Port SSH**:
```javascript
const SSH_USER = "partsfor";
const SSH_SERVER = "ftp.partsfortechs.com";
const SSH_PORT = "2022";
```

### **Tailscale Network**:
```javascript
const SSH_USER = "user1";
const SSH_SERVER = "runtipi1.tail1da69.ts.net";
const SSH_PORT = "22";
```

---

**Key Benefits**:
- ✅ **Dynamic configuration** for any SSH server
- ✅ **Real-time logging** with NO buffering issues using `tee`
- ✅ **Local log files** stored on your machine, not remote server
- ✅ **Persistent sessions** maintained by any LLM with MCP support
- ✅ **Immediate file writes** allow concurrent log monitoring
- ✅ **GUI log viewing** with Universal Environment Runner fallback strategy
- ✅ **Error handling** and session management
- ✅ **Security best practices** with key-based auth
- ✅ **Universal LLM support** - works with Claude, ChatGPT, Gemini, etc.
- ✅ **LLM-friendly** step-by-step instructions

**Remember**: Always customize SSH_USER, SSH_SERVER, and SSH_PORT variables for your target environment!

**Log Location**: All session logs stored in `/tmp/ssh_session_TIMESTAMP.log` on YOUR LOCAL MACHINE for real-time monitoring.

---

## 📖 GUI Log File Viewing with Universal Environment Runner

### **Step 6: Open Log File with Sequential Fallback Strategy**

**IMPORTANT: Use ONLY ONE method at a time. Try fallbacks ONLY if previous method fails.**

**⚠️ BREAKTHROUGH UPDATE (2025-09-08): Enhanced xdg-open now works reliably in MCP contexts! The Universal Environment Runner now detects when xdg-open would launch Electron apps (like codium) and launches them directly with proper MCP flags instead of going through .desktop files.**

**Primary Method (Try FIRST - now enhanced and reliable):**
```javascript
// Step 6.1: Try default application first (xdg-open) - NOW RELIABLE!
// Enhanced Universal Environment Runner detects and fixes Electron app launches
console.log("Opening log file with enhanced xdg-open...");
start_process(`python3 ~/shawndev1/universal_env_runner/universal_env_runner.py xdg-open ${logFile}`, timeout_ms=10000);

// ✅ NEW: Script automatically detects if xdg-open would use codium/code
// ✅ NEW: Launches directly with MCP flags instead of going through .desktop file
// ✅ RESULT: Should open file successfully in most cases now
```

**Fallback Method 1 (ONLY if xdg-open fails - MOST RELIABLE in MCP):**
```javascript
// Step 6.2: ONLY if xdg-open didn't work, try VS Code/Codium (most reliable in MCP)
console.log("xdg-open failed, trying VS Code/Codium (most reliable in MCP)...");
start_process(`python3 ~/shawndev1/universal_env_runner/universal_env_runner.py codium ${logFile}`, timeout_ms=10000);

// Alternative if codium not available:
// start_process(`python3 ~/shawndev1/universal_env_runner/universal_env_runner.py code ${logFile}`, timeout_ms=10000);
```

**Final Fallback (ONLY if both above fail):**
```javascript
// Step 6.3: ONLY if all else fails, use gedit (always works)
console.log("All advanced methods failed, using gedit fallback...");
start_process(`python3 ~/shawndev1/universal_env_runner/universal_env_runner.py gedit ${logFile}`, timeout_ms=10000);
```

### **Programmatic Implementation (Alternative to Sequential Approach):**

**ONLY use this if you want to implement ALL fallbacks programmatically in one function:**

```javascript
// Alternative: Comprehensive function with built-in fallbacks
// NOTE: This tries multiple methods automatically - use ONLY for automation
function openLogFileWithAllFallbacks(logFile) {
    console.log("Opening log file for real-time monitoring...");
    
    // Try 1: Default application (user's preference)
    console.log("Attempting default application (xdg-open)...");
    start_process(`python3 ~/shawndev1/universal_env_runner/universal_env_runner.py xdg-open ${logFile}`, timeout_ms=10000);
    
    // Note: In practice, you should check if the above succeeded before trying these
    console.log("Also trying VS Code as backup...");
    start_process(`python3 ~/shawndev1/universal_env_runner/universal_env_runner.py code ${logFile}`, timeout_ms=10000);
    
    console.log("And gedit as final fallback...");
    start_process(`python3 ~/shawndev1/universal_env_runner/universal_env_runner.py gedit ${logFile}`, timeout_ms=10000);
}

// Use this ONLY for automated scripts where you want multiple attempts
// openLogFileWithAllFallbacks(logFile);
```

**RECOMMENDED: Use the sequential approach above for manual operation.**

### **Troubleshooting Log File Opening (BREAKTHROUGH UPDATE 2025-09-08):**

**MAJOR IMPROVEMENT: Enhanced xdg-open now works reliably!**
- **Enhancement**: Universal Environment Runner now detects when xdg-open would launch Electron apps
- **Smart Bypass**: Launches codium/code directly with MCP flags instead of through .desktop files
- **Result**: Eliminates most silent failures and makes xdg-open reliable in MCP contexts

**Typical Enhanced Behavior:**
```javascript
// When you run xdg-open, you'll see:
🎯 xdg-open would use codium.desktop, launching codium directly with MCP flags...
🚀 Executing: codium file.log --no-sandbox --disable-gpu-sandbox --enable-features=UseOzonePlatform --ozone-platform=wayland
```

**Rare Fallback Cases:**
If enhanced xdg-open still doesn't work (very rare now), use:
```javascript
start_process(`python3 ~/shawndev1/universal_env_runner/universal_env_runner.py codium ${logFile}`, timeout_ms=10000);
```

**Alternative Strategy (No Longer Recommended):**
The previous recommendation to skip xdg-open is no longer necessary due to the enhancement.

**Alternative Optimized Strategy:**
1. **Direct Editor Launch** (`codium` or `code`) - Most reliable in MCP contexts
2. **Simple Editor** (`gedit`) - Always works fallback  
3. **System Default** (`xdg-open`) - If user prefers default app
```

**Expected Results**:
- ✅ **Default App**: Log opens in user's preferred .log file handler
- ✅ **VS Code**: Advanced editor with syntax highlighting and real-time updates
- ✅ **gedit**: Simple text editor that works on any GNOME-based system
- ✅ **Real-time Updates**: All applications show file changes as commands execute
- ✅ **Universal LLM Support**: Works with Claude, ChatGPT, Gemini, any MCP-enabled AI app

---

## 🔧 Universal Environment Runner - Complete Usage Guide

### **What is Universal Environment Runner?**
The Universal Environment Runner is a Python script that solves GUI application launching issues in **any LLM with MCP support** (Claude Desktop, ChatGPT Desktop, Gemini Desktop, etc.). It automatically detects MCP environments and injects proper GUI variables.

**Location**: `~/shawndev1/universal_env_runner/universal_env_runner.py`

### **Why Do We Need It?**
- **LLM Desktop Apps** run in restricted environments without full user session
- **Missing GUI Variables** like `DISPLAY`, `WAYLAND_DISPLAY`, `XDG_CURRENT_DESKTOP` 
- **Commands Fail** - `xdg-open`, `code`, `gedit` don't work in MCP environments
- **Universal Solution** - Works with any AI desktop application automatically

### **Basic Usage Examples:**
```bash
# Open any file with default application
python3 ~/shawndev1/universal_env_runner/universal_env_runner.py xdg-open /path/to/file.log

# Open in VS Code or VS Codium with Wayland support
python3 ~/shawndev1/universal_env_runner/universal_env_runner.py code /path/to/file.py
python3 ~/shawndev1/universal_env_runner/universal_env_runner.py codium /path/to/file.py

# Open in simple text editor
python3 ~/shawndev1/universal_env_runner/universal_env_runner.py gedit /path/to/file.txt

# Open file manager at location
python3 ~/shawndev1/universal_env_runner/universal_env_runner.py nautilus /tmp
```

### **Features:**
- ✅ **Auto MCP Detection** - Automatically detects any LLM desktop environment
- ✅ **Smart Environment Injection** - Injects proper Wayland/X11 variables
- ✅ **Application-Specific Flags** - VS Code/Codium get `--no-sandbox --ozone-platform=wayland`
- ✅ **Electron App Detection** - Intelligent detection for Chromium/Electron-based apps
- ✅ **Enhanced xdg-open Support** - Improved environment injection for MCP contexts (2025-09-08)
- ✅ **Fallback Support** - Uses available tools when preferred ones aren't found
- ✅ **Cross-Platform** - Works on any Linux distribution

### **Manual MCP Detection (if auto-detection fails):**
```bash
# Force MCP mode for any LLM desktop app
MCP_SERVER=true python3 ~/shawndev1/universal_env_runner/universal_env_runner.py xdg-open file.log

# Original Desktop Commander flag
DESKTOP_COMMANDER=true python3 ~/shawndev1/universal_env_runner/universal_env_runner.py code file.py
```

### **Supported LLM Desktop Applications:**
- ✅ **Claude Desktop** - Full support with auto-detection
- ✅ **ChatGPT Desktop** - Compatible (when available) 
- ✅ **Gemini Desktop** - Compatible (when available)
- ✅ **Desktop Commander MCP** - Original target, fully supported
- ✅ **Any Electron-based AI App** - Generic detection patterns
- ✅ **Custom MCP Implementations** - Manual trigger via `MCP_SERVER=true`

### **Troubleshooting MCP Detection:**
If the script shows "MCP Context: False" but you're in an LLM environment:

```bash
# Try manual triggers:
MCP_SERVER=true python3 ~/shawndev1/universal_env_runner/universal_env_runner.py [command]
DESKTOP_COMMANDER=true python3 ~/shawndev1/universal_env_runner/universal_env_runner.py [command]

# For ChatGPT Desktop (hypothetical):
OPENAI_MCP=true python3 ~/shawndev1/universal_env_runner/universal_env_runner.py [command]

# For Gemini Desktop (hypothetical):
GOOGLE_MCP=true python3 ~/shawndev1/universal_env_runner/universal_env_runner.py [command]
```

### **Integration with SSH Sessions:**
When you establish an SSH session with logging, use Universal Environment Runner to open the log file:

```javascript
// After establishing SSH session and getting logFile path:
start_process(`python3 ~/shawndev1/universal_env_runner/universal_env_runner.py xdg-open ${logFile}`, timeout_ms=10000);
```

This ensures the log file opens in your GUI application regardless of which LLM desktop app you're using.

### **Recent Enhancements (2025-09-08):**
**Enhanced Application Support:**
- ✅ **VS Codium Support** - Now handles both `code` and `codium` with full Wayland flags
- ✅ **Expanded Electron Detection** - Automatically detects apps like `signal-desktop`, `discord`, etc.
- ✅ **Intelligent Pattern Recognition** - Apps with `-desktop`, `electron-` patterns get proper flags
- ✅ **Enhanced xdg-open in MCP** - Better environment injection for launched applications

**Improved Reliability:**
- ✅ **Consistent Flag Application** - All Electron apps get same comprehensive Wayland support
- ✅ **Future-Proof Detection** - Pattern-based recognition catches new Electron apps automatically  
- ✅ **Safe Native App Handling** - GTK/Qt apps avoid incompatible Chromium flags

---

## 🛠️ Complete SSH + GUI Integration Workflow

### **Full Example - SSH Session with GUI Log Viewing:**
```javascript
// Complete workflow combining SSH session + Universal Environment Runner
const SSH_USER = "user1";
const SSH_SERVER = "runtipi1.tail1da69.ts.net";
const SSH_PORT = "22";

// 1. Start SSH session with logging (Steps 1-5 from above)
const result = start_process("bash", timeout_ms=5000);
const PID = result.pid;

const timestamp = new Date().toISOString().replace(/[:-]/g, '').replace('T', '_').split('.')[0];
const logFile = `/tmp/ssh_session_${timestamp}.log`;

interact_with_process(PID, `exec > >(tee -a ${logFile}) 2>&1`, timeout_ms=3000);
const sshCmd = `echo 'Starting SSH - $(date)' && ssh -T ${SSH_USER}@${SSH_SERVER}`;
interact_with_process(PID, sshCmd, timeout_ms=10000);
interact_with_process(PID, "echo 'Ready!' && pwd && hostname", timeout_ms=5000);

// 2. Open log file with Enhanced Universal Environment Runner (Step 6)
console.log("Opening log file for real-time monitoring...");
start_process(`python3 ~/shawndev1/universal_env_runner/universal_env_runner.py xdg-open ${logFile}`, timeout_ms=10000);

// ✅ NEW: Enhanced xdg-open now works reliably in MCP contexts
// ✅ Automatic detection and direct launch with proper flags
// Fallbacks now rarely needed: 
// If still fails: start_process(`python3 ~/shawndev1/universal_env_runner/universal_env_runner.py codium ${logFile}`, timeout_ms=10000);

console.log(`✅ SSH session established with PID ${PID}`);
console.log(`✅ Real-time logging to: ${logFile}`);
console.log(`✅ Log file opened in GUI application`);
```

---

*** If user asks you to connect to zencart production server, use ssh -T -p 2022 partsfor@ftp.partsfortechs.com
*** If user asks you to connect to runtipi1 server, use ssh -T -p 22 user1@runtipi1.tail1da69.ts.net 
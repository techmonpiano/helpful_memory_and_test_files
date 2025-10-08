# MCP SSH Session Guide for LLMs - PERSISTENT SESSIONS

## **🎯 Key Point: MCP Tools Required for Persistence**

**CRITICAL**: For persistent SSH sessions that LLMs can interact with, you MUST use MCP tools like `start_process` and `interact_with_process`. Standalone scripts won't give you ongoing session control.

---

## **📁 Available Tools:**

### **1. MCP Command Generator** (RECOMMENDED)
**Location**: `~/shawndev1/helpful_memory_and_test_files/generate-mcp-ssh.sh`
- ✅ **Generates copy-paste MCP commands**
- ✅ **Creates persistent sessions** you can interact with
- ✅ **Returns PID** for ongoing `interact_with_process` usage

### **2. Standalone SSH Script** (Non-persistent)
**Location**: `~/shawndev1/helpful_memory_and_test_files/auto-ssh-session.sh`
- ❌ **Not persistent** - runs independently
- ❌ **No MCP interaction** - can't send commands after connection
- ✅ **Good for** one-time connections or testing

---

## **🚀 RECOMMENDED: MCP Command Generator**

### **Generate Copy-Paste Commands:**
```bash
# Generate commands for Zencart
~/shawndev1/helpful_memory_and_test_files/generate-mcp-ssh.sh zencart -v

# Generate commands for Runtipi  
~/shawndev1/helpful_memory_and_test_files/generate-mcp-ssh.sh runtipi -v

# Generate commands for custom server
~/shawndev1/helpful_memory_and_test_files/generate-mcp-ssh.sh user@server.com -p 2022 -v
```

### **Example Output (Copy These Commands):**
```javascript
// Step 1: Start bash process for SSH session
start_process("bash", timeout_ms=5000)

// SAVE THE RETURNED PID! Use it in all subsequent commands
// Example: const PID = 12345; (replace with actual PID)

// Step 2: Setup real-time logging (replace PID with actual value)
interact_with_process(PID, "exec > >(tee -a /tmp/ssh_session_20250910_132527.log) 2>&1", timeout_ms=3000)

// Step 3: Start SSH connection
interact_with_process(PID, "echo 'Starting SSH session - $(date)' && ssh -T -p 2022 partsfor@ftp.partsfortechs.com", timeout_ms=10000)

// Step 4: Test connection and verify session
interact_with_process(PID, "echo 'Session ready - $(date)' && pwd && hostname", timeout_ms=5000)

// Step 5: Open log file in GUI (optional - run in separate command)
start_process("python3 ~/shawndev1/universal_env_runner/universal_env_runner.py xdg-open /tmp/ssh_session_20250910_132527.log", timeout_ms=10000)

// Step 6: Verify logging is working
read_file("/tmp/ssh_session_20250910_132527.log")
```

### **After Setup - Ongoing Usage:**
```javascript
// Use the PID from step 1 for all commands:
interact_with_process(PID, "ls -la", timeout_ms=5000)
interact_with_process(PID, "cd /var/www", timeout_ms=3000)
interact_with_process(PID, "pwd", timeout_ms=3000)
interact_with_process(PID, "systemctl status nginx", timeout_ms=8000)

// Session management:
list_sessions()                                    // Check session status
read_process_output(PID, timeout_ms=5000)          // Read any pending output
force_terminate(PID)                               // End session when done
```

---

## **⚡ Quick Commands for Common Servers:**

### **Zencart Production Server:**
```bash
~/shawndev1/helpful_memory_and_test_files/generate-mcp-ssh.sh zencart
```
**Result**: `partsfor@ftp.partsfortechs.com:2022`

### **Runtipi1 Server:**
```bash
~/shawndev1/helpful_memory_and_test_files/generate-mcp-ssh.sh runtipi
```
**Result**: `user1@runtipi1.tail1da69.ts.net:22`

### **Custom Server:**
```bash
~/shawndev1/helpful_memory_and_test_files/generate-mcp-ssh.sh user@myserver.com -p 2022
```

---

## **🔧 Options Available:**

```bash
# Verbose output with explanations
~/shawndev1/helpful_memory_and_test_files/generate-mcp-ssh.sh zencart -v

# Skip GUI log file opening
~/shawndev1/helpful_memory_and_test_files/generate-mcp-ssh.sh runtipi --no-gui

# Custom log directory
~/shawndev1/helpful_memory_and_test_files/generate-mcp-ssh.sh zencart -l /home/user/logs

# JavaScript/JSON format output
~/shawndev1/helpful_memory_and_test_files/generate-mcp-ssh.sh runtipi -j
```

---

## **📋 Complete Workflow:**

### **1. Generate Commands:**
```bash
~/shawndev1/helpful_memory_and_test_files/generate-mcp-ssh.sh zencart -v
```

### **2. Copy and Execute the Generated MCP Commands:**
```javascript
// Copy each command from the output and execute in sequence:
start_process("bash", timeout_ms=5000)                    // Save the PID!
interact_with_process(PID, "exec > >(tee -a ...)", ...)   // Setup logging
interact_with_process(PID, "ssh -T ...", ...)             // Connect
interact_with_process(PID, "echo 'Session ready'", ...)   // Test
```

### **3. Work with Your Session:**
```javascript
// Now you have a persistent SSH session:
interact_with_process(PID, "your_commands_here", timeout_ms=8000)
```

---

## **🆚 Why MCP Tools vs Standalone Scripts?**

### **✅ MCP Tools (PERSISTENT):**
- **Ongoing Control**: Send commands anytime with `interact_with_process(PID, "command")`
- **Session Management**: Check status with `list_sessions()`
- **Real-time Interaction**: Read output with `read_process_output(PID)`
- **LLM Integration**: Full integration with LLM workflow

### **❌ Standalone Scripts (NOT PERSISTENT):**
- **One-time Execution**: Script runs and exits
- **No Ongoing Control**: Can't send additional commands
- **No PID**: No way to interact with the session
- **Isolated**: Runs separate from LLM environment

---

## **🎯 Key Benefits of This Approach:**

- ✅ **True Persistence**: Get a PID you can use indefinitely
- ✅ **Real-time Logging**: Immediate updates with `tee` method
- ✅ **GUI Integration**: Automatic log file opening
- ✅ **No Manual Steps**: Automated command generation
- ✅ **Error Prevention**: Pre-validated commands
- ✅ **Predefined Servers**: Simple `zencart` or `runtipi` shortcuts

---

## **🛠️ Troubleshooting:**

### **View Available Options:**
```bash
~/shawndev1/helpful_memory_and_test_files/generate-mcp-ssh.sh --help
```

### **Test Command Generation:**
```bash
# Generate commands without connecting
~/shawndev1/helpful_memory_and_test_files/generate-mcp-ssh.sh zencart -v --no-gui
```

### **If Session Becomes Unresponsive:**
```javascript
list_sessions()                // Check session status
force_terminate(PID)           // Force close if needed
```

---

## **📝 Summary:**

**Use the MCP Command Generator** to get copy-paste ready commands that create **persistent SSH sessions** you can interact with using `interact_with_process(PID, "commands")`.

**This maintains the persistent, interactive nature** while automating the complex setup process!

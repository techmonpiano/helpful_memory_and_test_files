# LLMS START HERE - Persistent SSH Session Setup

## **🎯 CRITICAL: You MUST use MCP tools for persistent sessions!**

**The LLM needs a PID to interact with the SSH session using `interact_with_process(PID, "commands")`**

---

## **⚡ FASTEST METHOD - Two Steps:**

### **Step 1: Generate MCP Commands**
```bash
~/shawndev1/helpful_memory_and_test_files/generate-mcp-ssh.sh zencart -v
```
**OR**
```bash
~/shawndev1/helpful_memory_and_test_files/generate-mcp-ssh.sh runtipi -v
```

### **Step 2: Copy and Execute the Generated Commands**
Copy each MCP command from the output and execute them in sequence. The first command will give you a PID - **SAVE IT!**

---

## **📋 What You'll Get:**

### **Generated Commands Look Like:**
```javascript
// Step 1: Start bash process for SSH session
start_process("bash", timeout_ms=5000)         // ← SAVE THE PID FROM THIS!

// Step 2: Setup real-time logging (replace PID with actual value)
interact_with_process(PID, "exec > >(tee -a /tmp/ssh_session_20250910_132527.log) 2>&1", timeout_ms=3000)

// Step 3: Start SSH connection  
interact_with_process(PID, "echo 'Starting SSH session - $(date)' && ssh -T -p 2022 partsfor@ftp.partsfortechs.com", timeout_ms=10000)

// Step 4: Test connection and verify session
interact_with_process(PID, "echo 'Session ready - $(date)' && pwd && hostname", timeout_ms=5000)

// Step 5: Open log file in GUI
start_process("python3 ~/shawndev1/universal_env_runner/universal_env_runner.py xdg-open /tmp/ssh_session_20250910_132527.log", timeout_ms=10000)
```

### **After Setup - Use Your Session:**
```javascript
// Now you can work with the persistent session:
interact_with_process(PID, "ls -la", timeout_ms=5000)
interact_with_process(PID, "cd /var/www", timeout_ms=3000)  
interact_with_process(PID, "systemctl status nginx", timeout_ms=8000)
```

---

## **🔧 Available Targets:**

| **Command** | **Server** | **Result** |
|-------------|------------|------------|
| `zencart` | Zencart Production | `partsfor@ftp.partsfortechs.com:2022` |
| `runtipi` | Runtipi1 Server | `user1@runtipi1.tail1da69.ts.net:22` |
| `user@server.com` | Custom Server | Direct connection |
| `user@server.com -p 2022` | Custom with Port | Custom server with specific port |

---

## **✅ Complete Example - Zencart Connection:**

### **Run This:**
```bash
~/shawndev1/helpful_memory_and_test_files/generate-mcp-ssh.sh zencart
```

### **Copy and Execute Each Generated Command:**
```javascript
start_process("bash", timeout_ms=5000)                    // Save the returned PID!
interact_with_process(PID, "exec > >(tee -a /tmp/ssh_session_TIMESTAMP.log) 2>&1", timeout_ms=3000)
interact_with_process(PID, "echo 'Starting SSH session - $(date)' && ssh -T -p 2022 partsfor@ftp.partsfortechs.com", timeout_ms=10000)
interact_with_process(PID, "echo 'Session ready - $(date)' && pwd && hostname", timeout_ms=5000)
```

### **Then Work Normally:**
```javascript
interact_with_process(PID, "your_commands_here", timeout_ms=8000)
```

---

## **🎯 Why This Method Works:**

- ✅ **Persistent**: You get a PID to interact with indefinitely
- ✅ **Real-time Logging**: Immediate updates with `tee` method  
- ✅ **GUI Integration**: Log file opens automatically
- ✅ **No Manual Steps**: Commands are pre-generated and validated
- ✅ **Predefined Servers**: Simple shortcuts for common targets

---

**That's it! Use the generator, copy the commands, execute them, save the PID, and you have a persistent SSH session.**

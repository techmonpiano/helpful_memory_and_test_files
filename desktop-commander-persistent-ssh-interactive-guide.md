# Desktop Commander MCP - Persistent SSH Session Guide

**Purpose**: Guide for establishing and managing persistent SSH sessions using Desktop Commander MCP tools

**Target Audience**: LLMs and developers working with remote server management

---

## 🔧 Basic SSH Connection Setup

### **Connection Command**:
```bash
ssh -T -p 2022 partsfor@ftp.partsfortechs.com
```

**Key Parameters**:
- `-T`: Disable pseudo-terminal allocation (recommended for automated sessions)
- `-p 2022`: Custom port specification
- Authentication: Key-based (no password required)

### **Desktop Commander Process Management**:
```bash
# Start SSH session
start_process("ssh -T -p 2022 partsfor@ftp.partsfortechs.com", timeout_ms=10000)

# Check session status
list_sessions()

# Interact with session
interact_with_process(pid, "ls -la", timeout_ms=5000)

# Read output
read_process_output(pid, timeout_ms=3000)
```

---

## 🎯 Session Management Best Practices

### **1. Connection Establishment**:
- Use `start_process()` with appropriate timeout (10+ seconds for network connections)
- Verify connection success before proceeding with commands
- Store Process ID (PID) for session management

### **2. Command Execution Pattern**:
```bash
# Check if session is active
list_sessions()  # Look for your PID

# Execute command and wait for response
interact_with_process(pid, "your_command_here", timeout_ms=8000, wait_for_prompt=true)

# For long-running commands, use separate read calls
read_process_output(pid, timeout_ms=15000)
```

### **3. Session Persistence Features**:
- **Automatic Recovery**: Desktop Commander maintains connection across local machine reboots
- **Process Tracking**: PIDs remain consistent for session management
- **Network Resilience**: Handles network latency and temporary disconnections

---

## 📊 Performance Characteristics

### **Connection Timing**:
- **Initial Connection**: 2-3 seconds (network latency dependent)
- **Command Response**: 1-2 seconds for basic commands
- **Session Persistence**: Maintained throughout entire work session

### **Reliability Features**:
- Persistent connection maintained during long operations
- Automatic session recovery after local system events
- Consistent PID tracking for multi-hour sessions

---

## 🔍 Common Usage Patterns

### **File Operations**:
```bash
# Navigate directories
interact_with_process(pid, "cd /path/to/directory")

# List files with details
interact_with_process(pid, "ls -la")

# Check file contents
interact_with_process(pid, "head -20 filename.log")

# File transfer (if needed)
interact_with_process(pid, "scp local_file remote_path")
```

### **System Information**:
```bash
# Check system status
interact_with_process(pid, "df -h")  # Disk usage
interact_with_process(pid, "ps aux | head -10")  # Running processes
interact_with_process(pid, "uptime")  # System uptime

# Check cron jobs
interact_with_process(pid, "crontab -l")
```

### **Application Management**:
```bash
# PHP script execution
interact_with_process(pid, "php script_name.php --dry-run")

# Log file analysis
interact_with_process(pid, "tail -f /path/to/log/file.log")

# Git operations
interact_with_process(pid, "git status")
interact_with_process(pid, "git log --oneline -5")
```

---

## 🚨 CRITICAL SAFETY RULES for This Server:

### **NEVER Work from Web-Accessible Directories:**
- **❌ DANGEROUS**: `/home/partsfor/public_html/logs/` (where you want to check)
- **❌ DANGEROUS**: `/home/partsfor/public_html/` (any subdirectory)

### **✅ SAFE Protocol:**
1. **Always stay in home directory**: `cd /home/partsfor`
2. **Use full paths for analysis**: `/home/partsfor/public_html/logs/file.log`
3. **Limit output**: Use targeted searches, not broad listings

### **Why This Server Is Dangerous:**
- **LiteSpeed server** (not Apache) - more sensitive to file operations
- File operations in web directories trigger **PHP processes** that can get stuck
- Multiple stuck `lsphp` processes cause **522 Cloudflare errors**
- They previously caused a **5-10 minute site outage** doing log analysis

### **Safe Commands for Log Analysis:**
```bash
# ✅ SAFE - Analyze from home directory using full paths
cd /home/partsfor
find /home/partsfor/public_html/logs -name "*pattern*" -type f | head -10

# ❌ DANGEROUS - Working from inside web directory
cd /home/partsfor/public_html/logs/
ls -la *.log  # Can trigger stuck PHP processes!
```

### **Emergency Recovery (if 522 errors occur):**
1. Check for stuck processes: `ps aux | grep lsphp | grep -v grep`
2. Kill stuck processes: `kill [PID1] [PID2] [PID3]`
3. Exit web directories: `cd /home/partsfor`
4. Wait 2-3 minutes for stabilization

---

## 🚨 Session Management Tips

### **Connection Monitoring**:
- Use `list_sessions()` regularly to verify session status
- Look for "Blocked: true/false" status to understand session state
- Monitor runtime to track session duration

### **Error Handling**:
- If commands hang, check timeout settings (increase for slow operations)
- Use `force_terminate(pid)` only as last resort
- Re-establish connection if session becomes unresponsive

### **Security Considerations**:
- Use key-based authentication (no passwords in commands)
- Limit session duration for security best practices
- Terminate sessions when work is complete: `force_terminate(pid)`

---

## 📋 Quick Command Reference

| Operation | Command |
|-----------|---------|
| Start SSH Session | `start_process("ssh -T -p 2022 user@host")` |
| List Active Sessions | `list_sessions()` |
| Execute Command | `interact_with_process(pid, "command")` |
| Read Output | `read_process_output(pid)` |
| Check Session Status | `list_sessions()` (look for PID) |
| Terminate Session | `force_terminate(pid)` |

---

## 🎯 Example Session Flow

```bash
# 1. Establish connection
start_process("ssh -T -p 2022 partsfor@ftp.partsfortechs.com", timeout_ms=10000)
# Note the returned PID (e.g., 43107)

# 2. Verify connection
list_sessions()  # Confirm PID 43107 is active

# 3. Execute commands
interact_with_process(43107, "pwd")  # Check current directory
interact_with_process(43107, "ls -la")  # List files

# 4. Long-running operations
interact_with_process(43107, "php large_script.php", timeout_ms=30000)

# 5. Monitor progress
read_process_output(43107, timeout_ms=5000)

# 6. Clean up when done
force_terminate(43107)
```

---

**Key Advantage**: Desktop Commander MCP provides reliable, persistent SSH session management with automatic recovery and consistent process tracking, ideal for extended remote server operations.
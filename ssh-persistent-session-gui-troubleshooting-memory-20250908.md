# SSH Persistent Session + GUI Application Troubleshooting Memory
**Date:** September 8, 2025  
**Session:** runtipi1.tail1da69.ts.net SSH + Desktop Commander MCP GUI Integration  
**Status:** ✅ COMPLETE SUCCESS  

---

## 🎯 **Session Overview**

Successfully established SSH persistent session to runtipi1 server with real-time logging, and solved GUI application launching challenges in Desktop Commander MCP environment. Discovered working solutions for multiple text editors and established reliable patterns for future use.

---

## 🚀 **Final Working Solutions**

### **SSH Persistent Session to runtipi1**
```bash
# Step 1: Start bash process for logging setup
start_process("bash", timeout_ms=5000)  # Returns PID 808038

# Step 2: Setup real-time logging with tee (no buffering)
interact_with_process(PID, "exec > >(tee -a /tmp/ssh_session_runtipi1_$(date +%Y%m%d_%H%M%S).log) 2>&1", timeout_ms=3000)

# Step 3: SSH connection (corrected port)
interact_with_process(PID, "echo 'Starting SSH session to runtipi1 - $(date)' && ssh -T user1@runtipi1.tail1da69.ts.net", timeout_ms=10000)

# Result: Connected successfully on port 22 (not 2022)
# Log file: /tmp/ssh_session_runtipi1_20250908_085005.log
```

### **GUI Application Launching (Working Solutions)**

#### **Environment Variables Required:**
```bash
WAYLAND_DISPLAY=wayland-0
XDG_RUNTIME_DIR=/run/user/1000
XDG_SESSION_TYPE=wayland
XDG_CURRENT_DESKTOP=zorin:GNOME
```

#### **gedit (Simple Text Editor) - WORKS:**
```bash
cd /home/user1 && bash -l -c "WAYLAND_DISPLAY=wayland-0 XDG_RUNTIME_DIR=/run/user/1000 XDG_SESSION_TYPE=wayland XDG_CURRENT_DESKTOP=zorin:GNOME gedit /tmp/ssh_session_runtipi1_20250908_085005.log &"
```

#### **VS Code (Advanced Editor) - WORKS:**
```bash
cd /home/user1 && bash -l -c "WAYLAND_DISPLAY=wayland-0 XDG_RUNTIME_DIR=/run/user/1000 XDG_SESSION_TYPE=wayland XDG_CURRENT_DESKTOP=zorin:GNOME code --no-sandbox --disable-gpu-sandbox --enable-features=UseOzonePlatform --ozone-platform=wayland /tmp/ssh_session_runtipi1_20250908_085005.log &"
```

#### **Universal Environment Runner (Enhanced Method):**
```bash
cd /home/user1 && bash -l -c "DESKTOP_COMMANDER=true python3 /home/user1/shawndev1/universal_env_runner/universal_env_runner.py xdg-open /tmp/ssh_session_runtipi1_20250908_085005.log"
```

---

## 🔍 **Troubleshooting Journey & Discoveries**

### **Problem 1: SSH Connection Port Issue**
**❌ Failed Attempt:**
```bash
ssh -T -p 2022 user1@runtipi1.tail1da69.ts.net
# Result: Connection refused
```

**✅ Working Solution:**
```bash
ssh -T user1@runtipi1.tail1da69.ts.net  # Standard port 22
# Result: Success - Connected to Debian GNU/Linux system
```

**Key Learning:** Always try standard port 22 first, even if documentation suggests custom ports.

### **Problem 2: GUI Applications Not Opening from MCP**
**❌ Failed Attempts:**

1. **Direct xdg-open (no environment):**
```bash
xdg-open /tmp/ssh_session_runtipi1_20250908_085005.log
# Result: "cannot open display" errors
```

2. **Manual DISPLAY setting:**
```bash
DISPLAY=:0 xdg-open /tmp/file.log
# Result: Authorization required, segmentation fault
```

3. **Universal Environment Runner (initial attempts):**
```bash
python3 universal_env_runner.py xdg-open /tmp/file.log
# Result: Detected "headless" environment, just displayed file contents
```

4. **Login shell without environment variables:**
```bash
cd /home/user1 && bash -l -c "python3 universal_env_runner.py xdg-open /tmp/file.log"
# Result: Still detected headless, MCP Context: False
```

**✅ Breakthrough Discovery:**
GUI applications CAN work from Desktop Commander MCP, but require:
1. **Correct Wayland environment variables**
2. **Proper runtime directory access**
3. **Application-specific flags (for complex apps like VS Code)**

### **Problem 3: Universal Environment Runner MCP Detection**
**❌ Issue:** Script wasn't detecting MCP context automatically in our setup

**✅ Solution:** Explicit MCP detection trigger:
```bash
DESKTOP_COMMANDER=true python3 universal_env_runner.py [command]
# Result: Properly detected MCP and injected GUI environment
```

### **Problem 4: VS Code Specific Launching Issues**
**❌ Failed:** Basic VS Code launch (exit code 0 but no window)
```bash
code /tmp/file.log
```

**✅ Success:** VS Code with Wayland sandbox flags:
```bash
code --no-sandbox --disable-gpu-sandbox --enable-features=UseOzonePlatform --ozone-platform=wayland /tmp/file.log
```

---

## 🧪 **Environment Discovery Process**

### **System Analysis Results:**
```bash
# Display processes running:
- Xwayland :0 (primary display server)
- wayland-0 socket at /run/user/1000/wayland-0
- All applications using --ozone-platform=wayland
- Desktop: zorin:GNOME

# Working runtime directory: /run/user/1000
# User ID: 1000
# Session type: wayland
```

### **Critical Environment Variables:**
```bash
WAYLAND_DISPLAY=wayland-0          # Actual Wayland socket
XDG_RUNTIME_DIR=/run/user/1000     # User runtime directory  
XDG_SESSION_TYPE=wayland           # Session type
XDG_CURRENT_DESKTOP=zorin:GNOME    # Desktop environment
```

---

## 📋 **Universal Environment Runner Analysis**

### **Script Capabilities (Updated Version):**
- ✅ **MCP Context Detection:** Automatically detects Desktop Commander environments
- ✅ **Smart Environment Injection:** Injects GUI variables when MCP detected
- ✅ **Cross-platform Support:** Works with X11, Wayland, headless
- ✅ **Fallback Behavior:** Uses available tools when preferred ones fail

### **MCP Detection Triggers:**
1. Environment variables: `DESKTOP_COMMANDER`, `MCP_SERVER`, `CLAUDE_MCP`
2. Working directory patterns: `/usr/lib/claude-desktop`, etc.
3. Process hierarchy analysis
4. **Manual trigger:** `DESKTOP_COMMANDER=true`

### **Environment Injection Results:**
```
🔧 MCP Context Detected - Injecting GUI environment
   Injected WAYLAND_DISPLAY: wayland-0
   Injected XDG_CURRENT_DESKTOP: zorin:GNOME
✅ GUI environment injection complete
```

---

## 🛠️ **Technical Implementation Details**

### **SSH Real-time Logging Setup:**
```bash
# Uses tee for immediate logging (no buffering issues)
exec > >(tee -a /tmp/ssh_session_TIMESTAMP.log) 2>&1

# Advantages over 'script' command:
- Real-time file writes
- No buffering delays
- Concurrent log file access
- Works across different systems
```

### **Desktop Commander MCP Environment Characteristics:**
- **Working Directory:** `/usr/lib/claude-desktop` (for detection)
- **Environment Isolation:** Limited access to user GUI session
- **D-Bus Limitations:** `$DBUS_SESSION_BUS_ADDRESS` not accessible
- **Permission Model:** Restricted but GUI apps can work with proper setup

### **Application-Specific Requirements:**

#### **Simple GUI Apps (gedit, calculator):**
- Basic Wayland environment variables sufficient
- Quick startup, reliable operation

#### **Complex GUI Apps (VS Code, Electron-based):**
- Require sandbox bypass flags
- Need explicit Wayland platform specification
- Longer startup times but full functionality

---

## 📚 **Key Files and Locations**

### **SSH Session Log:**
```
/tmp/ssh_session_runtipi1_20250908_085005.log
- Real-time logging active
- Contains complete session history
- Open in gedit and VS Code for monitoring
```

### **Universal Environment Runner:**
```
/home/user1/shawndev1/universal_env_runner/universal_env_runner.py
- Updated with MCP detection
- Smart environment injection
- Cross-platform compatibility
```

### **SSH Session Guide:**
```
/home/user1/shawndev1/helpful_memory_and_test_files/llm-ssh-session-guide-with-logging.md
- Comprehensive SSH setup instructions
- Real-time logging methodology
- Best practices and troubleshooting
```

---

## 🎯 **Success Verification**

### **Active Processes:**
```bash
# SSH Session: PID 808038 (runtipi1 connection)
# gedit: PID 15794 (log file open)
# VS Code: Successfully launched with Wayland flags
# Log monitoring: Real-time updates in both editors
```

### **Test Commands Executed:**
```bash
# On runtipi1 server:
echo 'Testing real-time logging - $(date)' && ls -la
pwd && hostname && whoami

# Results: All logged in real-time to local file
# Visible immediately in both gedit and VS Code
```

---

## 🔮 **Future Use Patterns**

### **Quick SSH + Logging Setup:**
```bash
# 1. Start process and get PID
start_process("bash", timeout_ms=5000)

# 2. Setup logging
interact_with_process(PID, "exec > >(tee -a /tmp/ssh_session_$(date +%Y%m%d_%H%M%S).log) 2>&1", timeout_ms=3000)

# 3. Connect SSH
interact_with_process(PID, "ssh -T user@server", timeout_ms=10000)
```

### **GUI App Launch Templates:**

#### **Simple Apps:**
```bash
WAYLAND_DISPLAY=wayland-0 XDG_RUNTIME_DIR=/run/user/1000 XDG_SESSION_TYPE=wayland XDG_CURRENT_DESKTOP=zorin:GNOME [app] [file] &
```

#### **Complex Apps (Electron/Chrome-based):**
```bash
WAYLAND_DISPLAY=wayland-0 XDG_RUNTIME_DIR=/run/user/1000 XDG_SESSION_TYPE=wayland XDG_CURRENT_DESKTOP=zorin:GNOME [app] --no-sandbox --disable-gpu-sandbox --enable-features=UseOzonePlatform --ozone-platform=wayland [file] &
```

#### **Universal Environment Runner:**
```bash
cd /home/user1 && bash -l -c "DESKTOP_COMMANDER=true python3 /home/user1/shawndev1/universal_env_runner/universal_env_runner.py [command] [args]"
```

---

## 💡 **Key Insights & Lessons Learned**

### **SSH Connection Insights:**
1. **Port assumptions can be wrong** - Always test standard ports first
2. **Real-time logging with tee is superior** - No buffering issues vs script command
3. **Local log files enable concurrent monitoring** - Multiple editors can watch same file

### **GUI Application Insights:**
1. **Desktop Commander MCP is not completely isolated** - GUI apps can work with proper setup
2. **Environment variables are critical** - Must match actual system configuration
3. **Application complexity affects requirements** - Simple vs complex apps need different approaches
4. **Wayland requires specific flags** - Especially for Electron/Chromium-based applications

### **Troubleshooting Insights:**
1. **Test simple apps first** - Calculator confirmed GUI capability
2. **Process analysis reveals truth** - `ps aux` showed actual Wayland configuration
3. **Incremental testing works** - Build up from working simple cases
4. **Exit code 0 doesn't guarantee GUI launch** - Need additional verification methods

### **Universal Environment Runner Insights:**
1. **MCP detection can be explicit** - Use `DESKTOP_COMMANDER=true` when auto-detection fails
2. **Environment injection works well** - Script correctly identifies and sets variables
3. **Fallback behavior is valuable** - Script handles missing tools gracefully

---

## 🔧 **Debugging Techniques Used**

### **Environment Analysis:**
```bash
# Check actual display processes
ps aux | grep -E "(wayland|Xorg|X11)"

# Check runtime directory contents  
ls -la /run/user/1000/ | grep wayland

# Check environment variables
env | grep -E "(DISPLAY|WAYLAND|XDG|DESKTOP)"
```

### **Application Testing:**
```bash
# Test simple GUI app first
gnome-calculator &

# Check running processes
ps aux | grep -E "(gedit|code)" | grep -v grep

# Verify application launch
echo $?  # Check exit code
```

### **Session Verification:**
```bash
# Check SSH session status
list_sessions()  # Desktop Commander command

# Verify logging
tail -f /tmp/ssh_session_*.log

# Test real-time updates
interact_with_process(PID, "echo 'test - $(date)'", timeout_ms=5000)
```

---

## 📋 **Quick Reference Commands**

### **Immediate SSH Setup:**
```bash
# Complete one-liner for future sessions:
start_process("bash") -> interact_with_process(PID, "exec > >(tee -a /tmp/ssh_$(date +%Y%m%d_%H%M%S).log) 2>&1") -> interact_with_process(PID, "ssh -T user1@runtipi1.tail1da69.ts.net")
```

### **GUI App Launch (Working Environment):**
```bash
ENV_VARS="WAYLAND_DISPLAY=wayland-0 XDG_RUNTIME_DIR=/run/user/1000 XDG_SESSION_TYPE=wayland XDG_CURRENT_DESKTOP=zorin:GNOME"
WORKING_CMD="cd /home/user1 && bash -l -c \"$ENV_VARS [command]\""
```

### **Universal Environment Runner:**
```bash
UER_PATH="/home/user1/shawndev1/universal_env_runner/universal_env_runner.py"
COMMAND="cd /home/user1 && bash -l -c \"DESKTOP_COMMANDER=true python3 $UER_PATH [app] [file]\""
```

---

## ✅ **Session Success Summary**

1. **✅ SSH Persistent Session** - Successfully connected to runtipi1.tail1da69.ts.net
2. **✅ Real-time Logging** - Implemented with tee method, no buffering issues  
3. **✅ GUI Application Launch** - Solved Desktop Commander MCP restrictions
4. **✅ Multiple Editor Support** - Both gedit and VS Code working
5. **✅ Universal Environment Runner** - Enhanced with MCP detection
6. **✅ Comprehensive Documentation** - All solutions captured for future use

**Final Status:** Complete success with all objectives achieved and robust solutions established for future sessions.

---

*This memory file serves as a comprehensive reference for SSH persistent sessions, GUI application troubleshooting in Desktop Commander MCP environments, and the universal environment runner script capabilities.*
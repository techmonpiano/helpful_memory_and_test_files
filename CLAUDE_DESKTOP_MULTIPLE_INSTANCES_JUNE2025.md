## **grep Search Strategy - Primary Tool**

### **1. ALWAYS Use grep First**
- **grep -n "PATTERN" file.py** - Search single file with line numbers
- **grep -r -n "PATTERN" . 2>/dev/null** - Search recursively, skip permission errors
- **grep -n -C3 "PATTERN" file.py** - Search with 3 lines context (can use -C10, -C20 or more as needed)
- **grep -r -n --exclude='*backup*' "PATTERN" . 2>/dev/null** - Recursive search, exclude noise, skip errors
- For file operations: **read_file**, **edit_block**, **write_file** (MCP tools)

**CRITICAL: Directory searches REQUIRE -r flag**
- Without -r: grep expects specific files only
- With -r: grep searches directories recursively
- Add **2>/dev/null** to suppress permission denied warnings

**grep is universally available** and provides reliable, consistent results.

### **2. Tool Escalation Hierarchy (MANDATORY ORDER)**
1. **PRIMARY: grep** (universal, reliable, standard tool)
2. **SECONDARY: MCP tools** (when grep isn't suitable, use --maxResults=25-50)  
3. **TERTIARY: Task tool** (conceptual, multi-file searches)
4. **LAST RESORT: Claude Code tools** (basic operations only)

**Always follow this order** - no exceptions.

### **3. grep Examples and Syntax**

#### **✅ CORRECT grep Syntax:**
```bash
# Basic search - single file (NO -r flag!)
grep -n "PATTERN" file.py

# Recursive directory search (MUST use -r flag!)
grep -r -n "PATTERN" . 2>/dev/null

# OR patterns - use extended regex with -E
grep -E -n "pattern1|pattern2|pattern3" file.py
grep -r -E -n "func1|func2|func3" /directory/ 2>/dev/null

# Literal string search (when pattern has special chars)
grep -F -n "function_call()" file.py
grep -F -n "array[index]" file.py
grep -F -n "price: $99.99" file.txt

# With context (flexible - use more lines as needed)
grep -n -C3 "PATTERN" file.py    # 3 lines before and after
grep -n -C10 "PATTERN" file.py   # 10 lines before and after  
grep -n -C20 "PATTERN" file.py   # 20 lines before and after (or any number)
grep -n -B5 -A10 "PATTERN" file.py  # 5 before, 10 after (asymmetric context)

# Multiple specific files
grep -n "PATTERN" file1.py file2.py

# Recursive search, exclude noise files
grep -r -n --exclude='*backup*' --exclude='*.txt' "PATTERN" . 2>/dev/null

# Case insensitive
grep -i -n "PATTERN" file.py
grep -r -i -n "PATTERN" /directory/ 2>/dev/null

# Beginning of line anchor
grep -n "^setup_grub" /full/path/to/file.sh
grep -n "^def " file.py  # Find function definitions

# Word boundaries
grep -w -n "function" file.py  # Match whole words only
```

#### **🔧 Common grep Patterns:**
```bash
# Find function definitions
grep -n "^def " *.py
grep -n "function " *.js

# Find imports
grep -n "^import\|^from.*import" *.py
grep -n "require\|import" *.js

# Find TODO comments
grep -r -n "TODO\|FIXME\|BUG" . 2>/dev/null

# Find configuration patterns
grep -r -n "config\|setting" . 2>/dev/null

# Count matches
grep -c "PATTERN" file.py
grep -r -c "PATTERN" . 2>/dev/null
```

#### **📝 Quick Reference:**

| Task | Command |
|------|---------|
| Search single file | `grep -n "pattern" file.txt` |
| Search directory | `grep -r -n "pattern" . 2>/dev/null` |
| Case insensitive | `grep -i -n "pattern" file.txt` |
| Literal search | `grep -F -n "literal()" file.txt` |
| OR patterns | `grep -E -n "pat1\|pat2" file.txt` |
| With context | `grep -n -C3 "pattern" file.txt` |
| Exclude files | `grep -r -n --exclude='*.log' "pattern" .` |
| Count matches | `grep -c "pattern" file.txt` |

# Claude Desktop Multiple Instances Guide

**Date:** June 2025  
**System:** Linux (Zorin OS 17.3)

## Installation Details

- **Path:** `/usr/bin/claude-desktop`
- **Type:** Bash shell script wrapper
- **Actual Electron binary:** `/usr/lib/claude-desktop/node_modules/electron/dist/electron`
- **App bundle:** `/usr/lib/claude-desktop/app.asar`

## Current Running Status

Claude Desktop is typically running with multiple processes:
- Main Electron process with Wayland flags
- Chrome crashpad handlers
- Various zygote processes
- High CPU usage processes (renderer threads)

## Methods to Force Second Instance

### Method 1: New Instance Flag
```bash
claude-desktop --new-instance
```
- **Pros:** Simple, uses official Electron flag
- **Cons:** May share same user data directory

### Method 2: Separate User Data Directory
```bash
claude-desktop --user-data-dir=/tmp/claude-instance-2
```
- **Pros:** Complete isolation, separate settings/cache
- **Cons:** Fresh login required, separate configuration

### Method 3: Combined Flags
```bash
claude-desktop --new-instance --user-data-dir=/tmp/claude-instance-2
```
- **Pros:** Best of both methods
- **Cons:** Most resource intensive

### Method 4: Direct Electron Execution
```bash
cd /usr/lib/claude-desktop
/usr/lib/claude-desktop/node_modules/electron/dist/electron /usr/lib/claude-desktop/app.asar --new-instance
```
- **Pros:** Bypasses wrapper script entirely
- **Cons:** May miss Wayland optimizations from wrapper

### Method 5: Environment Variable Modification
```bash
ELECTRON_ENABLE_LOGGING=1 claude-desktop --new-instance
```
- **Pros:** Additional debugging info
- **Cons:** More verbose output

## Wayland Considerations

The launcher script automatically detects Wayland and adds these flags:
- `--enable-features=UseOzonePlatform,WaylandWindowDecorations`
- `--ozone-platform=wayland`
- `--enable-wayland-ime`
- `--wayland-text-input-version=3`

## Troubleshooting

### If Second Instance Won't Start:
1. Check if first instance is consuming too many resources
2. Try terminating existing instances first
3. Use different user data directory
4. Check log file: `~/claude-desktop-launcher.log`

### Resource Usage:
- Each instance uses significant RAM (200MB+ per instance)
- High CPU usage is normal for active renderer processes
- Multiple instances will multiply resource consumption

## Commands Reference

```bash
# Check current instances
ps aux | grep claude-desktop

# Kill all instances
pkill -f claude-desktop

# Start fresh second instance
claude-desktop --new-instance --user-data-dir=/tmp/claude-instance-2

# View launcher logs
tail -f ~/claude-desktop-launcher.log
```

## Notes

- Electron applications typically enforce single-instance by default
- Each method has different isolation levels
- Consider system resources before running multiple instances
- Wayland support is automatically configured by the wrapper script
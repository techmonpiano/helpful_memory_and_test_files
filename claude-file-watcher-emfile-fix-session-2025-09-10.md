# Claude File Watcher EMFILE Error - Troubleshooting Session
**Date:** 2025-09-10  
**Issue:** `Error: EMFILE: too many open files, watch '/home/user1/.claude/settings.json'`

## Problem Analysis

### Initial Error
```
Error: EMFILE: too many open files, watch '/home/user1/.claude/settings.json'
    at FSWatcher.<computed> (node:internal/fs/watchers:254:19)
    at watch (node:fs:2539:36)
    at FzA (file:///home/user1/.claude/local/node_modules/@anthropic-ai/claude-code/cli.js:784:7030)
```

### Root Cause Discovery
1. **File Descriptor Limit Check:** `ulimit -n` showed 1,048,576 (already very high)
2. **Open Files Investigation:** `lsof | grep claude | wc -l` revealed **14,063 open files** by claude processes
3. **File System Analysis:** `find /home/user1 -name "*.json" -type f | wc -l` found **50,237 JSON files**

### Key Finding
Claude's file watcher was attempting to monitor an excessive number of files, particularly in:
- `docker/` directories (MySQL data, nginx configs)
- `ubuntu-bootstrap/` directories (Ubuntu filesystem images)
- `conty-ubuntu/` directories (Container filesystem)
- `node_modules/` directories
- Various cache and temporary directories

## Failed Attempts
- `pkill -f claude` - Command executed but didn't provide feedback on success

## Successful Solutions

### 1. Immediate Fix: Kill Excessive Processes
```bash
pkill -f claude
```
- Terminated all claude processes consuming excessive file descriptors
- Cleared the immediate EMFILE error condition

### 2. System-Level Fix: Increase inotify Limits
```bash
echo "fs.inotify.max_user_watches=524288" | sudo tee -a /etc/sysctl.conf
sudo sysctl -p
```
- Increased inotify watch limit from default to 524,288
- Provides system-wide protection against future file watcher overload

### 3. Permanent Fix: Claude Ignore Configuration
Created `/home/user1/.claudeignore` with content:
```
node_modules/
docker/
ubuntu-bootstrap/
conty-ubuntu/
.git/
__pycache__/
*.log
*.tmp
.cache/
.local/share/
```

## Technical Details

### File Watcher Behavior
- Claude's CLI tool uses Node.js `fs.watch()` to monitor file changes
- Without proper exclusions, it attempts to watch ALL files in the working directory tree
- Large development environments with Docker containers, VM images, and build artifacts create tens of thousands of files

### System Resource Impact
- Each watched file consumes a file descriptor
- Linux systems have per-process limits on open file descriptors
- inotify watches are a finite kernel resource that can be exhausted
- **inotify has TWO separate limits:**
  - `max_user_watches`: Total number of files that can be watched (default: 8,192-65,536)
  - `max_user_instances`: Number of inotify instances/watcher objects (default: 128)

## Prevention Strategy

### Directory Exclusion Best Practices
Always exclude from file watching:
- `node_modules/` - NPM dependencies
- `docker/` - Container data volumes
- `*-bootstrap/` - OS filesystem images
- `.git/` - Git repository data
- Build output directories
- Cache directories
- Log files and temporary files

### Monitoring Commands
```bash
# Check current file descriptor usage
lsof | grep claude | wc -l

# Check inotify watch usage
cat /proc/sys/fs/inotify/max_user_watches
cat /proc/sys/fs/inotify/max_user_instances

# Check inotify usage for specific process
lsof -p PID | grep -c inotify

# Count potential watch targets
find /home/user1 -name "*.json" -type f | wc -l
```

## Lessons Learned

1. **File Watcher Scope:** Always configure exclusions before using file-watching tools in large development environments
2. **Resource Monitoring:** Monitor file descriptor usage in long-running development tools
3. **System Limits:** Understand and configure appropriate system resource limits
4. **Preventive Configuration:** Create `.claudeignore` files proactively in new projects

## Environment Context
- **OS:** Linux 6.8.0-79-generic (Zorin OS 17.3)
- **Working Directory:** `/home/user1/shawndev1` (large development workspace)
- **File Count:** 50,237+ JSON files across multiple Docker and VM projects
- **Claude Version:** 0.9.2

## Resolution Status
✅ **RESOLVED** - All three solutions implemented:
1. Processes killed and resources freed
2. System limits increased
3. Ignore file created for future prevention

---

## Update: 2025-10-01 - Additional inotify Instance Limit Fix

### Recurring Issue
Same EMFILE error occurred with 8 Claude processes running simultaneously:
- `ulimit -n`: 1,048,576 (already high)
- `max_user_watches`: 1,048,576 (already increased)
- Current process had **7,061 inotify watchers** open
- Error: "EMFILE: too many open files, watch"

### Root Cause
**Missing limit:** `max_user_instances` was still at default (~128)

Multiple Claude processes were hitting the **inotify instances limit**, not the watches limit.

### Solution Applied
```bash
echo "fs.inotify.max_user_instances = 8192" | sudo tee -a /etc/sysctl.conf
sudo sysctl -p
```

### Key Takeaway
**Two separate inotify limits must be configured:**
1. `max_user_watches` = 524,288+ (total files watchable)
2. `max_user_instances` = 8,192 (number of watcher objects)

Running multiple Claude sessions requires increasing BOTH limits.
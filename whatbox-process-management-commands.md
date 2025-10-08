# Whatbox Process Management Commands Research

## Overview
Research conducted on Whatbox.ca wiki for process management commands. Whatbox is a shared hosting service without root access but allows rootless Podman containers.

## Key Findings from Whatbox Wiki

### Process Restart Commands Found

**rTorrent restart:**
```bash
killall rtorrent\ main && screen -dmS rTorrent rtorrent
```

**General restart pattern:**
```bash
killall [process_name]
screen -dmS [session_name] [command]
```

### Screen Session Management
```bash
screen -r        # Reattach to screen session
screen -D        # Detach stuck session
screen -wipe     # Clean up dead sessions
screen -ls       # List screen sessions (standard Linux)
```

### Deluge Management
```bash
deluge-console                           # Start Deluge console
deluge-console "connect 127.0.0.1:PORT" # Connect to daemon
```

## Process Listing Commands - NOT Documented in Wiki

The Whatbox wiki **does NOT explicitly document** standard process listing commands:
- `ps` (process status)
- `top` (real-time process viewer)
- `htop` (enhanced top)
- `pgrep` (process grep)

## Standard Linux Commands (Should Work)

Since Whatbox provides bash shell access, these commands should be available:

### List Processes
```bash
# List your processes only
ps aux | grep $USER
ps -ef | grep $USER

# Find specific processes
pgrep -f "process_name"
ps aux | grep "process_name"

# Real-time monitoring (if installed)
top
htop
```

### Podman Container Management
```bash
podman ps           # List running containers
podman ps -a        # List all containers
podman restart [container_name]
podman stop [container] && podman start [container]
```

### Process Control
```bash
killall [process_name]    # Kill by name
kill [PID]               # Kill by process ID
pkill [pattern]          # Kill by pattern
```

## Wiki Structure Analysis

**Pages Searched:**
- Main wiki index
- SSH documentation
- Bash Shell Commands page
- rTorrent documentation  
- Deluge documentation
- screen documentation

**Key Limitation:**
- No root access (shared hosting)
- No systemctl or service management
- Apps typically run in screen sessions
- Focus on torrent client management rather than general system administration

## Recommendations

1. **For general process listing:** Use standard Linux `ps`, `top`, `htop` commands
2. **For app restarts:** Follow the `killall + screen` pattern shown for rTorrent
3. **For containers:** Use `podman ps` and `podman restart` commands
4. **For support:** Contact Whatbox support for specific process management needs

## Research Date
August 18, 2025

## Sources
- https://whatbox.ca/wiki
- https://whatbox.ca/wiki/SSH
- https://whatbox.ca/wiki/rTorrent
- https://whatbox.ca/wiki/Deluge
- https://whatbox.ca/wiki/screen
- https://whatbox.ca/wiki/Bash_Shell_Commands
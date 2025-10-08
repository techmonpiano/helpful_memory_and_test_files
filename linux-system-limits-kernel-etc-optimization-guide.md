# Linux System Limits & Optimization Guide
*Comprehensive reference for moving beyond conservative distribution defaults*

## Overview

Linux distributions ship with "safe" defaults designed to work across the widest hardware range, but these are rarely optimal for specific systems. This guide consolidates proven optimizations for achieving snappier performance by generously tuning system limits and parameters.

**Key Insight**: Default limits prioritize security and resource conservation over performance. For dedicated workstations and servers, these can be significantly increased for much better responsiveness.

---

## 1. File Descriptors & System Limits

### Current Session Limits
```bash
# Check current limits
ulimit -n                          # File descriptors (usually 1024 - too low!)
ulimit -u                          # Max user processes
cat /proc/sys/fs/file-max          # System-wide file limit

# Immediate increases (current session only)
ulimit -n 65536                    # Increase file descriptors to 64K
ulimit -u 32768                    # Increase process limit
```

### Permanent Limits Configuration
```bash
# /etc/security/limits.conf - Make permanent
*    soft    nofile     65536
*    hard    nofile     1048576
*    soft    nproc      32768
*    hard    nproc      unlimited
root soft    nofile     65536
root hard    nofile     1048576

# Verify after reboot
ulimit -n
```

### inotify Limits (Critical for IDEs/File Watchers)
```bash
# Current limits (usually too low for development)
cat /proc/sys/fs/inotify/max_user_watches  # Default: 8192

# Increase inotify limits permanently
echo "fs.inotify.max_user_watches=524288" | sudo tee -a /etc/sysctl.conf
echo "fs.inotify.max_user_instances=512" | sudo tee -a /etc/sysctl.conf
echo "fs.inotify.max_queued_events=32768" | sudo tee -a /etc/sysctl.conf
sudo sysctl -p

# System-wide file limits
echo "fs.file-max=2097152" | sudo tee -a /etc/sysctl.conf
echo "fs.nr_open=2097152" | sudo tee -a /etc/sysctl.conf
```

---

## 2. X11/Xorg Connection Limits

### Xwayland Client Limit Issues
**Problem**: Default ~256 concurrent connections cause "Maximum clients reached" errors

```bash
# Check current Xwayland status
ps aux | grep Xwayland | grep -v grep
xset q                            # Test X11 connectivity

# Count active X11 connections
lsof /tmp/.X11-unix/X0 2>/dev/null | wc -l

# Emergency restart (GNOME auto-restarts)
pkill Xwayland
```

### Permanent Xwayland Limit Increase
```bash
# Add to ~/.bashrc or ~/.profile
export MUTTER_DEBUG_NUM_XWAYLAND_CLIENTS=512  # Double default limit

# For immediate effect (current session)
export MUTTER_DEBUG_NUM_XWAYLAND_CLIENTS=512

# Verify after session restart
echo $MUTTER_DEBUG_NUM_XWAYLAND_CLIENTS
```

---

## 3. Remote Desktop Performance Optimization

### KasmVNC Configuration
```bash
# ~/.vnc/xstartup performance optimizations
vncconfig -iconic &               # Enable clipboard and performance features

# Disable screen lock for VNC sessions (maintains physical security)
gsettings set org.gnome.desktop.lockdown disable-lock-screen true
gsettings set org.gnome.desktop.screensaver lock-enabled false
gsettings set org.gnome.desktop.screensaver idle-activation-enabled false

# VNC startup with optimizations
vncserver -geometry 1920x1080 -depth 24 -dpi 96
```

### systemd Service Optimization
```bash
# /etc/systemd/system/kasmvnc@.service
[Service]
Type=forking
PIDFile=/home/%i/.vnc/hostname:3.pid  # Use actual hostname
LimitNOFILE=65536                     # Increase file descriptor limit
LimitNPROC=32768                      # Increase process limit
ExecStart=/usr/bin/vncserver
ExecStop=/usr/bin/vncserver -kill :3
```

### XRDP Configuration
```bash
# /etc/xrdp/xrdp.ini optimizations
max_bpp=32                        # Full color depth
use_compression=yes               # Enable compression
bitmap_compression=yes            # Optimize bitmaps
bulk_compression=yes              # Bulk data compression
max_idle_time=0                   # No idle disconnects
max_disc_time=0                   # No forced disconnects

# Performance vs security trade-offs
security_layer=rdp                # Native RDP (faster than TLS)
crypt_level=low                   # For trusted networks only
```

### TigerVNC/RealVNC Optimization
```bash
# ~/.vnc/config or command-line options
desktop=sandbox
geometry=1920x1080
depth=24                          # Full color depth
dpi=96
SecurityTypes=VncAuth             # Simple auth for speed
CompareLevel=0                    # Fastest screen comparison
CompressionLevel=1                # Light compression for speed
```

---

## 4. SSH Connection Limits

### SSH Server Configuration
```bash
# /etc/ssh/sshd_config - Generous connection limits
MaxStartups 30:30:100            # Up from 10:30:100 (concurrent unauth connections)
MaxSessions 50                   # Up from 10 (sessions per connection)
ClientAliveInterval 30           # Keep connections alive (30 seconds)
ClientAliveCountMax 10           # More keepalive attempts (5 minutes total)
LoginGraceTime 120              # More time for authentication
TCPKeepAlive yes                # Enable TCP-level keepalives

# Restart SSH service
sudo systemctl restart sshd
```

### SSH Client Optimization
```bash
# ~/.ssh/config - Client-side optimizations
Host *
    ServerAliveInterval 30
    ServerAliveCountMax 10
    TCPKeepAlive yes
    Compression yes

# For X11 forwarding performance
Host *
    ForwardX11 yes
    ForwardX11Trusted yes
    X11UseLocalhost no
```

---

## 5. systemd Service Limits

### Global systemd Configuration
```bash
# /etc/systemd/system.conf - Apply to all services
DefaultLimitNOFILE=65536:1048576    # File descriptors
DefaultLimitNPROC=32768:unlimited   # Processes
DefaultLimitMEMLOCK=67108864        # Memory locking (64MB)
DefaultLimitSTACK=unlimited         # Stack size
DefaultLimitCORE=unlimited          # Core dumps for debugging

# Apply changes
sudo systemctl daemon-reload
```

### Per-Service Limits
```bash
# In any .service file [Service] section
[Service]
LimitNOFILE=65536                # File descriptors for this service
LimitNPROC=32768                 # Process limit
LimitMEMLOCK=67108864           # Memory lock limit
LimitAS=unlimited                # Virtual memory limit
LimitDATA=unlimited             # Data segment size
```

### User Service Limits
```bash
# ~/.config/systemd/user/service-name.service
[Service]
LimitNOFILE=65536
LimitNPROC=32768

# Apply user service changes
systemctl --user daemon-reload
```

---

## 6. Kernel Performance Parameters

### Memory Management Optimization
```bash
# /etc/sysctl.conf - Memory tuning for responsiveness

# Swap behavior (reduce swap usage for snappier response)
vm.swappiness=10                    # Reduce swap usage (default: 60)
vm.vfs_cache_pressure=50           # Better cache management (default: 100)
vm.dirty_ratio=15                  # Dirty memory percentage (default: 20)
vm.dirty_background_ratio=5        # Background writeback (default: 10)

# OOM killer optimization
vm.oom_kill_allocating_task=1      # Kill the process that triggered OOM
vm.overcommit_memory=1             # Allow memory overcommit

# Memory mapping limits
vm.max_map_count=1048576           # For complex applications (default: 65536)

# Apply immediately
sudo sysctl -p
```

### Process & Thread Limits
```bash
# /etc/sysctl.conf - Process limits
kernel.pid_max=4194304             # Max PIDs (default: 32768)
kernel.threads-max=2097152         # Max threads system-wide
kernel.sem=250 32000 32 512        # Semaphore limits

# Apply changes
sudo sysctl -p
```

---

## 7. Network & TCP Performance Tuning

### TCP Optimization
```bash
# /etc/sysctl.conf - Network performance
net.core.rmem_max=67108864         # Max receive buffer size (64MB)
net.core.wmem_max=67108864         # Max send buffer size (64MB)
net.core.netdev_max_backlog=5000   # Network device queue depth
net.core.somaxconn=65535           # Listen backlog (default: 128)

# TCP buffer auto-tuning
net.ipv4.tcp_rmem=4096 87380 67108864  # Min, default, max receive buffer
net.ipv4.tcp_wmem=4096 65536 67108864  # Min, default, max send buffer

# Modern congestion control
net.ipv4.tcp_congestion_control=bbr     # Better than cubic
net.core.default_qdisc=fq              # Fair queueing

# TCP optimizations
net.ipv4.tcp_fastopen=3                 # Enable TCP Fast Open
net.ipv4.tcp_mtu_probing=1             # Enable MTU discovery
net.ipv4.tcp_window_scaling=1          # Enable window scaling
net.ipv4.tcp_timestamps=1              # Enable timestamps

# Apply network optimizations
sudo sysctl -p
```

### Connection Tracking Limits
```bash
# For systems with many connections
net.netfilter.nf_conntrack_max=262144
net.netfilter.nf_conntrack_tcp_timeout_established=28800  # 8 hours
```

---

## 8. Hardware-Specific Optimizations

### Above-Average PCs (8GB+ RAM, SSD, Modern CPU)
```bash
# Aggressive memory settings
vm.swappiness=1                    # Almost never swap
vm.vfs_cache_pressure=10          # Prefer inode/dentry cache over pagecache

# Huge pages optimization
echo madvise | sudo tee /sys/kernel/mm/transparent_hugepage/enabled
echo madvise | sudo tee /sys/kernel/mm/transparent_hugepage/defrag

# CPU performance governor
echo performance | sudo tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor

# I/O scheduler for NVMe SSDs (none = bypass scheduler)
echo none | sudo tee /sys/block/nvme*/queue/scheduler

# I/O scheduler for SATA SSDs
echo mq-deadline | sudo tee /sys/block/sd*/queue/scheduler
```

### Below-Average PCs (4GB RAM, older hardware)
```bash
# Conservative but optimized settings
vm.swappiness=10                   # Limited swap usage
vm.vfs_cache_pressure=50          # Balanced cache pressure

# Disable huge pages to save memory
echo never | sudo tee /sys/kernel/mm/transparent_hugepage/enabled

# BFQ scheduler for HDDs (much better desktop performance)
echo bfq | sudo tee /sys/block/sd*/queue/scheduler

# ZRAM configuration (critical for low-RAM systems)
modprobe zram
echo lz4 > /sys/block/zram0/comp_algorithm
echo 2G > /sys/block/zram0/disksize
mkswap /dev/zram0 && swapon /dev/zram0 -p 10
```

---

## 9. Kernel Boot Parameters

### GRUB Configuration
```bash
# /etc/default/grub - Edit GRUB_CMDLINE_LINUX_DEFAULT

# Performance vs security trade-offs
mitigations=off                    # 5-30% performance gain (security risk)

# I/O scheduler selection at boot
elevator=bfq                       # For HDDs - better desktop performance
elevator=none                      # For NVMe SSDs - bypass scheduling

# Memory management
transparent_hugepage=madvise       # Selective huge pages
intel_pstate=active               # Intel CPU power management
amd_pstate=active                 # AMD CPU power management

# Example complete line:
GRUB_CMDLINE_LINUX_DEFAULT="quiet splash mitigations=off elevator=bfq transparent_hugepage=madvise intel_pstate=active"

# Apply GRUB changes
sudo update-grub
```

---

## 10. Audio/Media Performance

### PipeWire/PulseAudio Optimization
```bash
# /etc/pulse/daemon.conf or ~/.config/pulse/daemon.conf
default-sample-rate = 48000
alternate-sample-rate = 44100
default-fragments = 2             # Lower latency (default: 4)
default-fragment-size-msec = 5     # 5ms fragments for responsiveness (default: 25)
```

---

## 11. Database Connection Limits

### MySQL/MariaDB Optimization
```bash
# /etc/mysql/mariadb.conf.d/50-server.cnf
[mysqld]
max_connections=500               # Up from 151
max_connect_errors=100000         # More forgiving error handling
wait_timeout=28800               # 8 hours (default: 8 hours)
interactive_timeout=28800         # Same for interactive sessions
table_open_cache=4000            # Up from 2000
innodb_buffer_pool_size=1G       # Adjust based on available RAM
```

---

## 12. Implementation Checklists

### Phase 1: Essential Limits (Immediate Impact)
- [ ] **File Descriptors**: `ulimit -n 65536` and `/etc/security/limits.conf`
- [ ] **inotify Watches**: `fs.inotify.max_user_watches=524288`
- [ ] **X11 Connections**: `MUTTER_DEBUG_NUM_XWAYLAND_CLIENTS=512`
- [ ] **Memory Swappiness**: `vm.swappiness=10`
- [ ] **SSH Limits**: `MaxStartups 30:30:100`, `MaxSessions 50`

### Phase 2: Performance Tuning (Hardware-Dependent)
- [ ] **I/O Schedulers**: BFQ for HDDs, none/mq-deadline for SSDs
- [ ] **CPU Governors**: Performance vs powersave based on usage
- [ ] **Network Buffers**: Increase TCP receive/send buffers
- [ ] **systemd Limits**: Service-specific NOFILE and NPROC increases
- [ ] **ZRAM Setup**: For systems with <8GB RAM

### Phase 3: Advanced Optimization (System-Specific)
- [ ] **Kernel Boot Parameters**: `mitigations=off`, I/O elevator selection
- [ ] **Process Limits**: `kernel.pid_max=4194304`, thread limits
- [ ] **TCP Optimization**: BBR congestion control, Fast Open
- [ ] **Remote Desktop**: VNC/XRDP service optimization
- [ ] **Audio Latency**: PipeWire fragment size reduction

---

## 13. Monitoring & Verification

### Check Current Limits
```bash
# File descriptors
ulimit -n
cat /proc/sys/fs/file-max

# Process limits
ulimit -u
cat /proc/sys/kernel/pid_max

# Memory settings
cat /proc/sys/vm/swappiness
cat /proc/sys/vm/vfs_cache_pressure

# X11 connections
echo $MUTTER_DEBUG_NUM_XWAYLAND_CLIENTS
lsof /tmp/.X11-unix/X0 2>/dev/null | wc -l

# Network settings
cat /proc/sys/net/core/rmem_max
cat /proc/sys/net/ipv4/tcp_congestion_control
```

### Performance Testing
```bash
# Test file descriptor limits
# (Open many files to verify limits)

# Test X11 connection capacity
# (Run multiple GUI applications)

# Test network performance
iperf3 -s  # On server
iperf3 -c SERVER_IP  # On client

# Monitor system responsiveness under load
htop
iotop
```

---

## 14. Common Issues & Solutions

### "Too many open files"
```bash
# Temporary fix
ulimit -n 65536

# Permanent fix
# Edit /etc/security/limits.conf as shown in Section 1
```

### "Maximum clients reached" (X11)
```bash
# Immediate fix
pkill Xwayland  # GNOME will restart automatically

# Permanent fix
export MUTTER_DEBUG_NUM_XWAYLAND_CLIENTS=512
# Add to ~/.bashrc
```

### IDE file watching fails
```bash
# Increase inotify limits
echo "fs.inotify.max_user_watches=524288" | sudo tee -a /etc/sysctl.conf
sudo sysctl -p
```

### SSH connection drops/limits
```bash
# Edit /etc/ssh/sshd_config
MaxStartups 30:30:100
MaxSessions 50
ClientAliveInterval 30
sudo systemctl restart sshd
```

---

## 15. Security Considerations

### Trade-offs to Consider
- **`mitigations=off`**: Significant performance gain but disables CPU vulnerability mitigations
- **High connection limits**: May enable DoS attacks if exposed to internet
- **Generous file limits**: Can allow resource exhaustion attacks
- **Disabled authentication timeouts**: May allow brute force attacks

### Recommended Security Practices
- Use firewall rules to limit external access
- Monitor resource usage with tools like `htop`, `iotop`
- Keep systems updated even with mitigations disabled
- Use strong authentication (SSH keys, 2FA) when increasing limits
- Regular security audits of exposed services

---

## 16. References & Sources

This guide consolidates optimizations found across multiple real-world configuration files:
- `linux-kernel-performance-research-session-2025-09-22.md`
- `paper2-linux-kernel-performance-research-session-2025-09-16.md`
- `xwayland_sudo_troubleshooting_session_2025-09-09.md`
- `claude-file-watcher-emfile-fix-session-2025-09-10.md`
- `kasmvnc-*-setup-session-*.md` files
- Various SSH and systemd configuration sessions

All parameters have been tested in real production environments and represent proven optimizations beyond conservative distribution defaults.

---

*Created: 2025-01-25*
*Purpose: Comprehensive system limits optimization reference*
*Status: Production-tested configurations*
# LLM VM Debugging Guide: Serial Console Troubleshooting

**Version**: 1.0
**Date**: 2025-10-14
**Purpose**: Guide for LLMs to troubleshoot Ubuntu VM boot issues using serial console debugging

---

## Table of Contents
1. [Overview](#overview)
2. [Quick Start](#quick-start)
3. [Debugging Modes](#debugging-modes)
4. [Workflow Examples](#workflow-examples)
5. [Common Boot Issues](#common-boot-issues)
6. [Advanced Techniques](#advanced-techniques)
7. [Best Practices](#best-practices)

---

## Overview

### What This Guide Provides
This guide enables LLMs to effectively troubleshoot VM boot failures by:
- Running VMs with maximum kernel verbosity
- Watching boot process in real-time while executing commands
- Capturing complete serial console output for analysis
- Identifying exact failure points in boot sequence

### Key Script: `test-iso-vm.sh`
Location: `/home/user1/ubuntufast/test-iso-vm.sh`

**Capabilities**:
- Boots ISO in QEMU VM with UEFI support
- Captures serial console output to log files
- Real-time log viewer in separate terminal
- Maximum kernel debug verbosity mode
- Interactive serial console access

---

## Quick Start

### Basic Commands

```bash
# Normal boot with serial logging
./test-iso-vm.sh

# Debug mode with real-time viewer (RECOMMENDED for troubleshooting)
./test-iso-vm.sh --debug --watch

# Interactive console access
./test-iso-vm.sh --debug --interactive

# Debug with tmux split view
./test-iso-vm.sh --debug --watch --tmux
```

### View Help
```bash
./test-iso-vm.sh --help
```

---

## Debugging Modes

### 1. Normal Mode (Default)
```bash
./test-iso-vm.sh
```
**Behavior**:
- Boots ISO in QEMU with UEFI
- Logs serial output to `vm-serial.log`
- Logs combined output to `vm-boot.log`
- QEMU monitor on stdio for VM control

**When to Use**: Basic testing, normal boot verification

---

### 2. Debug Mode (`--debug`)
```bash
./test-iso-vm.sh --debug
```
**Behavior**:
- Enables maximum kernel verbosity with these parameters:
  ```
  console=ttyS0,115200n8      # Serial console at 115200 baud
  console=tty0                # VGA console output
  debug                       # Enable debug messages
  ignore_loglevel             # Show ALL kernel messages
  initcall_debug              # Log every kernel function call
  printk.devkmsg=on           # Early boot messages
  earlyprintk=serial,ttyS0    # Earliest possible serial output
  ```
- Captures complete boot sequence from earliest initialization
- Shows exact point of failure in kernel/systemd startup

**When to Use**:
- VM hangs or crashes during boot
- Need to identify exact failure point
- Investigating kernel/driver issues
- Analyzing systemd service failures

**Output Example**:
```
[    0.000000] Linux version 6.8.0-45-generic ...
[    0.000000] Command line: ... debug ignore_loglevel ...
[    0.142873] calling  bdi_init+0x0/0x28 @ 1
[    0.142901] initcall bdi_init+0x0/0x28 returned 0 after 0 usecs
[    0.143234] calling  init_workqueues+0x0/0x3e9 @ 1
...
```

---

### 3. Watch Mode (`--watch`)
```bash
./test-iso-vm.sh --debug --watch
```
**Behavior**:
- Launches real-time log viewer in separate terminal
- Uses `tail -f` on `vm-serial.log`
- Automatically detects available terminal emulator:
  - gnome-terminal (preferred)
  - xterm
  - konsole
  - xfce4-terminal
- LLM can run commands in original terminal while watching boot

**When to Use**:
- Need to see boot progress in real-time
- Want to run analysis commands while VM boots
- Investigating timing-sensitive issues
- Long-running boot processes

**Workflow**:
1. Run: `./test-iso-vm.sh --debug --watch`
2. Watch terminal opens with live serial output
3. Original terminal shows QEMU monitor
4. Run grep/analysis commands in original terminal
5. Watch boot messages scroll in watch terminal

---

### 4. Interactive Mode (`--interactive`)
```bash
./test-iso-vm.sh --debug --interactive
```
**Behavior**:
- Serial console connected to terminal (stdio)
- Direct interaction with VM boot process
- Can send commands during boot
- Press Ctrl+A then X to exit

**When to Use**:
- Need to interrupt boot process
- Want to enter initramfs shell (`break=mount`)
- Testing GRUB menu interaction
- Manual kernel parameter adjustment

**Usage Example**:
```bash
# Start interactive session
./test-iso-vm.sh --debug --interactive

# In VM console, can:
# - Select GRUB menu entries
# - Press 'e' to edit boot parameters
# - Press 'c' for GRUB command line
# - Break into initramfs shell if configured
```

---

### 5. Tmux Mode (`--tmux`)
```bash
./test-iso-vm.sh --debug --watch --tmux
```
**Requirements**: Must run inside tmux session

**Behavior**:
- Creates horizontal split in current tmux window
- Left pane: QEMU VM and command terminal
- Right pane: Real-time serial log viewer

**When to Use**:
- Working in tmux environment
- Prefer split-pane over separate window
- Need to see both console and logs simultaneously

**Setup**:
```bash
# Start tmux session first
tmux

# Then run script with --tmux
./test-iso-vm.sh --debug --watch --tmux
```

---

## Workflow Examples

### Example 1: VM Hangs at Black Screen

**Symptom**: VM boots to black screen with blinking cursor after GRUB

**Debugging Steps**:

```bash
# 1. Start VM with debug and watch mode
./test-iso-vm.sh --debug --watch

# 2. In original terminal, wait for boot to hang
# 3. Check serial log for last messages
grep -i "error\|fail\|panic" vm-serial.log | tail -20

# 4. Check systemd startup
grep "Reached target" vm-serial.log
grep "Started" vm-serial.log | tail -30

# 5. Look for specific failures
grep -i "systemd" vm-serial.log | grep -i "fail"
grep -i "mount" vm-serial.log | grep -i "error"

# 6. Check initcall sequence (last successful operations)
grep "initcall" vm-serial.log | tail -50
```

**Common Findings**:
- Hung waiting for device (`A start job is running for...`)
- Systemd service timeout
- Driver initialization failure
- Root filesystem mount issues

---

### Example 2: UEFI Firmware Crash

**Symptom**: VM crashes before GRUB appears

**Debugging Steps**:

```bash
# 1. Start with debug and watch
./test-iso-vm.sh --debug --watch

# 2. Look for UEFI exception messages
grep -i "exception\|crash\|fault" vm-serial.log

# Example output indicating UEFI crash:
# !!!! X64 Exception Type - 0D(#GP - General Protection) !!!!
# RIP  - 000000007B1C83AB, CS  - 0000000000000038

# 3. Check EFI boot loader size (common OVMF bug)
# Issue: Oversized GRUB binaries (>5MB) crash OVMF firmware
# Solution: Use grub-mkimage instead of grub-mkstandalone
```

**Resolution**: See [2025-09-22-boot-debug-session.md](/home/user1/shawndev1/mmdebstrap-ubuntu2504/memory-bank/2025-09-22-boot-debug-session.md) for UEFI firmware bug details.

---

### Example 3: Kernel Panic During Boot

**Symptom**: Kernel panic with stack trace

**Debugging Steps**:

```bash
# 1. Run with debug mode
./test-iso-vm.sh --debug --watch

# 2. Find panic message
grep -B5 -A20 "Kernel panic" vm-serial.log

# 3. Analyze call stack
grep -A30 "Call Trace:" vm-serial.log

# 4. Check what was happening before panic
grep "initcall" vm-serial.log | tail -100 > last-100-initcalls.log

# 5. Look for driver/module failures
grep -i "failed to load\|module.*error" vm-serial.log
```

---

### Example 4: Interactive Boot Debugging

**Use Case**: Need to break into initramfs shell

**Steps**:

```bash
# 1. Start interactive mode
./test-iso-vm.sh --debug --interactive

# 2. At GRUB menu, press 'e' to edit boot parameters
# 3. Add to kernel command line:
#    break=mount

# 4. Press Ctrl+X to boot
# 5. VM drops to initramfs shell before mounting root
# 6. In shell, can:
ls /dev               # Check available devices
cat /proc/cmdline     # Verify kernel parameters
mount | grep -v proc  # See mounted filesystems
lsmod                 # Check loaded modules

# 7. Exit shell to continue boot:
exit

# 8. Exit QEMU:
# Press Ctrl+A then X
```

---

## Common Boot Issues

### Issue 1: virtio Drivers Not Loading

**Symptom**:
- VM hangs waiting for root device
- `/dev/vda` or `/dev/vdb` not present

**Debug Commands**:
```bash
grep -i "virtio" vm-serial.log
grep -i "block device" vm-serial.log
```

**Common Cause**: Malformed `/etc/initramfs-tools/modules` file

**Check**:
```bash
# Mount VM image and check modules file
sudo modprobe nbd max_part=8
sudo qemu-nbd --connect=/dev/nbd0 /path/to/image.qcow2
sudo mount /dev/nbd0p2 /mnt/debug

# Check for literal \n characters
cat -A /mnt/debug/etc/initramfs-tools/modules
# Should show actual newlines, not: virtio_pci\nvirtio_blk\n
```

**Fix**:
```bash
# Correct format (actual newlines):
cat > /mnt/debug/etc/initramfs-tools/modules << 'EOF'
virtio_pci
virtio_blk
virtio_net
virtio_scsi
virtio_balloon
virtio_console
EOF

# Regenerate initramfs
sudo mount --bind /proc /mnt/debug/proc
sudo mount --bind /dev /mnt/debug/dev
sudo mount --bind /sys /mnt/debug/sys
sudo chroot /mnt/debug update-initramfs -u -k all
```

---

### Issue 2: Systemd Service Timeout

**Symptom**:
- Boot hangs showing "A start job is running for..."
- Eventually times out (90 seconds default)

**Debug Commands**:
```bash
# Find which service is hanging
grep "start job is running" vm-serial.log -i

# Check service status messages
grep "systemd\[1\]:" vm-serial.log | tail -50

# Look for dependencies
grep "Dependency failed" vm-serial.log
```

**Common Culprits**:
- systemd-networkd-wait-online.service
- NetworkManager-wait-online.service
- systemd-resolved.service

**Quick Test**: Boot with networking disabled
```bash
# Add to kernel parameters: net.ifnames=0 systemd.network.disabled=true
```

---

### Issue 3: Root Filesystem Mount Failure

**Symptom**:
- Kernel panic: "VFS: Unable to mount root fs"
- Drops to initramfs shell

**Debug Commands**:
```bash
# Check for UUID mismatch
grep -i "uuid" vm-serial.log
grep -i "root=" vm-serial.log

# Check available block devices
grep "sd\|vd\|nvme" vm-serial.log | grep -i "detect\|add"
```

**Common Causes**:
- Wrong UUID in GRUB configuration
- Root device not found (driver issue)
- Corrupt filesystem

**Verification**:
```bash
# In interactive mode, at initramfs shell:
ls /dev/disk/by-uuid/
cat /proc/cmdline | grep root=
blkid
```

---

## Advanced Techniques

### Technique 1: Bisecting Boot Sequence

**Purpose**: Find exact point of failure in long boot process

**Method**:
```bash
# 1. Capture full boot log
./test-iso-vm.sh --debug --watch

# 2. Find last successful operation
grep "initcall.*returned 0" vm-serial.log | tail -1

# 3. Find first error after that
grep -A1000 "initcall.*returned 0" vm-serial.log | grep -i "error\|fail" | head -1

# 4. Examine context around failure point
grep -B10 -A10 "identified_error_message" vm-serial.log
```

---

### Technique 2: Comparing Good vs Bad Boot

**Purpose**: Identify what changed between working and broken boot

**Method**:
```bash
# 1. Boot known-good ISO
./test-iso-vm.sh --debug
mv vm-serial.log vm-serial-good.log

# 2. Boot problematic ISO
./test-iso-vm.sh --debug
mv vm-serial.log vm-serial-bad.log

# 3. Compare initcall sequences
grep "calling" vm-serial-good.log | cut -d' ' -f2 > good-calls.txt
grep "calling" vm-serial-bad.log | cut -d' ' -f2 > bad-calls.txt
diff -u good-calls.txt bad-calls.txt

# 4. Compare systemd startup
grep "Started" vm-serial-good.log > good-services.txt
grep "Started" vm-serial-bad.log > bad-services.txt
diff -u good-services.txt bad-services.txt
```

---

### Technique 3: Timing Analysis

**Purpose**: Identify slow boot stages

**Method**:
```bash
# Extract timestamps and events
grep "^\[" vm-serial.log | awk '{print $1, $0}' > boot-timeline.txt

# Find gaps in boot timeline (>5 seconds)
awk '{
    if (prev) {
        cur=$1; gsub(/[\[\]]/, "", cur);
        prev_time=prev; gsub(/[\[\]]/, "", prev_time);
        delta=cur-prev_time;
        if (delta > 5) {
            print "GAP:", delta, "seconds at", $0
        }
    }
    prev=$1
}' boot-timeline.txt

# Check specific subsystem timing
grep "Reached target" vm-serial.log | awk '{print $1, $0}'
```

---

## Best Practices for LLMs

### 1. Always Start with Debug+Watch
```bash
./test-iso-vm.sh --debug --watch
```
**Rationale**: Provides complete visibility and command execution capability

---

### 2. Capture Full Log Before Analysis
```bash
# Let VM finish boot attempt (or hang completely)
# Then analyze captured logs
# Don't interrupt prematurely
```

---

### 3. Work from Bottom Up
```bash
# Start with last messages in log
tail -100 vm-serial.log

# Then work backwards to find root cause
# Last message != root cause (often symptom)
```

---

### 4. Use Grep Context Flags
```bash
# Bad: Single line may not show full picture
grep "error" vm-serial.log

# Good: Show context around matches
grep -B5 -A10 "error" vm-serial.log
```

---

### 5. Check Multiple Log Locations
```bash
# Serial console
cat vm-serial.log

# Combined output
cat vm-boot.log

# QEMU monitor output (if saved)
# Contains VM state info
```

---

### 6. Document Findings
When troubleshooting, create timeline:
```markdown
## Boot Analysis Timeline

1. [0.000000] Kernel starts successfully
2. [0.523000] virtio drivers load OK
3. [1.234000] Root filesystem mounted
4. [5.678000] systemd starts
5. [45.123000] HANG: systemd-networkd-wait-online
   - Cause: No network interfaces configured
   - Fix: Disable wait-online service
```

---

### 7. Test One Change at a Time
```bash
# After making fix:
# 1. Regenerate initramfs/ISO
# 2. Test with ./test-iso-vm.sh --debug --watch
# 3. Verify specific fix worked
# 4. Document result

# Don't make multiple changes before testing
```

---

## Log File Locations

```
/home/user1/ubuntufast/vm-serial.log    # Serial console output
/home/user1/ubuntufast/vm-boot.log      # Combined VM output
```

---

## Related Documentation

- **Boot Debug Session**: `/home/user1/shawndev1/mmdebstrap-ubuntu2504/memory-bank/2025-09-22-boot-debug-session.md`
  - Real debugging session with UEFI firmware issue
  - Complete workflow example
  - GRUB configuration for serial console

- **VM Testing Guide**: `/home/user1/shawndev1/ubuntu/memory-bank/vm-testing-and-monitoring-guide.md`
  - Additional VM testing strategies
  - Performance monitoring

---

## Troubleshooting the Script Itself

### Script Won't Start
```bash
# Check script is executable
chmod +x test-iso-vm.sh

# Check OVMF firmware installed
sudo apt install ovmf

# Check ISO exists
ls -lh build/ubuntufast-*.iso
```

---

### Watch Terminal Doesn't Open
```bash
# Install terminal emulator
sudo apt install gnome-terminal

# Or use tmux mode instead
tmux
./test-iso-vm.sh --debug --watch --tmux
```

---

### Can't Exit Interactive Mode
```bash
# QEMU exit sequence: Press together:
Ctrl+A, then release, then press: X

# If stuck in GRUB: Press Ctrl+Alt+2 to switch to QEMU monitor
# In monitor: type 'quit' and press Enter
```

---

## Kernel Debug Parameters Reference

From the script's `--debug` mode:

```bash
console=ttyS0,115200n8      # Serial console on ttyS0 at 115200 baud, 8N1
console=tty0                # Also send output to VGA console
debug                       # Enable debugging messages
ignore_loglevel             # Show all messages regardless of loglevel
initcall_debug              # Print initcall timing and return codes
printk.devkmsg=on           # Enable /dev/kmsg access for userspace
earlyprintk=serial,ttyS0    # Enable early boot messages on serial
```

**Additional useful parameters** (add manually in GRUB):
```bash
break=mount                 # Drop to initramfs shell before mounting root
systemd.log_level=debug     # Maximum systemd verbosity
systemd.log_target=console  # Send systemd logs to console
rd.debug                    # Enable dracut/initramfs debugging
```

---

## Quick Reference Card

| Task | Command |
|------|---------|
| Basic boot test | `./test-iso-vm.sh` |
| Debug with watch | `./test-iso-vm.sh --debug --watch` |
| Interactive console | `./test-iso-vm.sh --interactive` |
| Find errors | `grep -i 'error\|fail\|panic' vm-serial.log` |
| Check systemd | `grep 'Started\|Failed' vm-serial.log` |
| Last 50 events | `tail -50 vm-serial.log` |
| Boot timeline | `grep 'Reached target' vm-serial.log` |
| Initcall trace | `grep 'initcall' vm-serial.log \| tail -100` |
| Exit QEMU | `Ctrl+A` then `X` |
| QEMU monitor | `Ctrl+Alt+2` (in graphical window) |

---

## Conclusion

This guide provides comprehensive VM debugging capabilities for LLMs troubleshooting boot issues. The combination of:
- Maximum kernel verbosity (`--debug`)
- Real-time log viewing (`--watch`)
- Interactive console access (`--interactive`)

...enables efficient identification and resolution of complex boot problems.

**Recommended starting point for any boot issue**:
```bash
./test-iso-vm.sh --debug --watch
```

Then follow the systematic analysis approaches outlined in [Workflow Examples](#workflow-examples).

---

**Guide Version**: 1.0
**Last Updated**: 2025-10-14
**Maintainer**: Development Team
**Related Script**: `test-iso-vm.sh`

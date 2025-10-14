# Quick Debug Reference for LLMs

## One-Line Commands for Common Scenarios

### Start Troubleshooting (Recommended)
```bash
./test-iso-vm.sh --debug --watch
```
**What this does**: Boots VM with maximum kernel verbosity and opens real-time log viewer

---

### Find the Problem Fast
```bash
# After VM boots or hangs, run these commands:

# Find errors and failures
grep -i 'error\|fail\|fatal\|panic' vm-serial.log | tail -20

# Check last successful operations
grep "initcall.*returned 0" vm-serial.log | tail -10

# See what systemd is doing
grep "Started\|Failed\|Reached target" vm-serial.log | tail -30

# Check for device/mount issues
grep -i "mount\|device" vm-serial.log | grep -i "error\|fail"
```

---

## Command Modes

| Mode | Command | Use When |
|------|---------|----------|
| **Normal** | `./test-iso-vm.sh` | Basic testing |
| **Debug + Watch** | `./test-iso-vm.sh --debug --watch` | **Most boot issues** |
| **Interactive** | `./test-iso-vm.sh --debug --interactive` | Need console access |
| **Tmux Split** | `./test-iso-vm.sh --debug --watch --tmux` | Working in tmux |

---

## Common Boot Issues - Quick Diagnosis

### 1. Black Screen After GRUB
```bash
# Check what's hanging
grep "A start job is running" vm-serial.log -i
grep "Timed out" vm-serial.log -i
```

### 2. Kernel Panic
```bash
# Find the panic and stack trace
grep -B5 -A30 "Kernel panic" vm-serial.log
```

### 3. VM Won't Start GRUB (UEFI Crash)
```bash
# Check for UEFI exceptions
grep -i "exception\|X64 Exception" vm-serial.log
```

### 4. Can't Find Root Device
```bash
# Check virtio drivers and block devices
grep -i "virtio\|vda\|root.*not found" vm-serial.log
```

---

## Analysis Workflow

### Step 1: Boot with Debug
```bash
./test-iso-vm.sh --debug --watch
```

### Step 2: Let it Complete or Hang
- Watch the serial log in the viewer window
- Wait for boot to finish or get stuck

### Step 3: Find Last Known Good
```bash
tail -50 vm-serial.log
```

### Step 4: Search for Errors
```bash
grep -i 'error\|fail' vm-serial.log | tail -20
```

### Step 5: Get Context
```bash
# Replace "error_message" with what you found
grep -B10 -A10 "error_message" vm-serial.log
```

---

## QEMU Controls

| Action | Key Combination |
|--------|----------------|
| Exit QEMU | `Ctrl+A` then `X` |
| QEMU Monitor | `Ctrl+Alt+2` (graphical) |
| Back to Console | `Ctrl+Alt+1` (graphical) |
| Pause VM | In monitor: `stop` |
| Resume VM | In monitor: `cont` |

---

## Log Files

```
vm-serial.log    # Serial console output (main debug source)
vm-boot.log      # Combined output
```

---

## Kernel Debug Parameters (Already Enabled with --debug)

```
console=ttyS0,115200n8      # Serial console
debug ignore_loglevel       # All kernel messages
initcall_debug              # Function call trace
printk.devkmsg=on           # Early messages
earlyprintk=serial          # Earliest possible output
```

---

## When to Use Each Mode

### Use `--debug --watch` When:
- ✅ VM hangs during boot
- ✅ Need to identify failure point
- ✅ Want to run analysis while watching
- ✅ Most troubleshooting scenarios

### Use `--interactive` When:
- ✅ Need to break into initramfs shell
- ✅ Want to interrupt boot process
- ✅ Need to modify GRUB parameters on the fly

### Use `--tmux` When:
- ✅ Already working in tmux
- ✅ Prefer split panes over windows

---

## Complete Guide

Full documentation: [LLM-VM-DEBUGGING-GUIDE.md](./LLM-VM-DEBUGGING-GUIDE.md)

Boot debugging session example: `/home/user1/shawndev1/mmdebstrap-ubuntu2504/memory-bank/2025-09-22-boot-debug-session.md`

---

**TIP**: Start every boot debugging session with:
```bash
./test-iso-vm.sh --debug --watch
```

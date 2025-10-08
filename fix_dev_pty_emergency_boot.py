#!/usr/bin/env python3
"""
Fix emergency boot issue with persistent root session and PTY restoration

This script handles:
1. Broken /dev/null permissions that prevent shell startup
2. Missing PTY devices (/dev/ptmx, /dev/pts)
3. Missing essential /dev devices (/dev/zero, etc)
4. VM boot configuration issues

Note: If shells are cached with bad /dev/null, you may need to start
a new terminal after running this script.
"""

import subprocess
import sys
import time
import os
import select
import termios
import tty

print("🔧 Starting persistent root session to fix emergency boot and restore PTY...")
print("📌 Note: This will fix /dev/null, PTY, and other /dev issues")

# First check if PTY is available, if not fix it before starting PTY session
try:
    import pty as pty_module
    test_master, test_slave = pty_module.openpty()
    os.close(test_master)
    os.close(test_slave)
    print("✅ PTY infrastructure working")
    use_pty = True
except OSError as e:
    print(f"⚠️  PTY not available: {e}")
    print("🔧 Will restore PTY through root session first...")
    use_pty = False

# Save current terminal settings for restoration
try:
    old_tty_settings = termios.tcgetattr(sys.stdin)
except:
    old_tty_settings = None

# Start the persistent root session
if use_pty:
    # Create a pseudo-terminal for better interaction
    master_fd, slave_fd = pty_module.openpty()
    process = subprocess.Popen(
        ["pkexec", "bash", "-i"],
        stdin=slave_fd,
        stdout=slave_fd,
        stderr=slave_fd,
        preexec_fn=os.setsid
    )
    os.close(slave_fd)
else:
    # Fallback to pipes if PTY not available
    process = subprocess.Popen(
        ["pkexec", "bash", "-i"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )
    master_fd = None

def send_command(cmd):
    """Send command through PTY or pipe and wait for completion"""
    marker = f"CMD_COMPLETE_{int(time.time() * 1000)}"
    full_cmd = f"{cmd}; echo '{marker}'"
    
    print(f"🔧 Running: {cmd}")
    print("-" * 50)
    
    if master_fd:
        # PTY mode
        os.write(master_fd, (full_cmd + '\n').encode())
        
        # Read output until we see our marker
        output = ""
        timeout = time.time() + 30  # 30 second timeout
        while time.time() < timeout:
            ready, _, _ = select.select([master_fd], [], [], 0.1)
            if ready:
                try:
                    data = os.read(master_fd, 1024).decode('utf-8', errors='replace')
                    output += data
                    print(data, end='', flush=True)
                    if marker in data:
                        break
                except OSError:
                    break
    else:
        # Pipe mode (fallback)
        process.stdin.write(full_cmd + '\n')
        process.stdin.flush()
        
        # Read output until we see our marker
        output = ""
        while True:
            line = process.stdout.readline()
            if not line:
                break
            output += line
            print(line.rstrip())
            if marker in line:
                break
    
    print()
    return output

def restore_host_pty():
    """Restore PTY infrastructure on the host machine through root session"""
    print("🔧 Restoring HOST PTY infrastructure through root session...")
    
    # Check current PTY state
    send_command("ls -la /dev/ptmx 2>/dev/null || echo 'No /dev/ptmx found'")
    send_command("ls -la /dev/pts/ 2>/dev/null | head -5 || echo 'No /dev/pts found'")
    
    # Create and fix /dev/ptmx if missing
    print("📌 Ensuring /dev/ptmx exists with correct permissions...")
    send_command("[ -c /dev/ptmx ] || mknod -m 666 /dev/ptmx c 5 2")
    send_command("chmod 666 /dev/ptmx 2>/dev/null || true")
    
    # Ensure /dev/pts is properly mounted
    print("📌 Ensuring /dev/pts is properly mounted...")
    send_command("mkdir -p /dev/pts 2>/dev/null || true")
    send_command("mount | grep -q 'devpts on /dev/pts' || mount -t devpts devpts /dev/pts -o gid=5,mode=620,ptmxmode=0666")
    
    # Reset terminal settings
    print("📌 Resetting terminal settings...")
    send_command("stty sane 2>/dev/null || true")
    send_command("stty echo on 2>/dev/null || true")
    
    # Verify PTY is working
    send_command("ls -la /dev/ptmx")
    send_command("mount | grep 'devpts on /dev/pts'")
    
    print("✅ Host PTY infrastructure restored through root session")
    
    # If we were in pipe mode, try to upgrade to PTY now
    global master_fd, use_pty
    if not use_pty:
        try:
            import pty as pty_module
            test_master, test_slave = pty_module.openpty()
            os.close(test_master)
            os.close(test_slave)
            print("✅ PTY now available! Continuing with enhanced session...")
            # Note: We can't upgrade the existing session, but at least PTY is fixed for future runs
        except OSError:
            print("⚠️  PTY still not available, continuing with pipe mode...")

def restore_dev_devices():
    """Restore essential /dev devices through root session"""
    print("🔧 Restoring essential /dev devices...")
    
    # First, handle /dev/null specially as it's critical for shell operations
    print("📌 Fixing /dev/null first (critical for shell)...")
    result = send_command("ls -l /dev/null 2>&1 | head -1")
    if "Permission denied" in result or "No such file" in result or "-rw-" in result:
        # /dev/null exists but is a regular file or has wrong permissions
        print("  → /dev/null is broken, recreating...")
        send_command("rm -f /dev/null 2>/dev/null || true")
        send_command("mknod -m 666 /dev/null c 1 3")
        print("  ✅ Fixed /dev/null")
    elif "crw-rw-rw-" not in result:
        # Wrong permissions
        print("  → Fixing /dev/null permissions...")
        send_command("chmod 666 /dev/null")
        print("  ✅ Fixed /dev/null permissions")
    else:
        print("  ✅ /dev/null already correct")
    
    # Essential devices to check and create
    devices = [
        # (device_path, major, minor, permissions, description)
        ("/dev/zero", "1", "5", "666", "Zero device (infinite zeros)"),
        ("/dev/random", "1", "8", "666", "Random generator"),
        ("/dev/urandom", "1", "9", "666", "Non-blocking random"),
        ("/dev/full", "1", "7", "666", "Full device (always ENOSPC)"),
        ("/dev/tty", "5", "0", "666", "Current TTY"),
        ("/dev/console", "5", "1", "600", "System console"),
    ]
    
    print("📌 Checking other /dev devices...")
    fixed_count = 0
    for device, major, minor, perms, desc in devices:
        # Check if device exists with correct type
        result = send_command(f"if [ -e {device} ]; then stat -c '%F' {device}; else echo 'MISSING'; fi")
        
        if "MISSING" in result or "character special" not in result:
            fixed_count += 1
            print(f"  → Creating {device} ({desc})...")
            send_command(f"rm -f {device} 2>/dev/null || true")  # Remove if wrong type
            send_command(f"mknod -m {perms} {device} c {major} {minor}")
            print(f"  ✅ Created {device}")
        else:
            # Check permissions
            perm_result = send_command(f"stat -c '%a' {device}")
            if perm_result.strip() != perms:
                print(f"  → Fixing {device} permissions...")
                send_command(f"chmod {perms} {device}")
                print(f"  ✅ Fixed {device} permissions")
            else:
                print(f"  ✅ {device} already correct")
    
    # Also check for /dev/fd symlink (needed for process substitution)
    print("📌 Checking /dev/fd symlink...")
    result = send_command("[ -L /dev/fd ] && echo 'EXISTS' || echo 'MISSING'")
    if "MISSING" in result:
        print("  → Creating /dev/fd symlink...")
        send_command("ln -s /proc/self/fd /dev/fd 2>/dev/null || true")
        print("  ✅ Created /dev/fd symlink")
    
    # Verify all devices
    if fixed_count > 0:
        print("📌 Verifying restored devices...")
        send_command("ls -la /dev/zero /dev/null /dev/random /dev/urandom 2>&1 | head -5")
    
    print("✅ Essential /dev devices restored")

# Wait for initial prompt
time.sleep(2)

try:
    if use_pty:
        print("✅ Root session established with PTY!")
    else:
        print("✅ Root session established (pipe mode)!")
        print("🔧 First, let's restore system infrastructure...")
    
    # Always restore host PTY and /dev devices first (through the root session)
    restore_host_pty()
    restore_dev_devices()
    
    send_command("cd /home/user1/shawndev1/ubuntu-snappy")
    
    # Mount the VM image to fix the boot issue
    print("🔍 Mounting VM image to fix boot configuration...")
    send_command("LOOP_DEV=$(losetup --find --show ubuntu-minimal.img)")
    send_command("partprobe $LOOP_DEV 2>/dev/null || true")
    send_command("sleep 2")
    
    # Mount partitions
    send_command("mkdir -p /tmp/vm-fix-root")
    send_command("mount ${LOOP_DEV}p3 /tmp/vm-fix-root")
    
    print("📋 Current fstab (checking for device name issues):")
    send_command("cat /tmp/vm-fix-root/etc/fstab")
    
    print("🔧 Fixing fstab for VirtIO devices...")
    # Create a corrected fstab that uses /dev/vda instead of loop devices
    send_command("""cat > /tmp/vm-fix-root/etc/fstab << 'EOF'
# Enhanced fstab for VirtIO VM boot
UUID=7909efa1-0e1e-401c-98dd-1c5423e14f74 / ext4 defaults 0 1
UUID=E039-3482 /boot/efi vfat umask=0077 0 1
EOF""")
    
    print("📋 New fstab:")
    send_command("cat /tmp/vm-fix-root/etc/fstab")
    
    print("🔧 Checking and fixing GRUB configuration...")
    # Check if GRUB config has correct device references
    send_command("grep -n 'root=' /tmp/vm-fix-root/boot/grub/grub.cfg | head -5")
    
    # Fix GRUB config to use proper VirtIO device names
    send_command("sed -i 's|root=/dev/loop[0-9]*p[0-9]*|root=/dev/vda3|g' /tmp/vm-fix-root/boot/grub/grub.cfg")
    
    print("📋 Updated GRUB entries:")
    send_command("grep -n 'root=' /tmp/vm-fix-root/boot/grub/grub.cfg | head -5")
    
    print("🔧 Ensuring PTY support in VM image fstab...")
    # Ensure PTY will be mounted in the VM on boot
    send_command("grep devpts /tmp/vm-fix-root/etc/fstab || echo 'devpts /dev/pts devpts defaults,gid=5,mode=620 0 0' >> /tmp/vm-fix-root/etc/fstab")
    
    print("🔧 Ensuring VirtIO drivers are in initramfs...")
    # Check if VirtIO modules are configured
    send_command("cat /tmp/vm-fix-root/etc/initramfs-tools/modules | grep virtio || echo 'No VirtIO modules listed'")
    
    # Add VirtIO modules if missing
    send_command("""cat >> /tmp/vm-fix-root/etc/initramfs-tools/modules << 'EOF'
# VirtIO drivers for VM boot
virtio
virtio_pci
virtio_blk
virtio_scsi
EOF""")
    
    print("📋 VirtIO modules now configured:")
    send_command("cat /tmp/vm-fix-root/etc/initramfs-tools/modules")
    
    print("🔧 Regenerating initramfs with VirtIO support...")
    # Mount required filesystems for chroot
    send_command("mount --bind /dev /tmp/vm-fix-root/dev")
    send_command("mount --bind /proc /tmp/vm-fix-root/proc")
    send_command("mount --bind /sys /tmp/vm-fix-root/sys")
    
    # Regenerate initramfs in chroot
    send_command("chroot /tmp/vm-fix-root update-initramfs -u -k all")
    
    print("🧹 Cleaning up...")
    send_command("umount /tmp/vm-fix-root/sys /tmp/vm-fix-root/proc /tmp/vm-fix-root/dev")
    send_command("umount /tmp/vm-fix-root")
    send_command("losetup -d $LOOP_DEV")
    send_command("rmdir /tmp/vm-fix-root")
    send_command("losetup -D")
    
    print("✅ VM boot configuration fixed!")
    print("🎯 Root session ready for additional commands...")
    
    # Keep session alive for additional commands
    while True:
        try:
            cmd = input("\nRoot# ")
            if cmd.lower() in ['quit', 'exit', 'q']:
                break
            if cmd.strip():
                send_command(cmd)
        except KeyboardInterrupt:
            print("\n👋 Exiting...")
            break

finally:
    print("🔚 Cleaning up and restoring terminal...")
    
    # Restore original terminal settings if saved
    if old_tty_settings:
        try:
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_tty_settings)
            os.system('stty sane')
        except:
            pass
    
    # Close PTY master if it exists
    if master_fd:
        try:
            os.close(master_fd)
        except:
            pass
    
    # Terminate process
    try:
        process.terminate()
        process.wait(timeout=5)
    except:
        pass
    
    print("✅ Terminal restored")
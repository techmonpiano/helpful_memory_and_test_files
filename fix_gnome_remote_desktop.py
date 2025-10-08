#!/usr/bin/env python3
"""
Fix GNOME Remote Desktop crashes and connectivity issues

This script fixes common gnome-remote-desktop problems:
1. Missing /dev/dri/renderD128 causing libEGL errors
2. Missing FUSE module preventing clipboard functionality
3. Missing graphics devices preventing hardware acceleration
4. Service crashes and restart loops

Run with: python3 fix_gnome_remote_desktop.py
Or with sudo/pkexec for automatic privilege elevation
"""

import subprocess
import sys
import os
import time

def run_command(cmd, check=False):
    """Run a shell command and return output"""
    try:
        result = subprocess.run(
            cmd, 
            shell=True, 
            capture_output=True, 
            text=True,
            timeout=30
        )
        if check and result.returncode != 0:
            print(f"  ⚠️  Command failed: {cmd}")
            print(f"     Error: {result.stderr}")
        return result.stdout.strip()
    except subprocess.TimeoutExpired:
        print(f"  ⚠️  Command timed out: {cmd}")
        return ""
    except Exception as e:
        print(f"  ⚠️  Error running command: {e}")
        return ""

def check_root():
    """Check if running as root, offer to elevate if not"""
    if os.geteuid() != 0:
        print("⚠️  This script needs root privileges to fix system devices.")
        print("🔧 Attempting to restart with sudo...")
        try:
            # Try sudo first
            os.execvp("sudo", ["sudo", sys.executable] + sys.argv)
        except:
            try:
                # Fall back to pkexec if sudo fails
                print("🔧 Sudo not available, trying pkexec...")
                os.execvp("pkexec", ["pkexec", sys.executable] + sys.argv)
            except:
                print("❌ Could not obtain root privileges.")
                print("   Please run with: sudo python3", sys.argv[0])
                sys.exit(1)

def load_essential_modules():
    """Load kernel modules required for gnome-remote-desktop"""
    print("\n🔧 Loading essential kernel modules...")
    
    modules = [
        ("fuse", "FUSE filesystem (clipboard support)"),
        ("drm", "Direct Rendering Manager"),
        ("drm_kms_helper", "KMS helper for graphics"),
    ]
    
    # Try to load platform-specific graphics drivers
    optional_modules = [
        ("i915", "Intel graphics"),
        ("amdgpu", "AMD graphics"),
        ("nouveau", "NVIDIA open-source"),
        ("vmwgfx", "VMware graphics"),
        ("virtio_gpu", "VirtIO graphics"),
    ]
    
    loaded = []
    for module, description in modules:
        print(f"  → Loading {module} ({description})...")
        result = run_command(f"modprobe {module} 2>&1")
        if "not found" not in result.lower() and "error" not in result.lower():
            loaded.append(module)
            print(f"  ✅ {module} loaded")
        else:
            print(f"  ⚠️  {module} failed to load")
    
    # Try optional modules silently
    for module, _ in optional_modules:
        result = run_command(f"modprobe {module} 2>/dev/null")
        if result == "":
            loaded.append(module)
    
    # Verify critical modules
    fuse_check = run_command("lsmod | grep -c '^fuse'")
    drm_check = run_command("lsmod | grep -c '^drm'")
    
    if fuse_check == "0":
        print("  ⚠️  FUSE module not loaded - clipboard may not work")
    if drm_check == "0":
        print("  ⚠️  DRM module not loaded - graphics acceleration may be limited")
    
    return loaded

def create_graphics_devices():
    """Create /dev/dri devices needed for gnome-remote-desktop"""
    print("\n🔧 Creating graphics devices...")
    
    # Create /dev/dri directory
    print("  → Creating /dev/dri directory...")
    run_command("mkdir -p /dev/dri")
    run_command("chmod 755 /dev/dri")
    
    # Create /dev/fuse device
    if not os.path.exists("/dev/fuse"):
        print("  → Creating /dev/fuse device...")
        run_command("mknod /dev/fuse c 10 229")
        run_command("chmod 666 /dev/fuse")
        print("  ✅ Created /dev/fuse")
    else:
        run_command("chmod 666 /dev/fuse")
        print("  ✅ /dev/fuse already exists")
    
    # Ensure video group exists
    run_command("getent group video >/dev/null || groupadd video")
    
    # Try to trigger udev to create devices
    print("  → Triggering udev for graphics devices...")
    run_command("udevadm trigger --subsystem-match=drm --action=add")
    run_command("udevadm settle --timeout=10")
    
    time.sleep(2)
    
    # Check if devices were created
    dri_exists = os.path.exists("/dev/dri/renderD128")
    
    if not dri_exists:
        print("  → Creating fallback DRI devices...")
        
        devices = [
            ("/dev/dri/card0", 226, 0, "Primary graphics card"),
            ("/dev/dri/renderD128", 226, 128, "Render node (required)"),
            ("/dev/dri/renderD129", 226, 129, "Secondary render node"),
        ]
        
        for device, major, minor, desc in devices:
            if not os.path.exists(device):
                print(f"    • Creating {device} - {desc}")
                run_command(f"mknod {device} c {major} {minor}")
                run_command(f"chmod 666 {device}")
                run_command(f"chown root:video {device}")
        
        print("  ✅ Created fallback DRI devices")
    else:
        print("  ✅ DRI devices already exist")
        # Fix permissions on existing devices
        run_command("chmod 666 /dev/dri/render* 2>/dev/null")
        run_command("chown root:video /dev/dri/* 2>/dev/null")
    
    # Verify critical device
    if os.path.exists("/dev/dri/renderD128"):
        print("  ✅ /dev/dri/renderD128 verified (required for gnome-remote-desktop)")
    else:
        print("  ❌ /dev/dri/renderD128 missing - remote desktop may fail")
    
    if os.path.exists("/dev/fuse"):
        print("  ✅ /dev/fuse verified (required for clipboard)")
    else:
        print("  ❌ /dev/fuse missing - clipboard will not work")

def detect_desktop_user():
    """Detect the primary desktop user (not root)"""
    print("\n🔍 Detecting desktop user...")
    
    # Method 1: SUDO_USER environment variable
    user = os.environ.get('SUDO_USER')
    if user and user != 'root':
        print(f"  → Found user via SUDO_USER: {user}")
        return user
    
    # Method 2: PKEXEC_UID
    pkexec_uid = os.environ.get('PKEXEC_UID')
    if pkexec_uid:
        try:
            import pwd
            user = pwd.getpwuid(int(pkexec_uid)).pw_name
            if user != 'root':
                print(f"  → Found user via PKEXEC_UID: {user}")
                return user
        except:
            pass
    
    # Method 3: Active desktop session
    result = run_command("loginctl list-sessions --no-pager | grep seat0 | awk '{print $3}' | head -1")
    if result and result != 'root':
        print(f"  → Found user via active session: {result}")
        return result
    
    # Method 4: Who's running gnome-session
    result = run_command("ps aux | grep '[g]nome-session' | grep -v root | awk '{print $1}' | head -1")
    if result and result != 'root':
        print(f"  → Found user via gnome-session: {result}")
        return result
    
    # Method 5: Who's running gnome-remote-desktop
    result = run_command("ps aux | grep '[g]nome-remote-desktop' | grep -v root | awk '{print $1}' | head -1")
    if result and result != 'root':
        print(f"  → Found user via gnome-remote-desktop: {result}")
        return result
    
    # Method 6: First real user in /home
    home_dirs = os.listdir('/home') if os.path.exists('/home') else []
    for dirname in home_dirs:
        if dirname not in ['lost+found', 'ubuntu', 'debian']:
            try:
                import pwd
                user_info = pwd.getpwnam(dirname)
                if user_info.pw_uid >= 1000:  # Regular users start at 1000
                    print(f"  → Found user via /home directory: {dirname}")
                    return dirname
            except:
                continue
    
    print("  ⚠️  Could not detect desktop user")
    return None

def add_user_to_groups(username):
    """Add user to necessary groups for device access"""
    if not username:
        return
    
    print(f"\n🔧 Configuring user permissions for {username}...")
    
    groups = ['video', 'input']
    for group in groups:
        # Check if group exists
        if run_command(f"getent group {group}") != "":
            print(f"  → Adding {username} to {group} group...")
            run_command(f"usermod -a -G {group} {username} 2>/dev/null")
            print(f"  ✅ Added to {group} group")
    
    print("  ℹ️  Note: User may need to log out/in for group changes to take effect")

def restart_remote_desktop_service(username):
    """Restart gnome-remote-desktop service for the user"""
    if not username:
        print("\n⚠️  Cannot restart service - user not detected")
        print("  Please run manually: systemctl --user restart gnome-remote-desktop")
        return False
    
    print(f"\n🔧 Restarting gnome-remote-desktop for {username}...")
    
    # Try to restart the service as the user
    result = run_command(f"sudo -u {username} systemctl --user restart gnome-remote-desktop 2>&1")
    
    # Check if successful
    time.sleep(2)
    status = run_command(f"sudo -u {username} systemctl --user is-active gnome-remote-desktop")
    
    if status == "active":
        print("  ✅ Service restarted successfully")
        
        # Show current status
        print("\n📊 Service Status:")
        status_output = run_command(f"sudo -u {username} systemctl --user status gnome-remote-desktop --no-pager | head -15")
        for line in status_output.split('\n'):
            print(f"  {line}")
        
        return True
    else:
        print("  ⚠️  Service may need manual restart")
        print(f"  Run as {username}: systemctl --user restart gnome-remote-desktop")
        return False

def check_current_status():
    """Check current status of devices and service"""
    print("\n📋 Current System Status:")
    
    # Check DRI devices
    if os.path.exists("/dev/dri/renderD128"):
        print("  ✅ /dev/dri/renderD128 exists")
    else:
        print("  ❌ /dev/dri/renderD128 missing")
    
    # Check FUSE
    if os.path.exists("/dev/fuse"):
        print("  ✅ /dev/fuse exists")
    else:
        print("  ❌ /dev/fuse missing")
    
    # Check FUSE module
    fuse_loaded = run_command("lsmod | grep -c '^fuse'")
    if fuse_loaded != "0":
        print("  ✅ FUSE module loaded")
    else:
        print("  ❌ FUSE module not loaded")
    
    # Check for any gnome-remote-desktop processes
    grd_running = run_command("pgrep -c gnome-remote-de")
    if grd_running != "0":
        print(f"  ✅ gnome-remote-desktop running ({grd_running} process(es))")
    else:
        print("  ❌ gnome-remote-desktop not running")

def main():
    """Main function to fix gnome-remote-desktop issues"""
    print("=" * 60)
    print("🔧 GNOME Remote Desktop Fix Tool")
    print("=" * 60)
    
    # Check current status
    check_current_status()
    
    # Check for root privileges
    check_root()
    
    print("\n🚀 Starting fixes...")
    
    # Load kernel modules
    load_essential_modules()
    
    # Create necessary devices
    create_graphics_devices()
    
    # Detect desktop user
    desktop_user = detect_desktop_user()
    
    # Add user to groups
    if desktop_user:
        add_user_to_groups(desktop_user)
    
    # Restart service
    if desktop_user:
        restart_remote_desktop_service(desktop_user)
    
    # Final status check
    print("\n" + "=" * 60)
    print("📊 Final Status Check:")
    print("=" * 60)
    check_current_status()
    
    print("\n✅ Fix process completed!")
    
    if desktop_user:
        print(f"\n💡 Next steps for {desktop_user}:")
        print("  1. Try connecting to remote desktop now")
        print("  2. If it still fails, log out and back in (for group changes)")
        print("  3. Check service logs: journalctl --user -u gnome-remote-desktop -f")
    else:
        print("\n💡 Manual steps required:")
        print("  1. Run as your user: systemctl --user restart gnome-remote-desktop")
        print("  2. Try connecting to remote desktop")
        print("  3. If needed, log out and back in")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
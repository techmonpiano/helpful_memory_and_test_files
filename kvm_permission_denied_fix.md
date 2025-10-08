# KVM Permission Denied Fix

## Problem
```
Error starting domain: internal error: process exited while connecting to monitor: Could not access KVM kernel module: Permission denied
qemu-system-x86_64: -accel kvm: failed to initialize kvm: Permission denied
```

## Root Cause
Missing udev rule file: `/etc/udev/rules.d/65-kvm.rules`

## Solution
1. **Fix device permissions:**
   ```bash
   sudo chmod 660 /dev/kvm
   sudo chown root:kvm /dev/kvm
   ```

2. **Create missing udev rule:**
   ```bash
   echo 'KERNEL=="kvm", NAME="%k", GROUP="kvm", MODE="0660"' | sudo tee /etc/udev/rules.d/65-kvm.rules
   ```

3. **Reload udev rules:**
   ```bash
   sudo udevadm control --reload-rules
   sudo udevadm trigger
   ```

## Verification
- User should be in kvm group: `groups $USER`
- Device permissions: `ls -la /dev/kvm` should show `crw-rw----+ 1 root kvm`
- Rule file exists: `/etc/udev/rules.d/65-kvm.rules`

## Notes
- This file can get deleted during system updates or manual cleanup
- No reboot required after applying fix
- Works immediately after udev reload
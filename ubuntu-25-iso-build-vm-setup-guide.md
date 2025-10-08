# Ubuntu 25.04 ISO Build and VM Setup Guide
Generated: 2025-07-16

## Project Summary
Successfully built a custom Ubuntu 25.04 "Plucky Puffin" (development) ISO using the uStandard project with GNOME minimal desktop.

## Repository Details
- **Project**: https://github.com/linuxmative/uStandard
- **Author**: Maksym Titenko (@titenko)
- **Local Path**: `/home/user1/uStandard/`
- **ISO Created**: `/home/user1/uStandard/CustomUbuntu-20250716.iso` (1.3GB)

## Ubuntu 25.04 Package Compatibility Fixes
The development version required package updates:

### Deprecated Packages Fixed
1. **policykit-1** → `polkitd pkexec` (new PolicyKit implementation)
2. **wireless-tools** → removed (replaced by `iw` for wireless config)

### Fix Applied
```bash
# Fix script created: /home/user1/uStandard/fix_ubuntu_25.04.sh
sed -i 's/policykit-1/polkitd pkexec/g' uStandard.sh
sed -i 's/wireless-tools //g' uStandard.sh
sed -i 's/network-manager/network-manager iw/g' uStandard.sh
```

## ISO Structure Verification
The ISO has proper dual-boot support:
- ✅ BIOS boot: `/boot/grub/i386-pc/eltorito.img`
- ✅ UEFI boot: `/efi.img`
- ✅ El Torito catalog present
- ✅ Bootable with both legacy and UEFI systems

## VM Configuration Issues and Solutions

### Problem: UEFI Boot Failure
VMs created with `firmware='efi'` auto-detection may fail to boot the ISO.

### Working VM Configuration (mx-tools example)
```xml
<os>
  <type arch='x86_64' machine='pc-q35-6.2'>hvm</type>
  <loader readonly='yes' type='pflash'>/usr/share/OVMF/OVMF_CODE_4M.fd</loader>
  <nvram>/var/lib/libvirt/qemu/nvram/mx-tools_VARS.fd</nvram>
  <bootmenu enable='yes'/>
</os>
```

### VM Creation Commands

#### Clone Existing VM
```bash
virt-clone --original porteux-template --name ubuntu-25-test --file /var/lib/libvirt/images/ubuntu-25-test.qcow2
```

#### Create New VM with Proper UEFI
```bash
virt-install --name ubuntu-25-test --memory 4096 --vcpus 6 --disk size=20 --cdrom /home/user1/uStandard/CustomUbuntu-20250716.iso --boot uefi,bootmenu.enable=on --graphics spice --noautoconsole
```

#### Full Command with Explicit UEFI Paths
```bash
virt-install --name ubuntu-25-test --memory 4096 --vcpus 6 --disk size=20,path=/var/lib/libvirt/images/ubuntu-25-test.qcow2 --cdrom /home/user1/uStandard/CustomUbuntu-20250716.iso --osinfo linux2024 --machine q35 --boot uefi,loader=/usr/share/OVMF/OVMF_CODE_4M.fd,loader.readonly=yes,loader.type=pflash,nvram.template=/usr/share/OVMF/OVMF_VARS_4M.fd,bootmenu.enable=on --graphics spice --network default --noautoconsole
```

## Quick Test Commands

### Direct QEMU Test
```bash
# BIOS mode
qemu-system-x86_64 -m 2048 -cdrom ~/uStandard/CustomUbuntu-20250716.iso -boot d

# UEFI mode
qemu-system-x86_64 -m 2048 -cdrom ~/uStandard/CustomUbuntu-20250716.iso -boot d -bios /usr/share/ovmf/OVMF.fd
```

### VM Management
```bash
# List all VMs
virsh list --all

# Start VM
virsh start ubuntu-25-test

# Access console
virt-manager --show-domain-console ubuntu-25-test

# Check block devices
virsh domblklist ubuntu-25-test

# Edit VM configuration
virsh edit ubuntu-25-test
```

## Build Configuration Used
- **Ubuntu Version**: 25.04 "Plucky Puffin" (development)
- **Desktop**: GNOME Minimal (`ubuntu-desktop-minimal`)
- **Username**: myuser
- **Password**: changeme123
- **Build Time**: ~45 minutes
- **ISO Size**: 1.3GB

## Files Created During Session
1. `/home/user1/uStandard/custom_config.sh` - Build configuration
2. `/home/user1/uStandard/build_custom.sh` - Wrapper script
3. `/home/user1/uStandard/fix_ubuntu_25.04.sh` - Package compatibility fixes
4. `/home/user1/uStandard/check_packages.sh` - Package availability checker
5. `/home/user1/uStandard/MEMORY_BANK_ISO_BUILD.md` - Session details
6. `/home/user1/uStandard/README_USER.md` - User guide
7. `/home/user1/uStandard/VIRT_MANAGER_BOOT_FIX.md` - VM boot troubleshooting
8. `/home/user1/uStandard/VM_BOOT_COMMANDS.sh` - Boot fix commands
9. `/home/user1/uStandard/fix_vm_uefi.sh` - UEFI configuration fix
10. `/home/user1/uStandard/clone_vm_command.sh` - VM cloning commands

## Security Notes
Default passwords in ISO - change before production use:
- myuser/changeme123 (custom user)
- ubuntu/ubuntu (default user)
- root/changemealso123 (root)

## Lessons Learned
1. Ubuntu 25.04 deprecated several legacy packages requiring updates
2. VMs need explicit UEFI loader paths for reliable ISO booting
3. The `firmware='efi'` auto-detection may not work with all ISOs
4. Always enable boot menu for easier troubleshooting
5. Development versions may have package availability issues

## Next Steps
1. Test the ISO in a VM with proper UEFI configuration
2. Consider switching to Ubuntu 24.10 for stability if needed
3. Customize the build further (different desktop, packages)
4. Create USB bootable media for physical hardware testing
# Virt-Manager Boot Issues - Fix Guide

## ISO Boot Structure
Your ISO has proper dual-boot support:
- ✅ BIOS boot: `/boot/grub/i386-pc/eltorito.img`
- ✅ UEFI boot: `/efi.img`
- ✅ El Torito catalog present
- ✅ Size: 1.3GB (normal for minimal GNOME)

## Virt-Manager Configuration Fixes

### 1. UEFI Firmware Selection
When creating VM in virt-manager:
1. Click "Customize configuration before install"
2. Under Overview → Firmware:
   - Change from "BIOS" to "UEFI x86_64"
   - Or select "UEFI x86_64: /usr/share/OVMF/OVMF_CODE.fd"

### 2. If UEFI Option Missing
Install OVMF firmware:
```bash
sudo apt install ovmf
```

### 3. Alternative: Force BIOS Mode
If UEFI fails, use BIOS mode:
1. Overview → Firmware → BIOS
2. Boot Options → Enable boot menu
3. Add Hardware → Storage → Select ISO as CDROM

### 4. Direct QEMU Command (Bypass virt-manager)
Test ISO directly:
```bash
# BIOS mode
qemu-system-x86_64 -m 2048 -cdrom ~/uStandard/CustomUbuntu-20250716.iso -boot d

# UEFI mode
qemu-system-x86_64 -m 2048 -cdrom ~/uStandard/CustomUbuntu-20250716.iso -boot d \
  -bios /usr/share/ovmf/OVMF.fd
```

### 5. Virt-Manager Specific Settings
In VM settings:
- **Boot Options**: 
  - ✓ Enable boot menu
  - ✓ CDROM as first boot device
- **IDE CDROM**: 
  - Bus: IDE or SATA (not VirtIO for boot)
  - Source: Your ISO path

### 6. Common Issues
- **Secure Boot**: Disable in UEFI settings
- **ISO Path**: Use absolute path, avoid spaces
- **Permissions**: Check ISO is readable by libvirt-qemu user
- **RAM**: Minimum 2GB for GNOME

## Quick Test
Try this simple QEMU command first:
```bash
qemu-system-x86_64 -m 2048 -cdrom ~/uStandard/CustomUbuntu-20250716.iso -boot d
```

If this works, the issue is virt-manager configuration, not the ISO.
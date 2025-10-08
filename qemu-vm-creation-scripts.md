# QEMU VM Creation Scripts

## Configurable VM Creation Script

Set your variables at the top, then run the commands below:

```bash
# ================================
# USER CONFIGURATION VARIABLES
# ================================
VM_NAME="ubuntu-25-test"
ISO_PATH="/home/user1/uStandard/CustomUbuntu-20250716.iso"
MEMORY="4096"
VCPUS="6"
DISK_SIZE="20"

# ================================
# GENERATED PATHS (DO NOT MODIFY)
# ================================
QCOW2_PATH="/var/lib/libvirt/images/${VM_NAME}.qcow2"
```

## Full VM Creation with UEFI

```bash
virt-install --name ${VM_NAME} --memory ${MEMORY} --vcpus ${VCPUS} \
  --disk size=${DISK_SIZE},path=${QCOW2_PATH} \
  --cdrom ${ISO_PATH} \
  --osinfo linux2024 --machine q35 \
  --boot uefi,loader=/usr/share/OVMF/OVMF_CODE_4M.fd,loader.readonly=yes,loader.type=pflash,nvram.template=/usr/share/OVMF/OVMF_VARS_4M.fd,bootmenu.enable=on \
  --graphics spice --network default --noautoconsole
```

## Quick QEMU Test Commands

```bash
# Basic test
qemu-system-x86_64 -m ${MEMORY} -cdrom ${ISO_PATH} -boot d

# UEFI mode test
qemu-system-x86_64 -m ${MEMORY} -cdrom ${ISO_PATH} -boot d -bios /usr/share/ovmf/OVMF.fd
```

## VM Cloning from Template

```bash
virt-clone --original porteux-template --name ${VM_NAME} --file ${QCOW2_PATH}
```

## VM Management Commands

```bash
# List VMs
virsh list --all

# Start VM
virsh start ${VM_NAME}

# Stop VM
virsh shutdown ${VM_NAME}

# Delete VM (keeps disk)
virsh undefine ${VM_NAME}

# Delete VM and disk
virsh undefine ${VM_NAME} --remove-all-storage
```

## Common Settings Variations

### High Performance VM
```bash
VM_NAME="ubuntu-performance"
MEMORY="8192"
VCPUS="8"
DISK_SIZE="50"
```

### Minimal Test VM
```bash
VM_NAME="ubuntu-minimal"
MEMORY="2048"
VCPUS="2"
DISK_SIZE="10"
```

### Development VM
```bash
VM_NAME="ubuntu-dev"
MEMORY="6144"
VCPUS="4"
DISK_SIZE="30"
```

## One-Line Terminal Paste Format

```bash
# Set your variables
VM_NAME="ubuntu-25-test" && \
ISO_PATH="/home/user1/uStandard/CustomUbuntu-20250716.iso" && \
MEMORY="4096" && \
VCPUS="6" && \
DISK_SIZE="20" && \
QCOW2_PATH="/var/lib/libvirt/images/${VM_NAME}.qcow2" && \
\
# Create VM with UEFI
virt-install --name ${VM_NAME} --memory ${MEMORY} --vcpus ${VCPUS} \
  --disk size=${DISK_SIZE},path=${QCOW2_PATH} \
  --cdrom ${ISO_PATH} \
  --osinfo linux2024 --machine q35 \
  --boot uefi,loader=/usr/share/OVMF/OVMF_CODE_4M.fd,loader.readonly=yes,loader.type=pflash,nvram.template=/usr/share/OVMF/OVMF_VARS_4M.fd,bootmenu.enable=on \
  --graphics spice --network default --noautoconsole
```

## Notes

- Change the variables at the top to customize your VM
- The script automatically uses the VM_NAME for the qcow2 file
- UEFI configuration fixes boot issues with modern ISOs
- Use `--noautoconsole` to prevent automatic console opening
- Machine type `q35` is recommended for modern VMs
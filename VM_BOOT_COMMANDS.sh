#!/bin/bash
# Commands to fix VM boot issues

echo "=== VM Boot Fix Commands ==="
echo ""
echo "1. Force boot from CDROM (while VM is running):"
echo "   virsh send-key porteux-template KEY_F12"
echo "   # Then select CDROM from boot menu"
echo ""
echo "2. Check VM console for boot messages:"
echo "   virsh console porteux-template"
echo "   # Press Ctrl+] to exit console"
echo ""
echo "3. Access VM through virt-manager GUI:"
echo "   virt-manager --connect qemu:///system --show-domain-console porteux-template"
echo ""
echo "4. Alternative: Create new VM with explicit UEFI:"
cat << 'EOF'
virt-install \
  --name ubuntu-test \
  --memory 4096 \
  --vcpus 2 \
  --cdrom /home/user1/uStandard/CustomUbuntu-20250716.iso \
  --disk size=20 \
  --boot uefi \
  --osinfo ubuntu24.04 \
  --graphics spice \
  --noautoconsole
EOF
echo ""
echo "5. If UEFI fails, try BIOS mode:"
echo "   virsh destroy porteux-template"
echo "   virsh edit porteux-template"
echo "   # Remove firmware='efi' from <os> line"
echo "   # Change to: <os>"
echo "   virsh start porteux-template"
# VM Export Script Development Session - January 2025

## Overview
Developed a comprehensive VM export/restore script for QEMU/libvirt with interactive features and progress monitoring.

## Initial Requirements
- Export VM configuration and disk files completely
- Interactive VM selection from auto-detected list
- Current directory as default export location
- Optional snapshot inclusion (excluded by default)
- Real-time copy progress with percentage

## Script Development Journey

### Version 1: Basic Export Script
- **Location**: `/home/user1/shawndev1/auto/scripts/export-vm.sh`
- **Features**: Basic VM export with manual VM name input
- **Issues**: 
  - No interactive selection
  - No progress display
  - Permission issues with libvirt disk access
  - Missing restore script generation

### Version 2: Interactive Enhanced Script
- **Location**: `/home/user1/shawndev1/auto/scripts/export-vm-fixed.sh`
- **Major Improvements**:
  - Interactive VM selection with auto-detection
  - Interactive disk selection (include/exclude each disk)
  - Real-time copy progress with multiple fallback options
  - Fixed restore script generation
  - Automatic disk path correction in XML

## Key Features Implemented

### 1. Interactive VM Selection
```bash
[INFO] Available VMs:
 1) mx-tools             [shut off]
 2) UbuntuX-GNOME-Test   [shut off]
Select VM to export (1-2): _
```

### 2. Export Directory Selection
- Current directory as default (press Enter)
- Custom directory option
- Clear prompt: `Choose export location (1-2) [default: 1]:`

### 3. Interactive Disk Selection
- Shows disk details: target, name, size, type (DISK/ISO/OTHER)
- Default behavior: Press Enter to include
- Press 'n' to exclude specific disks
- Example output:
```bash
Include disk: mxlinux-tools.qcow2  [DISK    ] 14GiB
Path: /var/lib/libvirt/images/mxlinux-tools.qcow2
Include this disk? [Y/n]: _
```

### 4. Real-Time Copy Progress
**Three-tier fallback system:**
1. **pv (pipe viewer)** - Best option with detailed progress
   ```bash
   holding.img: 45% [======>    ] 2.2GiB/5.0GiB [42.1MiB/s] [00:32<00:38]
   ```
2. **rsync** - Good fallback with percentage
   ```bash
   holding.img     2.2GB  45%   42.10MB/s    0:00:32
   ```
3. **Spinner** - Basic progress indicator for systems without pv/rsync

### 5. Permission Handling
- Automatic detection of read permissions
- Seamless sudo elevation when needed
- Proper file ownership correction after sudo operations

## Issues Encountered & Solutions

### Issue 1: Disk Detection Problems
**Problem**: Script was detecting disks from other VMs or showing cached data
**Root Cause**: Old disk list files and VM configuration changes
**Solution**: Added fresh data retrieval and debug output
```bash
# Ensure we get fresh data - remove any old disk list first
rm -f "$EXPORT_DIR/${VM_NAME}_disklist.txt"
```

### Issue 2: Restore Script Path Problems
**Problem**: Restored VMs couldn't start due to incorrect disk paths
**Error**: `Cannot access storage file '/original/path/disk.qcow2': No such file or directory`
**Solution**: Enhanced path update logic in restore script
```bash
# Update XML to point to new disk locations with multiple patterns
sed -i "s|<source file='[^']*/$disk_name'|<source file='/var/lib/libvirt/images/$disk_name'|g"
sed -i "s|<source file='[^']*$disk_name'|<source file='/var/lib/libvirt/images/$disk_name'|g"
```

### Issue 3: Missing Disk References
**Problem**: VM configuration referenced non-existent disk files
**Discovery**: VM had disk attachment to `/home/user1/shawndev1/ubuntux/vm-test/ubuntux-gnome-test.qcow2` but file didn't exist
**Impact**: Export script correctly skipped missing files, but VM couldn't start
**Resolution**: Need to remove broken disk references from VM configuration

## File Structure Created

### Export Directory Structure
```
mx-tools/
├── mx-tools_config.xml          # VM configuration
├── mx-tools_info.txt            # VM information
├── mx-tools_disklist.txt        # Detected disks list
├── mx-tools_networks.txt        # Network configuration
├── restore-mx-tools.sh          # Automated restore script
├── EXPORT_SUMMARY.txt           # Export summary and file list
├── holding.img                  # Exported disk 1
├── mxlinux-tools.qcow2         # Exported disk 2
└── ubuntux-gnome-test.qcow2    # Exported disk 3 (if included)
```

### Restore Script Features
- Automatic VM existence check with overwrite option
- Progress display during disk copying (same as export)
- Automatic XML path correction
- Proper libvirt ownership setting
- Success confirmation and start instructions

## Technical Insights

### libvirt/QEMU Disk Management
- Disk files typically owned by `libvirt-qemu:libvirt-qemu`
- Standard location: `/var/lib/libvirt/images/`
- VM XML configuration must match actual file locations
- Permission issues require sudo for access

### Progress Display Tools
- **pv**: Most comprehensive progress display
- **rsync**: Good alternative with built-in progress
- **Fallback spinner**: Works on minimal systems

### VM Configuration Consistency
- `virsh domblklist` shows attached disks
- `virsh dumpxml` shows full configuration
- Disk attachments can exist without actual files (causes startup errors)
- XML path updates require careful regex patterns

## Commands Reference

### Manual VM Operations
```bash
# List all VMs
virsh list --all

# Show VM disks
virsh domblklist vm-name

# Show disk sources in XML
virsh dumpxml vm-name | grep "source file"

# Edit VM configuration
virsh edit vm-name

# Check disk file existence
ls -la /var/lib/libvirt/images/
```

### Script Usage
```bash
# Interactive mode (recommended)
./export-vm-fixed.sh

# Command line mode
./export-vm-fixed.sh vm-name [export-directory]

# Restore VM
cd export-directory && ./restore-vm-name.sh
```

## Lessons Learned

1. **Always verify disk file existence** before VM operations
2. **Interactive selection prevents user errors** with large disk exports
3. **Progress display is crucial** for large file operations
4. **Path normalization in XML** requires multiple regex patterns
5. **Fresh data retrieval** prevents cached/stale information issues
6. **Fallback mechanisms** ensure compatibility across different systems

## Outstanding Issues

1. **Missing disk cleanup**: VMs may have references to non-existent disks
2. **Storage space validation**: Should check available space before export
3. **Network configuration**: May need adjustment after restore
4. **Snapshot handling**: Could be enhanced for complex snapshot trees

## Success Metrics

✅ **Interactive VM selection** - Working  
✅ **Interactive disk selection** - Working  
✅ **Real-time progress display** - Working  
✅ **Permission handling** - Working  
✅ **Restore script generation** - Working  
✅ **XML path correction** - Working  
⚠️ **VM startup after restore** - Needs disk reference cleanup  

## Next Steps

1. Add storage space validation before export
2. Implement automatic cleanup of missing disk references
3. Add network configuration restoration
4. Create batch export functionality for multiple VMs
5. Add compression options for large exports

---

**Session Date**: January 2025  
**Script Location**: `/home/user1/shawndev1/auto/scripts/export-vm-fixed.sh`  
**Status**: Functional with minor cleanup needed for disk references
# Timeshift Snapshot Cleanup Session - June 30, 2025

## Issue Summary
User encountered disk space issues (8% free, need 10%) that prevented APT package installation due to pre-update snapshot script failing. The script `/usr/local/bin/pre-update-snapshot.sh` was blocking package installations.

## Root Cause
- Timeshift snapshots consuming excessive disk space
- Pre-update snapshot script requires 10% free space minimum
- User had 23 snapshots taking up significant space

## Investigation Process

### 1. Located the Pre-Update Script
**File:** `/usr/local/bin/pre-update-snapshot.sh`
- APT hook that creates BTRFS snapshots before package installations
- Checks for minimum 10% free disk space
- Uses snapper or timeshift for snapshot creation
- Has interactive prompts and timeout handling

### 2. Timeshift Snapshot Analysis
Initial snapshot list showed 23 snapshots:
```
0-4:  Manual snapshots from May 2025 (kept)
5-22: Auto-update snapshots from June 19-27, 2025 (deleted)
```

### 3. Common Timeshift GUI Issues Found
Research revealed common problems:
- Cancelled snapshots not properly cleaned up
- Snapshots showing 0 size but disk space not recovered
- Files moved to trash instead of permanently deleted
- Nested snapshot structures preventing deletion
- GUI showing directory metadata size vs actual content

## Solution Applied

### Command Used for Bulk Deletion
```bash
for snapshot in "2025-06-19_11-37-31" "2025-06-19_15-53-32" "2025-06-19_15-53-35" "2025-06-20_06-46-34" "2025-06-20_16-37-40" "2025-06-21_07-58-55" "2025-06-23_14-07-31" "2025-06-24_12-20-36" "2025-06-26_14-55-45" "2025-06-27_08-47-09" "2025-06-27_08-47-12" "2025-06-27_10-23-33" "2025-06-27_10-45-38" "2025-06-27_10-49-50" "2025-06-27_10-54-19" "2025-06-27_11-14-14" "2025-06-27_14-13-00" "2025-06-27_14-23-29"; do sudo timeshift --delete --snapshot "$snapshot"; done
```

### Results
- Successfully deleted 18 snapshots (from June 19-27, 2025)
- Kept 5 older snapshots with important configurations
- Most snapshots deleted successfully with "Deleted subvolume" messages
- Some "Failed to destroy qgroup" errors (harmless - related to BTRFS quota management)
- Significant disk space recovered

## Key Learnings

### Timeshift CLI vs GUI
- **CLI deletion more reliable** than GUI for bulk operations
- Use snapshot names (e.g., "2025-06-19_11-37-31") not numbers
- Command: `sudo timeshift --delete --snapshot "SNAPSHOT_NAME"`

### Common Troubleshooting Commands
```bash
# List all snapshots
sudo timeshift --list

# Check actual disk usage
sudo ncdu /run/timeshift/backup

# Check for files in trash
ls -la /root/.local/share/trash
ls -la ~/.local/share/trash

# Direct BTRFS commands (if needed)
sudo btrfs subvolume list /
sudo btrfs subvolume delete /path/to/snapshot
```

### Best Practices
1. **Regular cleanup** of auto-update snapshots (keep only recent ones)
2. **Use CLI for bulk operations** instead of GUI
3. **Monitor disk space** before it becomes critical
4. **Keep important manual snapshots** (tagged with descriptions)
5. **Ignore qgroup errors** during deletion (they're harmless)

## Files Involved
- **Pre-update script:** `/usr/local/bin/pre-update-snapshot.sh`
- **Timeshift snapshots:** `/run/timeshift/backup/timeshift-btrfs/snapshots/`
- **Config file:** `/etc/default/pre-update-snapshot`
- **Log file:** `/var/log/auto-update-snapshots.log`

## Prevention
- Set up automatic cleanup policies in timeshift
- Monitor disk usage regularly
- Consider adjusting `MIN_FREE_SPACE_PERCENT` in pre-update script if needed
- Regularly review and clean old auto-update snapshots

## Error Patterns to Ignore
- "Failed to destroy qgroup" - BTRFS quota management, harmless
- Directory size showing 4KB instead of actual content - use proper tools like `ncdu`
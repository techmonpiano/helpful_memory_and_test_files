# Syncthing: Identifying Which Device Caused Sync Conflicts

## Problem Description
When Syncthing shows errors like:
- "directory has been deleted on a remote device but is not empty"
- "the contents are probably ignored on that remote device, but not locally"

It's not immediately clear from the logs which remote device deleted the directory.

## Methods to Identify the Culprit Device

### 1. **Check Recent Changes in Web GUI** (Easiest)
- Open Syncthing Web GUI: http://localhost:8384
- Look for the **"Recent Changes"** button (usually in top menu or under device list)
- This shows file operations since Syncthing last started, including which device initiated changes
- **Limitation**: Only shows changes since last restart

### 2. **Check Each Device's Folder Status**
In the Web GUI:
- Click on each connected device (e.g., "mxtools")
- Look at folder details for problematic folders
- Check if any device shows directories as "deleted" or "out of sync"
- Compare folder states across devices

### 3. **Check Folder Details for Failed Items**
In the Web GUI:
- Click on the problematic folders
- Look for "Failed Items" or "Out of Sync Items"
- Click on them to see detailed error messages
- These may indicate which device has the conflict

### 4. **Enable Audit Logging for Future Tracking**
To capture detailed information about future changes:

**Option A - Via Web GUI:**
- Go to Actions → Settings → Advanced
- Look for "Audit Events" option
- Enable it to track future changes

**Option B - Via Command Line:**
```bash
# Stop current Syncthing instance first
syncthing --audit
```

**Audit Log Location:**
- Logs are saved to: `~/.local/state/syncthing/audit-_date_-_time_.log`
- Contains JSON-formatted sequence of events
- Shows which device initiated each change

### 5. **Understanding the Error Messages**

**"directory has been deleted on a remote device but is not empty"**
- Means: A remote device deleted a directory
- But: Your local device still has files in it
- Often caused by different ignore patterns between devices

**Common Causes:**
1. Remote device has ignore patterns that exclude files in the directory
2. Remote device deleted the directory thinking it was empty
3. Local device doesn't have the same ignore patterns
4. Results in sync conflict

### 6. **Limitations to Be Aware Of**

- **Recent Changes** only shows changes since last Syncthing restart
- **Audit logs** must be enabled BEFORE the deletion occurs
- When devices reconnect after being offline, Syncthing only sees the final state, not the exact sequence of changes
- Complex network topologies can make it harder to track the originating device

### 7. **Example from Actual Logs**

From the provided logs:
```
Puller (folder "shawndev1" (fogk4-wjohp), item "uStandard/ustandardbuild"): 
syncing: delete dir: directory has been deleted on a remote device but is not empty

Puller (folder "auto" (xcamy-mqoe5), item "mcp-claudecode-quick-scripts"): 
syncing: delete dir: directory has been deleted on a remote device but is not empty
```

Connected devices seen:
- Local device: `EOO2FMD-TJTZD6J-I2THBWU-HKSH4UP-YUPN47H-I2C775L-L4XEPMV-CL6IAQ5`
- "mxtools" device: `63NJNZI-GRRULFV-PZAWS67-ZTZ64U7-Y3Y67FE-JEYM3EB-BITHHSE-74TBAA3`
- Ignored device: `Q37Q5PV-WASXH4W-FQHDMSQ-24IB5PA-3WYCCFE-CJZY5QJ-FJSJHRZ-6ANK4QY`
- Paused device: `CFVO63E-IR76V3G-M3XXVE6-GDWOCMC-QUXKLRJ-JXCHZWI-MOBEDJJ-HDDQYQJ`

### 8. **Resolution Steps**

1. **Identify the device** using methods above
2. **Check `.stignore` files** on both local and remote devices
3. **Decide on action:**
   - If files not needed: Delete them locally
   - If files needed: Update ignore patterns to match across devices
   - If unsure: Backup files first, then resolve conflict
4. **Restart sync** after cleanup

### 9. **Preventing Future Conflicts**

- Keep `.stignore` patterns synchronized across all devices
- Enable audit logging for easier troubleshooting
- Regularly check Recent Changes after major operations
- Document which device is authoritative for specific folders

---
*Created: August 4, 2025*
*Context: Troubleshooting Syncthing sync conflicts for uStandard/ustandardbuild and mcp-claudecode-quick-scripts directories*
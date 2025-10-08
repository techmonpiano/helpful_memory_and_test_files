# APT Snapshot Script Fixes - Memory Bank

## Problem Summary
APT package installations were failing due to a pre-update snapshot script (`/usr/local/bin/pre-update-snapshot.sh`) that would abort when it encountered a running Timeshift process (PID 727639). The script used `set -e` and had no graceful handling for existing processes.

## Root Cause
- APT was configured with a pre-install hook: `DPkg::Pre-Install-Pkgs {"/usr/local/bin/pre-update-snapshot.sh";}` in `/etc/apt/apt.conf.d/50unattended-upgrades`
- The script failed when Timeshift was already running, causing all APT operations to abort
- No graceful process handling or fallback options were implemented

## Solution Implemented

### 1. Enhanced Process Detection and Handling
Added functions to:
- Check if processes are running and their age
- Wait for existing processes to complete (with configurable timeout)
- Optionally kill stuck processes that have been running too long
- Gracefully handle process conflicts

### 2. Interactive User Prompts (NEW)
Added intelligent user interaction when snapshots fail or timeout:
- **30-second timeout** for snapshot operations by default
- **Interactive prompts** when timeshift/snapper fails or times out
- **User options**: Bypass snapshots (y), Abort installation (n), or Wait longer (w)
- **Smart detection** of interactive vs non-interactive sessions
- **Configurable** prompt behavior via `ENABLE_INTERACTIVE_PROMPT`

### 3. Improved Error Handling
- Removed `set -e` for more granular error control
- Added proper return codes instead of immediate exits
- Better logging of specific failure reasons
- Fallback options when snapshot tools fail
- **New**: Special return code (2) for user-initiated bypass

### 4. Enhanced Configuration System
Updated `/etc/default/pre-update-snapshot` with new options:
- `PROCESS_WAIT_TIMEOUT`: Time to wait for existing processes (default: 300s)
- `INTERACTIVE_TIMEOUT`: Timeout for snapshot operations and user prompts (default: 30s) **NEW**
- `ENABLE_INTERACTIVE_PROMPT`: Enable/disable user prompts (default: true) **NEW**
- `ALLOW_SKIP_SNAPSHOTS`: Allow proceeding without snapshots in certain conditions
- `KILL_STUCK_PROCESSES`: Kill processes running over 1 hour
- `SKIP_SNAPSHOTS`: Environment variable to temporarily disable snapshots

### 5. Key Script Improvements
- **Process Detection**: `check_process_age()` function identifies running processes and their age
- **Interactive Prompts**: `prompt_user_bypass()` function handles user interaction **NEW**
- **Graceful Waiting**: `handle_existing_processes()` waits for or handles existing processes
- **Timeout Protection**: All snapshot operations now have timeout protection **NEW**
- **Flexible Execution**: Main function now has multiple fallback paths
- **Better Logging**: Enhanced logging with timestamps and detailed status messages

## Usage Examples

### Interactive Prompt Scenarios (NEW)
When a snapshot tool fails or times out after 30 seconds, users see:
```
⚠️  SNAPSHOT TIMEOUT: timeshift failed to complete within 30s
   This may prevent package installation from proceeding.

Options:
  y/Y - Bypass snapshots and continue with package installation
  n/N - Abort package installation (default)
  w/W - Wait another 30s for timeshift to complete

Decision [y/n/w]:
```

### Temporary Snapshot Bypass
```bash
SKIP_SNAPSHOTS=1 apt install package-name
```

### Disable Interactive Prompts (for Automated Systems)
Edit `/etc/default/pre-update-snapshot`:
```bash
ENABLE_INTERACTIVE_PROMPT=false
```

### Adjust Timeout for Snapshot Operations
```bash
INTERACTIVE_TIMEOUT=60  # Wait 60 seconds instead of 30
```

### Allow System to Proceed When Snapshots Fail
```bash
ALLOW_SKIP_SNAPSHOTS=true
```

### Kill Stuck Processes Automatically
```bash
KILL_STUCK_PROCESSES=true
```

## Files Modified
1. `/usr/local/bin/pre-update-snapshot.sh` - Main script with enhanced logic
2. `/etc/default/pre-update-snapshot` - Configuration file for customization

## Testing
Successfully tested with `apt install ffmpeg` - the script now handles existing Timeshift processes gracefully instead of aborting the entire APT operation.

## Key Takeaways
- Always implement graceful process handling in system scripts
- **Interactive prompts greatly improve user experience when automation fails**
- Provide configuration options for different operational scenarios
- Use proper error handling instead of `set -e` for complex scripts
- Include fallback mechanisms for critical system operations
- **Timeout protection prevents indefinite hangs in critical system scripts**
- Document configuration options for future maintenance

## Interactive Features Added
1. **Smart Terminal Detection**: Only prompts when in interactive sessions
2. **User-Friendly Options**: Clear choices with explanations of consequences
3. **Flexible Timeout**: 30-second default with option to wait longer
4. **Bypass Capability**: Users can override snapshot failures when needed
5. **Non-Interactive Fallback**: Graceful degradation for automated systems

## Future Considerations
- Monitor the auto-update-snapshots.log for any recurring issues
- Consider adding process cleanup on system boot if stuck processes are frequent
- **Evaluate user feedback on the 30-second timeout - may need adjustment**
- Review snapshot retention policies to ensure disk space management
- **Consider adding notification/email alerts when users bypass snapshots**
- **Track bypass frequency to identify systemic snapshot issues**
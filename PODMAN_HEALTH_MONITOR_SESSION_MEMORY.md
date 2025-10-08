# Podman Health Monitor Implementation - Session Memory

## Overview
This document captures the complete implementation of a Podman health monitoring system with automatic repair and email notifications. The session involved extensive troubleshooting of podman access in a shared rootless environment and building a comprehensive email notification system.

## Environment Details
- **Platform**: whatbox.ca shared hosting
- **User**: advser (non-root user)
- **Podman Setup**: Rootless podman installation
- **Container Count**: 7 active containers (filebrowser, samba, librespeed, claude-code, etc.)
- **Podman Location**: `/usr/bin/podman` (confirmed working in interactive shell)
- **Script Location**: `/home/advser/syncthing/auto/scripts/podman_health_monitor.sh`

## Final Working Solution

### Script Features
- **Automatic Detection**: Monitors for `level=error` in podman output
- **Auto-Repair**: Uses `podman system migrate` with configurable retry attempts (default: 10)
- **Email Notifications**: HTML emails with complete command outputs and repair results
- **Default Email Fallback**: teamit@partsfortechs.com with EMAIL_TO override capability
- **Multiple Operation Modes**: Normal, dry-run, test-email, always-email

### Working Cron Configuration
```bash
# Production mode (only emails on actual issues):
* * * * * /home/advser/syncthing/auto/scripts/podman_health_monitor.sh >/dev/null 2>&1

# Debug mode (emails every minute showing health status):
* * * * * /home/advser/syncthing/auto/scripts/podman_health_monitor.sh --always-email >/dev/null 2>&1

# Custom email recipient:
* * * * * EMAIL_TO="admin@company.com" /home/advser/syncthing/auto/scripts/podman_health_monitor.sh >/dev/null 2>&1
```

### Final Podman Command Configuration
```bash
# Simple approach that works in cron environment:
PODMAN_CMD="podman"

# With comprehensive PATH:
export PATH="$HOME/bin:/home/advser/bin:/usr/local/sbin:/usr/local/bin:/usr/bin:/opt/bin:/usr/lib/llvm/20/bin:/usr/lib/llvm/18/bin:/bin"
```

## Troubleshooting Journey & Attempts

### Issue 1: Podman Path Problems

#### **Failed Attempts:**
1. **Hardcoded `/usr/bin/podman`**: Script couldn't find podman at this path when running via cron
   ```bash
   PODMAN_CMD="/usr/bin/podman"
   # Result: "/usr/bin/podman: No such file or directory"
   ```

2. **Complex Path Detection Logic**: Tried multiple fallback methods
   ```bash
   # Method 1: command -v podman
   # Method 2: Check common locations  
   # Method 3: Manual PATH search
   # Result: Still failed to find podman in cron environment
   ```

3. **User Switching with `su`**: Attempted to switch from root to advser user
   ```bash
   exec su - advser -c "$0 $*"
   # Result: Complex execution path, didn't resolve the core issue
   ```

4. **User Switching with `runuser`**: Tried alternative user switching
   ```bash
   exec runuser -l advser -c "cd /home/advser && $0 $*"
   # Result: "runuser: not found" - command not available
   ```

#### **Root Cause Discovery:**
- Script was running as root user when executed via cron
- Podman was only accessible to user `advser`
- Different PATH environment between interactive shell and cron execution
- Claude Code environment (container) vs host environment confusion

#### **Successful Solution:**
```bash
# Simple approach - let system find podman in PATH
PODMAN_CMD="podman"

# Ensure proper PATH is set
export PATH="$HOME/bin:/home/advser/bin:/usr/local/sbin:/usr/local/bin:/usr/bin:/opt/bin:/usr/lib/llvm/20/bin:/usr/lib/llvm/18/bin:/bin"
```

### Issue 2: Email System Implementation

#### **Successful Implementation:**
1. **Default Email Fallback**: Hardcoded teamit@partsfortechs.com in send_email.py
2. **Environment Variable Override**: EMAIL_TO can override default
3. **SMTP Configuration**: Uses existing smtp_config.json from PS1 scripts
4. **HTML Email Templates**: Professional styling with command output sections

#### **Email Types Implemented:**
- **SUCCESS**: Issues detected and automatically resolved
- **FAILURE**: Issues detected but repair failed
- **HEALTHY**: All containers running normally (debug mode only)

### Issue 3: Command Output Integration

#### **Successful Implementation:**
- Real-time capture of all podman commands during repair process
- Formatted display in email with monospace styling
- Complete visibility from initial error through final verification

#### **Command Sequence Captured:**
1. Initial `podman ps` showing errors
2. Each `podman system migrate` attempt with results
3. `podman start --all` container restart
4. Final `podman ps -a` verification

## Key Learnings & Best Practices

### Rootless Podman on Shared Hosting
1. **User Context is Critical**: Podman must run as the user who installed it
2. **Simple PATH Approach**: Let system find podman rather than hardcoding paths
3. **Environment Variables**: Ensure full PATH is available in cron context
4. **No Sudo Required**: Proper PATH setup eliminates need for user switching

### Cron Best Practices for Shared Hosting
```bash
# Working cron setup for shared rootless podman:
* * * * * /full/path/to/script.sh >/dev/null 2>&1

# Key requirements:
# - Full script path
# - Proper PATH set in script
# - Run as the same user who can access podman
# - No sudo/su needed if properly configured
```

### Email System Architecture
- **Centralized SMTP Config**: Shared smtp_config.json between scripts
- **Python Email Script**: Reusable send_email.py with fallback logic
- **Environment Variable Flexibility**: EMAIL_TO override for different use cases
- **HTML Templates**: Professional appearance with CSS styling

## File Structure
```
/home/advser/syncthing/auto/scripts/
├── podman_health_monitor.sh           # Main monitoring script
├── send_email.py                      # Email sending utility
├── smtp_config.json                   # SMTP configuration
├── test_podman_path.sh               # Debugging utility
└── PODMAN_HEALTH_MONITOR_SESSION_MEMORY.md # This documentation
```

## Usage Examples

### Production Deployment
```bash
# Add to crontab for automatic monitoring:
crontab -e
* * * * * /home/advser/syncthing/auto/scripts/podman_health_monitor.sh >/dev/null 2>&1
```

### Manual Testing
```bash
# Test email templates:
./podman_health_monitor.sh --test-email

# Preview repair actions:
./podman_health_monitor.sh --dry-run

# Force email notifications (temporary):
./podman_health_monitor.sh --always-email
```

### Custom Email Recipients
```bash
# One-time custom recipient:
EMAIL_TO="admin@company.com" ./podman_health_monitor.sh

# Cron with custom recipient:
* * * * * EMAIL_TO="admin@company.com" /home/advser/syncthing/auto/scripts/podman_health_monitor.sh >/dev/null 2>&1
```

## Critical Success Factors

1. **Correct User Context**: Script must run as user with podman access
2. **Proper PATH Configuration**: Include all directories where podman might be found
3. **Simple Command Resolution**: Use `podman` not `/usr/bin/podman`
4. **Comprehensive Email System**: Default fallback with override capability
5. **Real Command Output**: Capture actual podman commands for transparency

## Future Considerations

### Potential Enhancements
- Add configuration file for customizable settings
- Implement retry logic for email sending failures
- Add support for multiple notification channels (Slack, Discord, etc.)
- Include container-specific health checks
- Add metrics collection and trending

### Monitoring & Maintenance
- Review logs regularly: `/home/advser/podman/last-run.log`
- Monitor email delivery success rates
- Update SMTP credentials as needed
- Test script functionality after system updates

## Troubleshooting Quick Reference

### Common Issues & Solutions
1. **"podman: command not found"**
   - Verify PATH includes podman location
   - Check user context (should run as advser)
   - Confirm podman works in interactive shell

2. **"Email send failed"**
   - Verify smtp_config.json exists and is readable
   - Check SMTP credentials and server settings
   - Test send_email.py directly

3. **"No issues detected" but containers are down**
   - Verify error detection logic (looks for "level=error")
   - Check if podman ps output format changed
   - Review LOG_FILE for detailed output

### Debug Commands
```bash
# Test podman access:
./test_podman_path.sh

# Test email system:
echo "test" | python3 send_email.py "" "Test Subject" --config smtp_config.json --stdin

# Manual script execution with debug:
./podman_health_monitor.sh --always-email

# Check recent logs:
tail -20 /home/advser/podman/last-run.log
```

## Session Conclusion

The implementation successfully created a robust podman health monitoring system that:
- Automatically detects and repairs podman runtime issues
- Provides comprehensive email notifications with full command visibility
- Works reliably in a shared hosting rootless podman environment
- Requires no special privileges or user switching mechanisms
- Integrates seamlessly with existing cron infrastructure

The key breakthrough was recognizing that the complex path detection and user switching approaches were unnecessary - the simple approach of using `podman` with proper PATH configuration works perfectly in the shared hosting environment.
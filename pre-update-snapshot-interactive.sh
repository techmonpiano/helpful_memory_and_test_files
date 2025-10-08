#!/bin/bash

# Pre-Update Snapshot Script
# Creates BTRFS snapshot before automatic updates
# Priority: snapper > timeshift > abort

# Load configuration
CONFIG_FILE="/etc/default/pre-update-snapshot"
if [ -f "$CONFIG_FILE" ]; then
    source "$CONFIG_FILE"
fi

# Configuration (can be overridden in /etc/default/pre-update-snapshot)
LOG_FILE="${LOG_FILE:-/var/log/auto-update-snapshots.log}"
MIN_FREE_SPACE_PERCENT="${MIN_FREE_SPACE_PERCENT:-10}"
SNAPSHOT_DESCRIPTION="Auto-update pre-snapshot $(date '+%Y-%m-%d %H:%M:%S')"
PROCESS_WAIT_TIMEOUT="${PROCESS_WAIT_TIMEOUT:-300}"
ALLOW_SKIP_SNAPSHOTS="${ALLOW_SKIP_SNAPSHOTS:-false}"
KILL_STUCK_PROCESSES="${KILL_STUCK_PROCESSES:-false}"
INTERACTIVE_TIMEOUT="${INTERACTIVE_TIMEOUT:-30}"
ENABLE_INTERACTIVE_PROMPT="${ENABLE_INTERACTIVE_PROMPT:-true}"

# Logging function
log_message() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" | tee -a "$LOG_FILE"
}

# Check if we're on BTRFS
check_btrfs() {
    if ! df -T / | grep -q btrfs; then
        log_message "ERROR: Root filesystem is not BTRFS - snapshots not possible"
        return 1
    fi
    return 0
}

# Check if a process is running and how long it's been running
check_process_age() {
    local process_name="$1"
    local pid=$(pgrep -f "$process_name" | head -1)
    
    if [ -z "$pid" ]; then
        return 1  # Process not running
    fi
    
    # Get process start time in seconds since epoch
    local start_time=$(stat -c %Y /proc/$pid 2>/dev/null || echo 0)
    local current_time=$(date +%s)
    local age=$((current_time - start_time))
    
    echo "$pid:$age"
    return 0
}

# Prompt user for decision with timeout
prompt_user_bypass() {
    local tool_name="$1"
    local timeout="$2"
    
    if [ "$ENABLE_INTERACTIVE_PROMPT" != "true" ]; then
        return 1  # Don't prompt if disabled
    fi
    
    # Check if we're in an interactive terminal
    if [ ! -t 0 ] || [ ! -t 1 ]; then
        log_message "INFO: Non-interactive session, cannot prompt user"
        return 1
    fi
    
    echo ""
    echo "⚠️  SNAPSHOT TIMEOUT: $tool_name failed to complete within ${timeout}s"
    echo "   This may prevent package installation from proceeding."
    echo ""
    echo "Options:"
    echo "  y/Y - Bypass snapshots and continue with package installation"
    echo "  n/N - Abort package installation (default)"
    echo "  w/W - Wait another ${timeout}s for $tool_name to complete"
    echo ""
    
    local response
    read -t 30 -p "Decision [y/n/w]: " response
    
    case "${response,,}" in  # Convert to lowercase
        y|yes)
            log_message "INFO: User chose to bypass snapshots and continue"
            return 0
            ;;
        w|wait)
            log_message "INFO: User chose to wait longer for $tool_name"
            return 2
            ;;
        *)
            log_message "INFO: User chose to abort or no response - aborting installation"
            return 1
            ;;
    esac
}

# Wait for existing processes to complete or handle them
handle_existing_processes() {
    local tool_name="$1"
    local process_info
    
    if process_info=$(check_process_age "$tool_name"); then
        local pid=$(echo "$process_info" | cut -d: -f1)
        local age=$(echo "$process_info" | cut -d: -f2)
        
        log_message "INFO: Found existing $tool_name process (PID: $pid, age: ${age}s)"
        
        # If process is very old and we're allowed to kill stuck processes
        if [ "$age" -gt 3600 ] && [ "$KILL_STUCK_PROCESSES" = "true" ]; then
            log_message "WARNING: $tool_name process appears stuck (running for ${age}s), attempting to terminate"
            if kill -TERM "$pid" 2>/dev/null; then
                sleep 5
                if kill -0 "$pid" 2>/dev/null; then
                    log_message "WARNING: Force killing stuck $tool_name process"
                    kill -KILL "$pid" 2>/dev/null || true
                fi
                sleep 2
            fi
        else
            # Wait for process to complete with interactive timeout
            log_message "INFO: Waiting up to ${INTERACTIVE_TIMEOUT}s for $tool_name to complete"
            local waited=0
            while [ $waited -lt "$INTERACTIVE_TIMEOUT" ] && kill -0 "$pid" 2>/dev/null; do
                sleep 5
                waited=$((waited + 5))
            done
            
            if kill -0 "$pid" 2>/dev/null; then
                log_message "WARNING: $tool_name still running after ${INTERACTIVE_TIMEOUT}s timeout"
                
                # Prompt user for decision
                local user_choice
                while true; do
                    prompt_user_bypass "$tool_name" "$INTERACTIVE_TIMEOUT"
                    user_choice=$?
                    
                    case $user_choice in
                        0)  # Bypass
                            return 2  # Special return code for bypass
                            ;;
                        1)  # Abort
                            return 1
                            ;;
                        2)  # Wait more
                            log_message "INFO: Waiting another ${INTERACTIVE_TIMEOUT}s for $tool_name"
                            local extra_waited=0
                            while [ $extra_waited -lt "$INTERACTIVE_TIMEOUT" ] && kill -0 "$pid" 2>/dev/null; do
                                sleep 5
                                extra_waited=$((extra_waited + 5))
                            done
                            
                            if ! kill -0 "$pid" 2>/dev/null; then
                                log_message "INFO: $tool_name process completed during extended wait"
                                return 0
                            fi
                            # Continue loop to prompt again
                            ;;
                    esac
                done
            else
                log_message "INFO: $tool_name process completed"
            fi
        fi
    fi
    
    return 0
}

# Check available disk space
check_disk_space() {
    local available_percent=$(df / | awk 'NR==2 {print int((100-$5))}')
    if [ "$available_percent" -lt "$MIN_FREE_SPACE_PERCENT" ]; then
        log_message "ERROR: Insufficient disk space (${available_percent}% free, need ${MIN_FREE_SPACE_PERCENT}%)"
        return 1
    fi
    log_message "INFO: Disk space check passed (${available_percent}% free)"
    return 0
}

# Create snapshot with snapper
create_snapper_snapshot() {
    if command -v snapper >/dev/null 2>&1; then
        log_message "INFO: Creating snapshot with snapper"
        if timeout "$INTERACTIVE_TIMEOUT" snapper create --description "$SNAPSHOT_DESCRIPTION" --cleanup-algorithm timeline; then
            log_message "SUCCESS: Snapper snapshot created successfully"
            return 0
        else
            log_message "ERROR: Snapper snapshot creation failed or timed out"
            
            # Prompt user if snapper itself fails
            if [ "$ENABLE_INTERACTIVE_PROMPT" = "true" ]; then
                prompt_user_bypass "snapper snapshot creation" "$INTERACTIVE_TIMEOUT"
                case $? in
                    0)  # Bypass
                        log_message "INFO: User chose to bypass failed snapper snapshot"
                        return 2
                        ;;
                    *)  # Abort or wait (but waiting won't help if creation failed)
                        return 1
                        ;;
                esac
            fi
            return 1
        fi
    else
        return 1
    fi
}

# Create snapshot with timeshift
create_timeshift_snapshot() {
    if command -v timeshift >/dev/null 2>&1; then
        # Check for existing timeshift processes
        local handle_result
        handle_existing_processes "timeshift"
        handle_result=$?
        
        case $handle_result in
            0)  # Process handled successfully
                ;;
            1)  # Process handling failed
                log_message "ERROR: Unable to proceed due to existing timeshift process"
                return 1
                ;;
            2)  # User chose to bypass
                log_message "INFO: User chose to bypass timeshift snapshot"
                return 2
                ;;
        esac
        
        log_message "INFO: Creating snapshot with timeshift"
        if timeout "$INTERACTIVE_TIMEOUT" timeshift --create --comments "$SNAPSHOT_DESCRIPTION" --scripted; then
            log_message "SUCCESS: Timeshift snapshot created successfully"
            return 0
        else
            log_message "ERROR: Timeshift snapshot creation failed or timed out"
            
            # Prompt user if timeshift itself fails
            if [ "$ENABLE_INTERACTIVE_PROMPT" = "true" ]; then
                prompt_user_bypass "timeshift snapshot creation" "$INTERACTIVE_TIMEOUT"
                case $? in
                    0)  # Bypass
                        log_message "INFO: User chose to bypass failed timeshift snapshot"
                        return 2
                        ;;
                    *)  # Abort or wait (but waiting won't help if creation failed)
                        return 1
                        ;;
                esac
            fi
            return 1
        fi
    else
        return 1
    fi
}

# Main execution
main() {
    log_message "INFO: Starting pre-update snapshot process"
    
    # Check if snapshots are disabled
    if [ "$ALLOW_SKIP_SNAPSHOTS" = "true" ] && [ -n "$SKIP_SNAPSHOTS" ]; then
        log_message "INFO: Snapshots disabled via SKIP_SNAPSHOTS environment variable"
        exit 0
    fi
    
    # Perform safety checks
    if ! check_btrfs; then
        if [ "$ALLOW_SKIP_SNAPSHOTS" = "true" ]; then
            log_message "WARNING: Not on BTRFS filesystem, proceeding without snapshots"
            exit 0
        else
            exit 1
        fi
    fi
    
    if ! check_disk_space; then
        log_message "ERROR: Insufficient disk space for snapshots"
        exit 1
    fi
    
    # Try snapshot tools in priority order
    local snapshot_created=false
    local user_bypass=false
    
    # Try snapper first
    local snapper_result
    create_snapper_snapshot
    snapper_result=$?
    if [ $snapper_result -eq 0 ]; then
        log_message "INFO: Pre-update snapshot completed with snapper"
        snapshot_created=true
    elif [ $snapper_result -eq 2 ]; then
        log_message "INFO: User chose to bypass snapper snapshot"
        user_bypass=true
    fi
    
    # Try timeshift if snapper didn't work and user didn't choose to bypass
    if [ "$snapshot_created" = "false" ] && [ "$user_bypass" = "false" ]; then
        local timeshift_result
        create_timeshift_snapshot
        timeshift_result=$?
        if [ $timeshift_result -eq 0 ]; then
            log_message "INFO: Pre-update snapshot completed with timeshift"
            snapshot_created=true
        elif [ $timeshift_result -eq 2 ]; then
            log_message "INFO: User chose to bypass timeshift snapshot"
            user_bypass=true
        fi
    fi
    
    # Determine final action
    if [ "$snapshot_created" = "true" ]; then
        exit 0
    elif [ "$user_bypass" = "true" ]; then
        log_message "WARNING: Proceeding without snapshots due to user choice"
        exit 0
    else
        log_message "ERROR: No snapshot tool available or all failed"
        if [ "$ALLOW_SKIP_SNAPSHOTS" = "true" ]; then
            log_message "WARNING: Proceeding without snapshots due to configuration"
            exit 0
        else
            log_message "ERROR: Aborting updates for safety"
            exit 1
        fi
    fi
}

# Create log directory if it doesn't exist
mkdir -p "$(dirname "$LOG_FILE")"

# Run main function
main "$@"
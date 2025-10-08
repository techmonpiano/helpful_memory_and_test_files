#!/bin/bash

# =============================================================================
# Fully Automated MCP SSH Session Creator
# =============================================================================
# Purpose: One command creates complete persistent SSH session for LLM
# Usage: ~/shawndev1/helpful_memory_and_test_files/auto-mcp-ssh-complete.sh [target]
# Output: PID ready for interact_with_process usage
# =============================================================================

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Default configuration
DEFAULT_PORT="22"
LOG_DIR="/tmp"
UNIVERSAL_RUNNER_PATH="$HOME/shawndev1/universal_env_runner/universal_env_runner.py"

# Predefined server configurations
declare -A PREDEFINED_SERVERS=(
    ["zencart"]="partsfor@ftp.partsfortechs.com:2022"
    ["runtipi"]="user1@runtipi1.tail1da69.ts.net:22"
    ["runtipi1"]="user1@runtipi1.tail1da69.ts.net:22"
)

print_banner() {
    echo -e "${CYAN}=================================================================${NC}"
    echo -e "${CYAN}  Fully Automated MCP SSH Session Creator v2.0.0${NC}"
    echo -e "${CYAN}  One command - Complete persistent SSH session${NC}"
    echo -e "${CYAN}=================================================================${NC}"
}

print_help() {
    cat << 'EOF'
USAGE:
    ./auto-mcp-ssh-complete.sh [target] [options]

TARGETS:
    user@server[:port]     - Direct SSH connection
    zencart               - Zencart production server (partsfor@ftp.partsfortechs.com:2022)
    runtipi|runtipi1      - Runtipi1 server (user1@runtipi1.tail1da69.ts.net:22)

OPTIONS:
    -p, --port PORT       - SSH port (default: 22)
    -l, --log-dir DIR     - Log directory (default: /tmp)
    -n, --no-gui          - Skip GUI log file opening
    -q, --quiet           - Minimal output (just PID)
    -v, --verbose         - Detailed output
    -h, --help            - Show this help

EXAMPLES:
    ./auto-mcp-ssh-complete.sh zencart           # Complete Zencart session
    ./auto-mcp-ssh-complete.sh runtipi           # Complete Runtipi session  
    ./auto-mcp-ssh-complete.sh user@server.com   # Complete custom session
    ./auto-mcp-ssh-complete.sh zencart -q        # Quiet mode (just PID)

OUTPUT:
    Returns PID ready for: interact_with_process(PID, "commands", timeout_ms=8000)

LLM USAGE:
    Just run the script and use the returned PID with interact_with_process()
EOF
}

log_info() {
    if [[ "$QUIET" != "true" ]]; then
        echo -e "${GREEN}[INFO]${NC} $1"
    fi
}

log_warn() {
    if [[ "$QUIET" != "true" ]]; then
        echo -e "${YELLOW}[WARN]${NC} $1"
    fi
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

log_debug() {
    if [[ "$VERBOSE" == "true" ]]; then
        echo -e "${BLUE}[DEBUG]${NC} $1"
    fi
}

parse_target() {
    local target="$1"
    
    # Check if it's a predefined server
    if [[ -n "${PREDEFINED_SERVERS[$target]}" ]]; then
        local server_config="${PREDEFINED_SERVERS[$target]}"
        SSH_USER_SERVER="${server_config%:*}"
        SSH_PORT="${server_config##*:}"
        log_debug "Using predefined server '$target': $SSH_USER_SERVER (port $SSH_PORT)"
        return 0
    fi
    
    # Parse user@server[:port] format
    if [[ "$target" =~ ^([^@]+)@([^:]+)(:([0-9]+))?$ ]]; then
        SSH_USER="${BASH_REMATCH[1]}"
        SSH_SERVER="${BASH_REMATCH[2]}"
        SSH_USER_SERVER="$SSH_USER@$SSH_SERVER"
        
        if [[ -n "${BASH_REMATCH[4]}" ]]; then
            SSH_PORT="${BASH_REMATCH[4]}"
        else
            SSH_PORT="$DEFAULT_PORT"
        fi
        
        log_debug "Parsed target: $SSH_USER_SERVER (port $SSH_PORT)"
        return 0
    fi
    
    log_error "Invalid target format: $target"
    log_error "Expected: user@server[:port] or predefined server name"
    return 1
}

generate_log_filename() {
    local timestamp=$(date '+%Y%m%d_%H%M%S')
    LOG_FILENAME="$LOG_DIR/ssh_session_${timestamp}.log"
    log_debug "Generated log filename: $LOG_FILENAME"
}

cleanup_old_logs() {
    log_debug "Cleaning up old SSH session logs..."
    find "$LOG_DIR" -name "ssh_session_*.log" -mtime +7 -delete 2>/dev/null || true
}

open_log_file_gui() {
    if [[ "$NO_GUI" == "true" ]]; then
        log_debug "GUI opening skipped (--no-gui specified)"
        return 0
    fi
    
    if [[ ! -f "$UNIVERSAL_RUNNER_PATH" ]]; then
        log_warn "Universal Environment Runner not found - GUI log viewing unavailable"
        return 1
    fi
    
    log_debug "Opening log file in GUI application..."
    
    # Try enhanced xdg-open first (background process)
    python3 "$UNIVERSAL_RUNNER_PATH" xdg-open "$LOG_FILENAME" > /dev/null 2>&1 &
    
    # Brief delay to let it start
    sleep 1
    
    # Check if it worked by looking for the process
    if pgrep -f "$LOG_FILENAME" > /dev/null 2>&1; then
        log_debug "✅ Log file opened successfully in GUI application"
    else
        log_debug "Primary method may have failed, trying VS Code fallback..."
        python3 "$UNIVERSAL_RUNNER_PATH" codium "$LOG_FILENAME" > /dev/null 2>&1 &
        sleep 1
        
        if ! pgrep -f "$LOG_FILENAME" > /dev/null 2>&1; then
            log_debug "VS Code unavailable, trying gedit fallback..."
            python3 "$UNIVERSAL_RUNNER_PATH" gedit "$LOG_FILENAME" > /dev/null 2>&1 &
        fi
    fi
}

create_ssh_session() {
    log_info "Creating persistent SSH session..."
    
    # 1. Generate log filename
    generate_log_filename
    
    # 2. Clean up old logs
    cleanup_old_logs
    
    # 3. Create session script
    local session_script=$(mktemp)
    cat > "$session_script" << EOF
#!/bin/bash

# Setup real-time logging with tee (no buffering)
exec > >(tee -a "$LOG_FILENAME") 2>&1

# Log session start
echo "# SSH Session Log"
echo "# Target: $SSH_USER_SERVER:$SSH_PORT"
echo "# Started: \$(date)"
echo "# Script: auto-mcp-ssh-complete.sh v2.0.0"
echo "# ================================================================"
echo

# Start SSH connection
echo "Starting SSH session - \$(date)"
echo "Target: $SSH_USER_SERVER:$SSH_PORT"
echo "================================================================"

# Build and execute SSH command
if [[ "$SSH_PORT" != "22" ]]; then
    ssh -T -p $SSH_PORT $SSH_USER_SERVER
else
    ssh -T $SSH_USER_SERVER
fi
EOF
    
    chmod +x "$session_script"
    
    # 4. Start the session in background
    bash "$session_script" &
    local ssh_pid=$!
    
    # 5. Wait for connection to establish and check for success indicators
    local connection_attempts=0
    local max_attempts=10
    local connection_success=false
    
    while [[ $connection_attempts -lt $max_attempts ]]; do
        sleep 1
        ((connection_attempts++))
        
        # Check if log file shows successful connection (login banner or prompt)
        if [[ -f "$LOG_FILENAME" ]] && grep -q -E "(Linux|Ubuntu|Debian|Welcome|Last login|\$ |# |user@)" "$LOG_FILENAME" 2>/dev/null; then
            connection_success=true
            log_debug "✅ SSH connection successful - detected login indicators"
            break
        fi
        
        # Also check if process still exists (but don't fail immediately if it doesn't)
        if ! kill -0 "$ssh_pid" 2>/dev/null; then
            log_debug "SSH process exited, checking if connection was successful..."
            # Give it one more second to see if success indicators appear in log
            sleep 1
            if [[ -f "$LOG_FILENAME" ]] && grep -q -E "(Linux|Ubuntu|Debian|Welcome|Last login|\$ |# |user@)" "$LOG_FILENAME" 2>/dev/null; then
                connection_success=true
                log_debug "✅ SSH connection was successful despite process exit"
                break
            fi
        fi
    done
    
    # 6. Final connection check
    if [[ "$connection_success" != "true" ]]; then
        log_error "SSH connection failed - no success indicators found after $max_attempts seconds"
        log_error "Check log file for details: $LOG_FILENAME"
        rm -f "$session_script"
        return 1
    fi
    
    # 7. Open log file in GUI
    open_log_file_gui
    
    # 8. Clean up temp script
    rm -f "$session_script"
    
    # 9. Output results
    if [[ "$QUIET" == "true" ]]; then
        echo "$ssh_pid"
    else
        echo -e "${CYAN}=================================================================${NC}"
        echo -e "${GREEN}✅ SSH Session Created Successfully!${NC}"
        echo -e "${CYAN}=================================================================${NC}"
        echo -e "${YELLOW}Target:${NC} $SSH_USER_SERVER:$SSH_PORT"
        echo -e "${YELLOW}Log File:${NC} $LOG_FILENAME"
        echo -e "${YELLOW}Session PID:${NC} $ssh_pid"
        echo
        echo -e "${GREEN}Ready for LLM interaction:${NC}"
        echo -e "${CYAN}interact_with_process($ssh_pid, \"your_command_here\", timeout_ms=8000)${NC}"
        echo
        echo -e "${BLUE}Session Management:${NC}"
        echo "- list_sessions()                                    # Check session status"
        echo "- read_process_output($ssh_pid, timeout_ms=5000)          # Read pending output"
        echo "- force_terminate($ssh_pid)                               # End session"
        echo -e "${CYAN}=================================================================${NC}"
    fi
    
    return 0
}

main() {
    # Initialize variables
    VERBOSE="false"
    NO_GUI="false" 
    QUIET="false"
    SSH_PORT="$DEFAULT_PORT"
    
    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            -h|--help)
                print_help
                exit 0
                ;;
            -p|--port)
                SSH_PORT="$2"
                shift 2
                ;;
            -l|--log-dir)
                LOG_DIR="$2"
                shift 2
                ;;
            -n|--no-gui)
                NO_GUI="true"
                shift
                ;;
            -q|--quiet)
                QUIET="true"
                shift
                ;;
            -v|--verbose)
                VERBOSE="true"
                shift
                ;;
            -*)
                log_error "Unknown option: $1"
                echo "Use --help for usage information"
                exit 1
                ;;
            *)
                if [[ -z "$TARGET" ]]; then
                    TARGET="$1"
                else
                    log_error "Multiple targets specified: $TARGET and $1"
                    exit 1
                fi
                shift
                ;;
        esac
    done
    
    # Check if target was provided
    if [[ -z "$TARGET" ]]; then
        if [[ "$QUIET" != "true" ]]; then
            print_banner
            echo
        fi
        log_error "No target specified"
        if [[ "$QUIET" != "true" ]]; then
            echo
            print_help
        fi
        exit 1
    fi
    
    # Parse and validate target
    if ! parse_target "$TARGET"; then
        exit 1
    fi
    
    # Print banner in verbose mode
    if [[ "$VERBOSE" == "true" ]]; then
        print_banner
        echo
    fi
    
    # Create SSH session
    if ! create_ssh_session; then
        exit 1
    fi
}

# Script entry point
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    # Trap Ctrl+C for clean exit
    trap 'log_warn "Session creation aborted by user"; exit 130' INT
    
    # Run main function with all arguments
    main "$@"
else
    log_error "This script should be executed, not sourced"
    exit 1
fi

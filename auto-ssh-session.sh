#!/bin/bash

# =============================================================================
# Auto SSH Session with Real-time Logging & GUI Integration
# =============================================================================
# Purpose: Automated SSH session establishment with real-time logging for LLMs
# Usage: ./auto-ssh-session.sh [user@server] [port] [options]
# Compatible: Any LLM with MCP support (Claude, ChatGPT, Gemini, etc.)
# =============================================================================

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Script version and info
SCRIPT_VERSION="2.0.0"
SCRIPT_DATE="2025-09-10"

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

# =============================================================================
# Helper Functions
# =============================================================================

print_banner() {
    echo -e "${CYAN}=================================================================${NC}"
    echo -e "${CYAN}  Auto SSH Session with Real-time Logging v${SCRIPT_VERSION}${NC}"
    echo -e "${CYAN}  Compatible with any LLM MCP environment${NC}"
    echo -e "${CYAN}=================================================================${NC}"
}

print_help() {
    cat << 'EOF'
USAGE:
    ./auto-ssh-session.sh [target] [options]

TARGETS:
    user@server[:port]     - Direct SSH connection
    zencart               - Zencart production server (partsfor@ftp.partsfortechs.com:2022)
    runtipi|runtipi1      - Runtipi1 server (user1@runtipi1.tail1da69.ts.net:22)

OPTIONS:
    -p, --port PORT       - SSH port (default: 22)
    -l, --log-dir DIR     - Log directory (default: /tmp)
    -n, --no-gui          - Skip GUI log file opening
    -k, --keep-logs       - Don't clean up old log files
    -v, --verbose         - Verbose output
    -h, --help            - Show this help

EXAMPLES:
    ./auto-ssh-session.sh zencart                    # Connect to Zencart production
    ./auto-ssh-session.sh runtipi                    # Connect to Runtipi1 server  
    ./auto-ssh-session.sh user@myserver.com          # Connect to custom server
    ./auto-ssh-session.sh user@server.com -p 2022    # Custom server with port
    ./auto-ssh-session.sh zencart --no-gui           # No GUI log viewing
    ./auto-ssh-session.sh runtipi -v                 # Verbose mode

LOG FILES:
    Format: ssh_session_YYYYMMDD_HHMMSS.log
    Location: /tmp/ (or specified with --log-dir)
    Real-time: Updates immediately with tee method

INTEGRATION:
    For LLM MCP tools:
    start_process("~/shawndev1/helpful_memory_and_test_files/auto-ssh-session.sh zencart", timeout_ms=15000)
EOF
}

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

log_debug() {
    if [[ "$VERBOSE" == "true" ]]; then
        echo -e "${BLUE}[DEBUG]${NC} $1"
    fi
}

# =============================================================================
# Configuration Functions
# =============================================================================

parse_target() {
    local target="$1"
    
    # Check if it's a predefined server
    if [[ -n "${PREDEFINED_SERVERS[$target]}" ]]; then
        local server_config="${PREDEFINED_SERVERS[$target]}"
        SSH_USER_SERVER="${server_config%:*}"
        SSH_PORT="${server_config##*:}"
        log_info "Using predefined server '$target': $SSH_USER_SERVER (port $SSH_PORT)"
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
        
        log_info "Parsed target: $SSH_USER_SERVER (port $SSH_PORT)"
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
    if [[ "$KEEP_LOGS" != "true" ]]; then
        log_info "Cleaning up old SSH session logs..."
        find "$LOG_DIR" -name "ssh_session_*.log" -mtime +7 -delete 2>/dev/null || true
        log_debug "Cleaned up logs older than 7 days"
    fi
}

# =============================================================================
# SSH Session Functions
# =============================================================================

setup_logging() {
    log_info "Setting up real-time logging with tee method..."
    
    # Create log file with header
    cat > "$LOG_FILENAME" << EOF
# SSH Session Log
# Target: $SSH_USER_SERVER:$SSH_PORT
# Started: $(date)
# Script: auto-ssh-session.sh v$SCRIPT_VERSION
# ================================================================

EOF
    
    # Setup tee for real-time logging (no buffering issues!)
    exec > >(tee -a "$LOG_FILENAME") 2>&1
    
    log_info "Real-time logging active: $LOG_FILENAME"
}

build_ssh_command() {
    SSH_COMMAND="ssh -T"
    
    # Add port if not default
    if [[ "$SSH_PORT" != "22" ]]; then
        SSH_COMMAND="$SSH_COMMAND -p $SSH_PORT"
    fi
    
    SSH_COMMAND="$SSH_COMMAND $SSH_USER_SERVER"
    
    log_debug "SSH command: $SSH_COMMAND"
}

establish_ssh_connection() {
    log_info "Establishing SSH connection..."
    echo "Starting SSH session - $(date)"
    echo "Target: $SSH_USER_SERVER:$SSH_PORT"
    echo "Command: $SSH_COMMAND"
    echo "================================================================"
    
    # Execute SSH connection
    exec $SSH_COMMAND
}

# =============================================================================
# GUI Integration Functions
# =============================================================================

open_log_file_gui() {
    if [[ "$NO_GUI" == "true" ]]; then
        log_info "GUI opening skipped (--no-gui specified)"
        return 0
    fi
    
    if [[ ! -f "$UNIVERSAL_RUNNER_PATH" ]]; then
        log_warn "Universal Environment Runner not found at: $UNIVERSAL_RUNNER_PATH"
        log_warn "GUI log viewing unavailable - install Universal Environment Runner"
        return 1
    fi
    
    log_info "Opening log file in GUI application..."
    
    # Try enhanced xdg-open first (2025-09-08 enhancement)
    log_debug "Attempting enhanced xdg-open via Universal Environment Runner..."
    python3 "$UNIVERSAL_RUNNER_PATH" xdg-open "$LOG_FILENAME" &
    
    # Brief delay to let it start
    sleep 2
    
    # Check if it worked by looking for the process
    if pgrep -f "$LOG_FILENAME" > /dev/null; then
        log_info "✅ Log file opened successfully in GUI application"
    else
        log_warn "Primary method may have failed, trying VS Code fallback..."
        python3 "$UNIVERSAL_RUNNER_PATH" codium "$LOG_FILENAME" &
        sleep 1
        
        if pgrep -f "$LOG_FILENAME" > /dev/null; then
            log_info "✅ Log file opened in VS Codium"
        else
            log_warn "VS Code unavailable, trying gedit fallback..."
            python3 "$UNIVERSAL_RUNNER_PATH" gedit "$LOG_FILENAME" &
            log_info "✅ Log file opened in gedit (fallback)"
        fi
    fi
}

# =============================================================================
# Main Script Logic
# =============================================================================

main() {
    # Initialize variables
    VERBOSE="false"
    NO_GUI="false"
    KEEP_LOGS="false"
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
            -k|--keep-logs)
                KEEP_LOGS="true"
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
        print_banner
        echo
        log_error "No target specified"
        echo
        print_help
        exit 1
    fi
    
    # Print banner in verbose mode or for help
    if [[ "$VERBOSE" == "true" ]]; then
        print_banner
        echo
    fi
    
    # Main execution flow
    log_info "Starting automated SSH session setup..."
    
    # 1. Parse and validate target
    if ! parse_target "$TARGET"; then
        exit 1
    fi
    
    # 2. Generate log filename
    generate_log_filename
    
    # 3. Clean up old logs
    cleanup_old_logs
    
    # 4. Setup logging
    setup_logging
    
    # 5. Open log file in GUI (background process)
    open_log_file_gui
    
    # 6. Build SSH command
    build_ssh_command
    
    # 7. Final status before connection
    log_info "Configuration complete:"
    log_info "  Target: $SSH_USER_SERVER:$SSH_PORT"
    log_info "  Log file: $LOG_FILENAME"
    log_info "  GUI viewing: $([ "$NO_GUI" == "true" ] && echo "disabled" || echo "enabled")"
    echo
    log_info "Connecting in 2 seconds... (Ctrl+C to abort)"
    sleep 2
    
    # 8. Establish SSH connection (this will replace current process)
    establish_ssh_connection
}

# =============================================================================
# Script Entry Point
# =============================================================================

# Make sure we're not being sourced
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    # Trap Ctrl+C for clean exit
    trap 'log_warn "Connection aborted by user"; exit 130' INT
    
    # Run main function with all arguments
    main "$@"
else
    log_error "This script should be executed, not sourced"
    exit 1
fi

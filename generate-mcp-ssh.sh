#!/bin/bash

# =============================================================================
# MCP SSH Session Command Generator
# =============================================================================
# Purpose: Generate proper MCP tool commands for persistent SSH sessions
# Usage: ./generate-mcp-ssh.sh [target] [options]
# Output: Copy-paste MCP commands for LLM execution
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

# Predefined server configurations
declare -A PREDEFINED_SERVERS=(
    ["zencart"]="partsfor@ftp.partsfortechs.com:2022"
    ["runtipi"]="user1@runtipi1.tail1da69.ts.net:22"
    ["runtipi1"]="user1@runtipi1.tail1da69.ts.net:22"
)

print_banner() {
    echo -e "${CYAN}=================================================================${NC}"
    echo -e "${CYAN}  MCP SSH Session Command Generator v2.0.0${NC}"
    echo -e "${CYAN}  Generates persistent MCP-compatible SSH session commands${NC}"
    echo -e "${CYAN}=================================================================${NC}"
}

print_help() {
    cat << 'EOF'
USAGE:
    ./generate-mcp-ssh.sh [target] [options]

TARGETS:
    user@server[:port]     - Direct SSH connection
    zencart               - Zencart production server (partsfor@ftp.partsfortechs.com:2022)
    runtipi|runtipi1      - Runtipi1 server (user1@runtipi1.tail1da69.ts.net:22)

OPTIONS:
    -p, --port PORT       - SSH port (default: 22)
    -l, --log-dir DIR     - Log directory (default: /tmp)
    -n, --no-gui          - Skip GUI log file opening
    -v, --verbose         - Show detailed explanations
    -j, --javascript      - Output as JavaScript/JSON format
    -h, --help            - Show this help

EXAMPLES:
    ./generate-mcp-ssh.sh zencart                    # Zencart MCP commands
    ./generate-mcp-ssh.sh runtipi -v                 # Runtipi with explanations
    ./generate-mcp-ssh.sh user@myserver.com -j       # JavaScript format
    ./generate-mcp-ssh.sh zencart --no-gui           # Skip GUI opening

OUTPUT:
    Copy-paste ready MCP tool commands for persistent SSH sessions
    Compatible with interact_with_process for ongoing communication
EOF
}

parse_target() {
    local target="$1"
    
    # Check if it's a predefined server
    if [[ -n "${PREDEFINED_SERVERS[$target]}" ]]; then
        local server_config="${PREDEFINED_SERVERS[$target]}"
        SSH_USER_SERVER="${server_config%:*}"
        SSH_PORT="${server_config##*:}"
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
        return 0
    fi
    
    echo -e "${RED}[ERROR]${NC} Invalid target format: $target"
    return 1
}

generate_timestamp() {
    date '+%Y%m%d_%H%M%S'
}

generate_mcp_commands() {
    local timestamp=$(generate_timestamp)
    local log_file="$LOG_DIR/ssh_session_${timestamp}.log"
    
    echo -e "${CYAN}=================================================================${NC}"
    echo -e "${GREEN}MCP SSH Session Commands - Copy and Execute These:${NC}"
    echo -e "${CYAN}=================================================================${NC}"
    echo
    
    if [[ "$VERBOSE" == "true" ]]; then
        echo -e "${YELLOW}# Target: $SSH_USER_SERVER:$SSH_PORT${NC}"
        echo -e "${YELLOW}# Log file: $log_file${NC}"
        echo -e "${YELLOW}# These commands create a persistent SSH session via MCP tools${NC}"
        echo
    fi
    
    if [[ "$JAVASCRIPT" == "true" ]]; then
        generate_javascript_format "$log_file"
    else
        generate_copy_paste_format "$log_file"
    fi
}

generate_copy_paste_format() {
    local log_file="$1"
    
    echo -e "${GREEN}// Step 1: Start bash process for SSH session${NC}"
    echo "start_process(\"bash\", timeout_ms=5000)"
    echo
    echo -e "${YELLOW}// SAVE THE RETURNED PID! Use it in all subsequent commands${NC}"
    echo -e "${YELLOW}// Example: const PID = 12345; (replace with actual PID)${NC}"
    echo
    
    echo -e "${GREEN}// Step 2: Setup real-time logging (replace PID with actual value)${NC}"
    echo "interact_with_process(PID, \"exec > >(tee -a $log_file) 2>&1\", timeout_ms=3000)"
    echo
    
    echo -e "${GREEN}// Step 3: Start SSH connection${NC}"
    if [[ "$SSH_PORT" != "22" ]]; then
        echo "interact_with_process(PID, \"echo 'Starting SSH session - \$(date)' && ssh -T -p $SSH_PORT $SSH_USER_SERVER\", timeout_ms=10000)"
    else
        echo "interact_with_process(PID, \"echo 'Starting SSH session - \$(date)' && ssh -T $SSH_USER_SERVER\", timeout_ms=10000)"
    fi
    echo
    
    echo -e "${GREEN}// Step 4: Test connection and verify session${NC}"
    echo "interact_with_process(PID, \"echo 'Session ready - \$(date)' && pwd && hostname\", timeout_ms=5000)"
    echo
    
    if [[ "$NO_GUI" != "true" ]]; then
        echo -e "${GREEN}// Step 5: Open log file in GUI (optional - run in separate command)${NC}"
        echo "start_process(\"python3 ~/shawndev1/universal_env_runner/universal_env_runner.py xdg-open $log_file\", timeout_ms=10000)"
        echo
    fi
    
    echo -e "${GREEN}// Step 6: Verify logging is working${NC}"
    echo "read_file(\"$log_file\")"
    echo
    
    echo -e "${CYAN}=================================================================${NC}"
    echo -e "${GREEN}✅ SSH session established! Use this PID for all future commands:${NC}"
    echo -e "${YELLOW}interact_with_process(PID, \"your_command_here\", timeout_ms=8000)${NC}"
    echo -e "${CYAN}=================================================================${NC}"
    
    if [[ "$VERBOSE" == "true" ]]; then
        echo
        echo -e "${BLUE}[INFO] Session Management:${NC}"
        echo "- list_sessions()                              # Check session status"
        echo "- read_process_output(PID, timeout_ms=5000)    # Read any pending output"
        echo "- force_terminate(PID)                         # End session when done"
        echo
        echo -e "${BLUE}[INFO] Log File Management:${NC}"
        echo "- read_file(\"$log_file\")                   # View current log content"
        echo "- list_directory(\"$LOG_DIR\")                # See all log files"
    fi
}

generate_javascript_format() {
    local log_file="$1"
    
    echo "{"
    echo "  \"target\": \"$SSH_USER_SERVER:$SSH_PORT\","
    echo "  \"logFile\": \"$log_file\","
    echo "  \"commands\": ["
    echo "    {"
    echo "      \"step\": 1,"
    echo "      \"description\": \"Start bash process\","
    echo "      \"command\": \"start_process('bash', timeout_ms=5000)\","
    echo "      \"note\": \"Save the returned PID for subsequent commands\""
    echo "    },"
    echo "    {"
    echo "      \"step\": 2,"
    echo "      \"description\": \"Setup real-time logging\","
    echo "      \"command\": \"interact_with_process(PID, 'exec > >(tee -a $log_file) 2>&1', timeout_ms=3000)\""
    echo "    },"
    echo "    {"
    echo "      \"step\": 3,"
    echo "      \"description\": \"Start SSH connection\","
    if [[ "$SSH_PORT" != "22" ]]; then
        echo "      \"command\": \"interact_with_process(PID, 'echo \\\"Starting SSH session - \\\$(date)\\\" && ssh -T -p $SSH_PORT $SSH_USER_SERVER', timeout_ms=10000)\""
    else
        echo "      \"command\": \"interact_with_process(PID, 'echo \\\"Starting SSH session - \\\$(date)\\\" && ssh -T $SSH_USER_SERVER', timeout_ms=10000)\""
    fi
    echo "    },"
    echo "    {"
    echo "      \"step\": 4,"
    echo "      \"description\": \"Test connection\","
    echo "      \"command\": \"interact_with_process(PID, 'echo \\\"Session ready - \\\$(date)\\\" && pwd && hostname', timeout_ms=5000)\""
    echo "    }"
    if [[ "$NO_GUI" != "true" ]]; then
        echo "    ,"
        echo "    {"
        echo "      \"step\": 5,"
        echo "      \"description\": \"Open log file in GUI\","
        echo "      \"command\": \"start_process('python3 ~/shawndev1/universal_env_runner/universal_env_runner.py xdg-open $log_file', timeout_ms=10000)\""
        echo "    }"
    fi
    echo "  ]"
    echo "}"
}

main() {
    # Initialize variables
    VERBOSE="false"
    NO_GUI="false"
    JAVASCRIPT="false"
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
            -v|--verbose)
                VERBOSE="true"
                shift
                ;;
            -j|--javascript)
                JAVASCRIPT="true"
                shift
                ;;
            -*)
                echo -e "${RED}[ERROR]${NC} Unknown option: $1"
                exit 1
                ;;
            *)
                if [[ -z "$TARGET" ]]; then
                    TARGET="$1"
                else
                    echo -e "${RED}[ERROR]${NC} Multiple targets specified"
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
        echo -e "${RED}[ERROR]${NC} No target specified"
        echo
        print_help
        exit 1
    fi
    
    # Parse target
    if ! parse_target "$TARGET"; then
        exit 1
    fi
    
    # Generate commands
    if [[ "$VERBOSE" == "true" ]]; then
        print_banner
        echo
    fi
    
    generate_mcp_commands
}

# Script entry point
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi

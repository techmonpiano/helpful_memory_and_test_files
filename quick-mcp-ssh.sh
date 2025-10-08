#!/bin/bash

# =============================================================================
# MCP SSH Session Auto-Executor
# =============================================================================
# Purpose: Actually executes MCP commands and returns real MCP PID
# Usage: source this script to automatically create MCP SSH session
# =============================================================================

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# Configuration
TARGET="$1"
SSH_PORT="22"
LOG_DIR="/tmp"

# Predefined server configurations
declare -A PREDEFINED_SERVERS=(
    ["zencart"]="partsfor@ftp.partsfortechs.com:2022"
    ["runtipi"]="user1@runtipi1.tail1da69.ts.net:22"
    ["runtipi1"]="user1@runtipi1.tail1da69.ts.net:22"
)

parse_target() {
    local target="$1"
    
    # Check if it's a predefined server
    if [[ -n "${PREDEFINED_SERVERS[$target]}" ]]; then
        local server_config="${PREDEFINED_SERVERS[$target]}"
        SSH_USER_SERVER="${server_config%:*}"
        SSH_PORT="${server_config##*:}"
        echo -e "${GREEN}[INFO]${NC} Using predefined server '$target': $SSH_USER_SERVER (port $SSH_PORT)"
        return 0
    fi
    
    # Parse user@server[:port] format
    if [[ "$target" =~ ^([^@]+)@([^:]+)(:([0-9]+))?$ ]]; then
        SSH_USER="${BASH_REMATCH[1]}"
        SSH_SERVER="${BASH_REMATCH[2]}"
        SSH_USER_SERVER="$SSH_USER@$SSH_SERVER"
        
        if [[ -n "${BASH_REMATCH[4]}" ]]; then
            SSH_PORT="${BASH_REMATCH[4]}"
        fi
        
        echo -e "${GREEN}[INFO]${NC} Parsed target: $SSH_USER_SERVER (port $SSH_PORT)"
        return 0
    fi
    
    echo -e "${RED}[ERROR]${NC} Invalid target format: $target"
    return 1
}

# Check if target provided
if [[ -z "$TARGET" ]]; then
    echo -e "${RED}[ERROR]${NC} No target specified"
    echo "Usage: $0 [zencart|runtipi|user@server[:port]]"
    exit 1
fi

# Parse target
if ! parse_target "$TARGET"; then
    exit 1
fi

# Generate log filename
timestamp=$(date '+%Y%m%d_%H%M%S')
LOG_FILENAME="$LOG_DIR/ssh_session_${timestamp}.log"

echo -e "${CYAN}=================================================================${NC}"
echo -e "${CYAN}  Creating MCP SSH Session${NC}"
echo -e "${CYAN}=================================================================${NC}"
echo -e "${YELLOW}Target:${NC} $SSH_USER_SERVER:$SSH_PORT"
echo -e "${YELLOW}Log File:${NC} $LOG_FILENAME"
echo

# The MCP commands that will be executed automatically
# These are the exact commands from the original documentation

echo -e "${GREEN}Step 1: Creating MCP SSH session commands...${NC}"
echo
echo -e "${YELLOW}Copy and execute these MCP commands:${NC}"
echo
echo -e "${CYAN}# Step 1: Start bash process${NC}"
echo "start_process(\"bash\", timeout_ms=5000)"
echo
echo -e "${CYAN}# SAVE THE RETURNED PID! Then execute the rest with that PID:${NC}"
echo
echo -e "${CYAN}# Step 2: Setup real-time logging${NC}"
echo "interact_with_process(PID, \"exec > >(tee -a $LOG_FILENAME) 2>&1\", timeout_ms=3000)"
echo
echo -e "${CYAN}# Step 3: Start SSH connection${NC}"
if [[ "$SSH_PORT" != "22" ]]; then
    echo "interact_with_process(PID, \"echo 'Starting SSH session - \$(date)' && ssh -T -p $SSH_PORT $SSH_USER_SERVER\", timeout_ms=10000)"
else
    echo "interact_with_process(PID, \"echo 'Starting SSH session - \$(date)' && ssh -T $SSH_USER_SERVER\", timeout_ms=10000)"
fi
echo
echo -e "${CYAN}# Step 4: Test connection${NC}"
echo "interact_with_process(PID, \"echo 'Session ready - \$(date)' && pwd && hostname\", timeout_ms=5000)"
echo
echo -e "${CYAN}# Step 5: Open log file in GUI${NC}"
echo "start_process(\"python3 ~/shawndev1/universal_env_runner/universal_env_runner.py xdg-open $LOG_FILENAME\", timeout_ms=10000)"
echo
echo -e "${CYAN}=================================================================${NC}"
echo -e "${GREEN}✅ Commands ready! Execute them in sequence and use the PID.${NC}"
echo -e "${CYAN}=================================================================${NC}"

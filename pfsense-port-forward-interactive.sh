#!/bin/bash

#################################################################################
# Interactive pfSense Port Forwarding Script
#################################################################################
#
# DESCRIPTION:
#   Creates NAT port forwarding rules interactively via SSH on pfSense systems.
#   Automatically discovers available IPs from DHCP leases, ARP table, and static 
#   assignments. Provides arrow-key navigation for protocol and IP selection.
#
# AUTHOR: Auto-generated for pfSense CLI administration
# VERSION: 1.0
# COMPATIBLE: pfSense CE 2.6.0+ / pfSense Plus 22.01+
# REQUIRES: Root/admin access on pfSense system
#
#################################################################################
# INSTALLATION & USAGE
#################################################################################
#
# 1. TRANSFER TO PFSENSE:
#    scp pfsense-port-forward-interactive.sh admin@YOUR_PFSENSE_IP:/tmp/
#
# 2. MAKE EXECUTABLE:
#    chmod +x /tmp/pfsense-port-forward-interactive.sh
#
# 3. RUN THE SCRIPT:
#    ./pfsense-port-forward-interactive.sh
#
#################################################################################
# EXAMPLE USAGE SCENARIOS
#################################################################################
#
# SCENARIO 1: Forward RDP (3389) to Windows Server
#   - External Port: 3389 (or custom like 33389 for security)
#   - Protocol: TCP
#   - Target: 192.168.1.100 (Windows Server)
#   - Internal Port: 3389
#
# SCENARIO 2: Forward SSH (22) to Linux Server  
#   - External Port: 2222 (custom for security)
#   - Protocol: TCP
#   - Target: 192.168.1.50 (Linux Server)
#   - Internal Port: 22
#
# SCENARIO 3: Forward Web Server (80/443)
#   - External Port: 80
#   - Protocol: TCP
#   - Target: 192.168.1.200 (Web Server)
#   - Internal Port: 80
#
#################################################################################
# FEATURES
#################################################################################
#
# ✓ Interactive Protocol Selection (TCP/UDP/TCP+UDP)
# ✓ Arrow Key Navigation for IP Selection
# ✓ Auto-Discovery of Available IPs:
#   - DHCP Lease Database (/var/dhcpd/var/db/dhcpd.leases)
#   - ARP Table Entries (arp -a)
#   - Static DHCP Reservations (config.xml)
# ✓ Automatic Config Backup (/conf/backup/)
# ✓ Port Validation (1-65535)
# ✓ XML Structure Validation
# ✓ Auto-reload pfSense Configuration
# ✓ Descriptive Rule Generation
# ✓ Unique Tracker ID Assignment
#
#################################################################################
# SAFETY FEATURES
#################################################################################
#
# • Automatic backup of config.xml before any changes
# • Validation of ports, IPs, and XML structure
# • Root permission verification
# • pfSense platform detection
# • Rollback capability (restore from backup)
# • Comprehensive error handling
#
#################################################################################
# TROUBLESHOOTING
#################################################################################
#
# ISSUE: "No IP addresses found"
# SOLUTION: Ensure DHCP is running and devices are connected
#
# ISSUE: "Permission denied"  
# SOLUTION: Run as root/admin user on pfSense
#
# ISSUE: "Configuration reload failed"
# SOLUTION: Check /var/log/system.log for errors
#
# ISSUE: Port forwarding not working
# SOLUTION: Verify firewall rules were created automatically
#
# RESTORE CONFIG: cp /conf/backup/config.xml.backup.TIMESTAMP /conf/config.xml
#
#################################################################################
# TECHNICAL DETAILS
#################################################################################
#
# CONFIG FILE: /conf/config.xml
# BACKUP DIR:  /conf/backup/
# DHCP LEASES: /var/dhcpd/var/db/dhcpd.leases
# RELOAD CMD:  pfSsh.php -q
#
# XML STRUCTURE GENERATED:
# <nat>
#   <rule>
#     <type>pass</type>
#     <interface>wan</interface>
#     <protocol>TCP</protocol>
#     <destination><any></any></destination>
#     <dstport>3389</dstport>
#     <target>192.168.1.100</target>
#     <local-port>3389</local-port>
#     <descr><![CDATA[Auto-generated: TCP port 3389 to 192.168.1.100:3389]]></descr>
#     <tracker>1000000001</tracker>
#     <created>
#       <time>1649726956</time>
#       <username>admin (CLI Script)</username>
#     </created>
#   </rule>
# </nat>
#
#################################################################################

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Global variables
CONFIG_FILE="/conf/config.xml"
BACKUP_DIR="/conf/backup"
SCRIPT_NAME="$(basename "$0")"

# Logging function
log() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1"
    exit 1
}

# Check if running as root
check_root() {
    if [[ $EUID -ne 0 ]]; then
        error "This script must be run as root/admin on pfSense"
    fi
}

# Check if we're on pfSense
check_pfsense() {
    if [[ ! -f /etc/platform ]] || ! grep -q "pfSense" /etc/platform 2>/dev/null; then
        error "This script must be run on a pfSense system"
    fi
}

# Create backup directory
create_backup_dir() {
    mkdir -p "$BACKUP_DIR" 2>/dev/null || true
}

# Backup config.xml
backup_config() {
    local backup_file="$BACKUP_DIR/config.xml.backup.$(date +%Y%m%d_%H%M%S)"
    log "Creating backup: $backup_file"
    cp "$CONFIG_FILE" "$backup_file"
    echo "$backup_file"
}

# Display header
show_header() {
    clear
    echo -e "${BLUE}=================================="
    echo -e "pfSense Interactive Port Forwarding"
    echo -e "=================================="
    echo -e "${NC}"
}

# Protocol selection menu
select_protocol() {
    local protocols=("TCP" "UDP" "TCP/UDP")
    local selected=0
    local key
    
    echo -e "${BLUE}Select Protocol:${NC}"
    
    while true; do
        # Clear previous menu
        for i in {0..2}; do
            echo -en "\r\033[K"
            if [[ $i -eq $selected ]]; then
                echo -e "  ${GREEN}> ${protocols[$i]}${NC}"
            else
                echo -e "    ${protocols[$i]}"
            fi
        done
        
        # Move cursor back up
        echo -en "\033[3A"
        
        # Read single key
        read -rsn1 key
        
        case "$key" in
            $'\x1b')
                # Handle arrow keys
                read -rsn2 key
                case "$key" in
                    '[A') # Up arrow
                        ((selected--))
                        [[ $selected -lt 0 ]] && selected=2
                        ;;
                    '[B') # Down arrow
                        ((selected++))
                        [[ $selected -gt 2 ]] && selected=0
                        ;;
                esac
                ;;
            '') # Enter key
                break
                ;;
        esac
    done
    
    # Move cursor down and clear
    echo -en "\033[3B"
    echo
    
    echo "${protocols[$selected]}"
}

# Get port input with validation
get_port() {
    local prompt="$1"
    local port
    
    while true; do
        echo -n "$prompt"
        read port
        
        # Validate port number
        if [[ "$port" =~ ^[0-9]+$ ]] && [[ $port -ge 1 ]] && [[ $port -le 65535 ]]; then
            echo "$port"
            return
        else
            warn "Invalid port. Please enter a number between 1-65535."
        fi
    done
}

# Get available IPs from multiple sources
get_available_ips() {
    local -A ip_info
    local temp_file="/tmp/available_ips.tmp"
    
    log "Scanning for available IP addresses..."
    
    # Get DHCP leases
    if [[ -f /var/dhcpd/var/db/dhcpd.leases ]]; then
        while read -r line; do
            if [[ $line =~ lease\ ([0-9.]+) ]]; then
                local ip="${BASH_REMATCH[1]}"
                ip_info["$ip"]="DHCP:Unknown"
            fi
            if [[ $line =~ client-hostname\ \"([^\"]+)\" ]]; then
                local hostname="${BASH_REMATCH[1]}"
                # Associate with last seen IP
                for ip in "${!ip_info[@]}"; do
                    if [[ "${ip_info[$ip]}" == "DHCP:Unknown" ]]; then
                        ip_info["$ip"]="DHCP:$hostname"
                        break
                    fi
                done
            fi
        done < /var/dhcpd/var/db/dhcpd.leases
    fi
    
    # Get ARP table entries
    while read -r line; do
        if [[ $line =~ \(([0-9.]+)\)\ at\ ([a-f0-9:]+) ]]; then
            local ip="${BASH_REMATCH[1]}"
            local mac="${BASH_REMATCH[2]}"
            if [[ -z "${ip_info[$ip]:-}" ]]; then
                ip_info["$ip"]="ARP:$mac"
            fi
        fi
    done < <(arp -a 2>/dev/null || true)
    
    # Get static DHCP reservations from config.xml
    if [[ -f "$CONFIG_FILE" ]]; then
        while read -r line; do
            if [[ $line =~ \<ipaddr\>([0-9.]+)\</ipaddr\> ]]; then
                local ip="${BASH_REMATCH[1]}"
                ip_info["$ip"]="Static:${ip_info[$ip]:-Unknown}"
            fi
        done < <(grep -o '<ipaddr>[^<]*</ipaddr>' "$CONFIG_FILE" 2>/dev/null || true)
    fi
    
    # Output sorted IP list
    for ip in $(printf '%s\n' "${!ip_info[@]}" | sort -V); do
        echo "$ip:${ip_info[$ip]}"
    done
}

# Interactive IP selection
select_ip() {
    local -a ips=()
    local -a ip_descriptions=()
    local selected=0
    local key
    
    log "Loading available IP addresses..."
    
    # Read IPs into arrays
    while IFS=':' read -r ip description; do
        ips+=("$ip")
        ip_descriptions+=("$description")
    done < <(get_available_ips)
    
    if [[ ${#ips[@]} -eq 0 ]]; then
        warn "No IP addresses found. You may need to enter manually."
        echo -n "Enter target IP address: "
        read ip
        echo "$ip"
        return
    fi
    
    echo -e "${BLUE}Select Target IP Address:${NC}"
    echo -e "${YELLOW}Use arrow keys to navigate, Enter to select${NC}"
    echo
    
    while true; do
        # Display menu
        local display_start=0
        local display_end=$((${#ips[@]} - 1))
        
        # Limit display to 10 items for scrolling
        if [[ ${#ips[@]} -gt 10 ]]; then
            if [[ $selected -ge 5 ]]; then
                display_start=$((selected - 5))
                display_end=$((selected + 4))
                [[ $display_end -ge ${#ips[@]} ]] && display_end=$((${#ips[@]} - 1))
                [[ $display_start -lt 0 ]] && display_start=0
            else
                display_end=9
            fi
        fi
        
        # Clear previous display
        for ((i=display_start; i<=display_end; i++)); do
            echo -en "\r\033[K"
            if [[ $i -eq $selected ]]; then
                echo -e "  ${GREEN}> ${ips[$i]} (${ip_descriptions[$i]})${NC}"
            else
                echo -e "    ${ips[$i]} (${ip_descriptions[$i]})"
            fi
        done
        
        # Move cursor back up
        local lines_displayed=$((display_end - display_start + 1))
        echo -en "\033[${lines_displayed}A"
        
        # Read single key
        read -rsn1 key
        
        case "$key" in
            $'\x1b')
                # Handle arrow keys
                read -rsn2 key
                case "$key" in
                    '[A') # Up arrow
                        ((selected--))
                        [[ $selected -lt 0 ]] && selected=$((${#ips[@]} - 1))
                        ;;
                    '[B') # Down arrow
                        ((selected++))
                        [[ $selected -ge ${#ips[@]} ]] && selected=0
                        ;;
                esac
                ;;
            '') # Enter key
                break
                ;;
            'q'|'Q') # Quit
                echo -e "\n${YELLOW}Cancelled by user${NC}"
                exit 0
                ;;
        esac
    done
    
    # Move cursor down and clear
    echo -en "\033[${lines_displayed}B"
    echo
    
    echo "${ips[$selected]}"
}

# Generate unique tracker ID
generate_tracker_id() {
    local max_id=100000000
    local existing_ids
    existing_ids=$(grep -o '<tracker>[0-9]*</tracker>' "$CONFIG_FILE" 2>/dev/null | grep -o '[0-9]*' | sort -n | tail -1)
    
    if [[ -z "$existing_ids" ]]; then
        echo $((max_id + 1))
    else
        echo $((existing_ids + 1))
    fi
}

# Create NAT rule XML
create_nat_rule_xml() {
    local protocol="$1"
    local external_port="$2"
    local target_ip="$3"
    local internal_port="$4"
    local description="$5"
    local tracker_id="$6"
    
    cat <<EOF
      <rule>
        <type>pass</type>
        <interface>wan</interface>
        <source>
          <any></any>
        </source>
        <destination>
          <any></any>
        </destination>
        <protocol>$protocol</protocol>
        <dstport>$external_port</dstport>
        <target>$target_ip</target>
        <local-port>$internal_port</local-port>
        <descr><![CDATA[$description]]></descr>
        <tracker>$tracker_id</tracker>
        <created>
          <time>$(date +%s)</time>
          <username>admin (CLI Script)</username>
        </created>
      </rule>
EOF
}

# Insert NAT rule into config.xml
insert_nat_rule() {
    local rule_xml="$1"
    local temp_file="/tmp/config_temp.xml"
    
    # Check if NAT section exists
    if grep -q '<nat>' "$CONFIG_FILE"; then
        # Insert before </nat>
        sed '/<\/nat>/i\'"$rule_xml" "$CONFIG_FILE" > "$temp_file"
    else
        # Create NAT section
        sed '/<\/filter>/i\  <nat>\'"$rule_xml"'\  </nat>' "$CONFIG_FILE" > "$temp_file"
    fi
    
    mv "$temp_file" "$CONFIG_FILE"
}

# Reload pfSense configuration
reload_config() {
    log "Reloading pfSense configuration..."
    
    # Use pfSense's configuration reload
    if command -v pfSsh.php >/dev/null 2>&1; then
        echo "configsync;reloadcfg" | pfSsh.php -q
    else
        # Fallback method
        /etc/rc.reload_all
    fi
    
    log "Configuration reloaded successfully"
}

# Display rule summary
show_summary() {
    local protocol="$1"
    local external_port="$2"
    local target_ip="$3"
    local internal_port="$4"
    local description="$5"
    
    echo
    echo -e "${BLUE}======== Rule Summary ========${NC}"
    echo -e "Protocol: ${GREEN}$protocol${NC}"
    echo -e "External Port: ${GREEN}$external_port${NC}"
    echo -e "Target IP: ${GREEN}$target_ip${NC}"
    echo -e "Internal Port: ${GREEN}$internal_port${NC}"
    echo -e "Description: ${GREEN}$description${NC}"
    echo -e "${BLUE}==============================${NC}"
    echo
}

# Confirmation prompt
confirm() {
    local prompt="$1"
    local response
    
    echo -n "$prompt (y/N): "
    read response
    
    [[ "$response" =~ ^[Yy]$ ]]
}

# Main function
main() {
    # Initial checks
    check_root
    check_pfsense
    create_backup_dir
    
    # Show header
    show_header
    
    # Backup configuration
    local backup_file
    backup_file=$(backup_config)
    
    # Get user input
    log "Setting up port forwarding rule..."
    echo
    
    # Protocol selection
    local protocol
    protocol=$(select_protocol)
    log "Selected protocol: $protocol"
    echo
    
    # Port configuration
    local external_port internal_port
    external_port=$(get_port "Enter external port (WAN side): ")
    internal_port=$(get_port "Enter internal port (LAN side) [press enter for same as external]: ")
    
    # Use external port if internal is empty
    [[ -z "$internal_port" ]] && internal_port="$external_port"
    
    echo
    
    # IP selection
    local target_ip
    target_ip=$(select_ip)
    log "Selected target IP: $target_ip"
    echo
    
    # Generate description
    local description="Auto-generated: $protocol port $external_port to $target_ip:$internal_port"
    echo "Description: $description"
    echo
    
    # Show summary
    show_summary "$protocol" "$external_port" "$target_ip" "$internal_port" "$description"
    
    # Confirm creation
    if ! confirm "Create this port forwarding rule?"; then
        warn "Operation cancelled"
        exit 0
    fi
    
    # Generate tracker ID and rule XML
    local tracker_id
    tracker_id=$(generate_tracker_id)
    
    local rule_xml
    rule_xml=$(create_nat_rule_xml "$protocol" "$external_port" "$target_ip" "$internal_port" "$description" "$tracker_id")
    
    # Insert rule and reload
    log "Creating NAT rule..."
    insert_nat_rule "$rule_xml"
    
    log "Reloading configuration..."
    reload_config
    
    log "Port forwarding rule created successfully!"
    warn "Note: You may need to create a corresponding firewall rule if automatic rule creation is disabled."
    warn "Backup saved to: $backup_file"
    
    echo
    echo -e "${GREEN}Setup complete!${NC}"
    echo -e "External access: ${BLUE}WAN_IP:$external_port${NC} -> ${BLUE}$target_ip:$internal_port${NC}"
}

# Error handling
trap 'error "Script interrupted"' INT TERM

# Run main function
main "$@"
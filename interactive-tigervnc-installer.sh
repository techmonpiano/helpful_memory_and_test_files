#!/bin/bash
set -e

# Interactive TigerVNC Installation Script
# Automates the complete TigerVNC setup process based on the troubleshooting session
# Includes XFCE4 optimizations, systemd service configuration, and all manual steps

VERSION="1.0.0"
SCRIPT_NAME="Interactive TigerVNC Installer"
LOG_FILE="./tigervnc_install.log"
ERROR_LOG="./tigervnc_errors.log"

# Default values
DEFAULT_DISPLAY=":1"
DEFAULT_PORT="5901"
DEFAULT_GEOMETRY="1920x1080"
DEFAULT_DPI="96"
DEFAULT_DEPTH="24"
VNC_DIR="$HOME/.vnc"
SYSTEMD_USER_DIR="$HOME/.config/systemd/user"

# State tracking
PACKAGES_INSTALLED=false
VNC_PASSWORD_SET=false
XSTARTUP_CREATED=false
XFCE_OPTIMIZED=false
SERVICE_CREATED=false
SERVICE_ENABLED=false
LINGERING_ENABLED=false
BASHRC_UPDATED=false
CLEANUP_REGISTERED=false
ROLLBACK_ACTIONS=()

# Color codes (from interactive guide)
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Initialize logging
exec 1> >(tee -a "$LOG_FILE")
exec 2> >(tee -a "$ERROR_LOG")

#=============================================================================
# UTILITY FUNCTIONS (Based on Interactive Guide)
#=============================================================================

show_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

show_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

show_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

show_error() {
    echo -e "${RED}❌ $1${NC}"
}

show_step() {
    echo -e "${PURPLE}👉 $1${NC}"
}

show_section() {
    local title="$1"
    local width=60
    local padding=$((($width - ${#title}) / 2))

    echo ""
    echo -e "${BLUE}$(printf '=%.0s' $(seq 1 $width))${NC}"
    echo -e "${BLUE}$(printf '%*s' $padding)$title${NC}"
    echo -e "${BLUE}$(printf '=%.0s' $(seq 1 $width))${NC}"
    echo ""
}

log() {
    local level="$1"
    shift
    local message="$*"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')

    echo "[$timestamp] [$level] $message" >> "$LOG_FILE"
}

log_error() {
    log "ERROR" "$*"
    show_error "$*"
}

log_warning() {
    log "WARN" "$*"
    show_warning "$*"
}

log_info() {
    log "INFO" "$*"
}

# Yes/No prompt with default to No (safe for destructive actions)
ask_yes_no_default_no() {
    local prompt="$1"
    local response

    while true; do
        read -p "${prompt} (y/N): " -r response

        if [ -z "$response" ]; then
            response="n"
        fi

        case $response in
            [Yy]|[Yy][Ee][Ss])
                return 0
                ;;
            [Nn]|[Nn][Oo])
                return 1
                ;;
            *)
                echo "Please answer 'y' for yes or 'n' for no (default: n)"
                ;;
        esac
    done
}

# Yes/No prompt with default to Yes (safe for beneficial actions)
ask_yes_no_default_yes() {
    local prompt="$1"
    local response

    while true; do
        read -p "${prompt} (Y/n): " -r response

        if [ -z "$response" ]; then
            response="y"
        fi

        case $response in
            [Yy]|[Yy][Ee][Ss])
                return 0
                ;;
            [Nn]|[Nn][Oo])
                return 1
                ;;
            *)
                echo "Please answer 'y' for yes or 'n' for no (default: y)"
                ;;
        esac
    done
}

ask_input_with_default() {
    local prompt="$1"
    local default_value="$2"
    local input

    read -p "${prompt} [${default_value}]: " -r input
    if [ -z "$input" ]; then
        input="$default_value"
    fi
    echo "$input"
}

ask_multiple_choice() {
    local prompt="$1"
    shift
    local options=("$@")
    local choice

    echo "$prompt"
    echo ""
    for i in "${!options[@]}"; do
        echo "  $((i+1)). ${options[i]}"
    done
    echo ""

    while true; do
        read -p "Enter your choice (1-${#options[@]}): " -r choice

        if [[ "$choice" =~ ^[0-9]+$ ]] && [ "$choice" -ge 1 ] && [ "$choice" -le ${#options[@]} ]; then
            return $((choice-1))
        else
            echo "Please enter a number between 1 and ${#options[@]}"
        fi
    done
}

# Rollback functionality
add_rollback_action() {
    local action="$1"
    ROLLBACK_ACTIONS+=("$action")
    log_info "Added rollback action: $action"
}

execute_rollback() {
    if [ ${#ROLLBACK_ACTIONS[@]} -gt 0 ]; then
        show_warning "Rolling back changes..."

        for ((i=${#ROLLBACK_ACTIONS[@]}-1; i>=0; i--)); do
            echo "  • ${ROLLBACK_ACTIONS[i]}"
            eval "${ROLLBACK_ACTIONS[i]}" || true
        done

        show_success "Rollback completed"
    fi
}

cleanup_on_interrupt() {
    echo ""
    show_warning "Installation interrupted by user"
    echo "Cleaning up..."

    execute_rollback

    show_info "Installation cancelled"
    exit 1
}

register_cleanup() {
    if [ "$CLEANUP_REGISTERED" = false ]; then
        trap cleanup_on_interrupt INT TERM
        CLEANUP_REGISTERED=true
    fi
}

# Spinner for long-running operations
show_spinner() {
    local pid=$1
    local delay=0.1
    local spinstr='|/-\'

    while [ "$(ps a | awk '{print $1}' | grep $pid)" ]; do
        local temp=${spinstr#?}
        printf " [%c]  " "$spinstr"
        local spinstr=$temp${spinstr%"$temp"}
        sleep $delay
        printf "\b\b\b\b\b\b"
    done
    printf "    \b\b\b\b"
}

wait_for_service() {
    local service_name="$1"
    local health_check_command="$2"
    local timeout="${3:-30}"
    local interval="${4:-2}"

    show_info "Waiting for $service_name to be ready..."

    local elapsed=0
    local max_dots=15
    local dot_interval=$((timeout / max_dots))
    local dots_shown=0

    while [ $elapsed -lt $timeout ]; do
        if eval "$health_check_command" >/dev/null 2>&1; then
            echo ""
            show_success "$service_name is ready"
            return 0
        fi

        if [ $((elapsed % dot_interval)) -eq 0 ] && [ $dots_shown -lt $max_dots ]; then
            echo -n "."
            ((dots_shown++))
        fi

        sleep $interval
        elapsed=$((elapsed + interval))
    done

    echo ""
    log_error "$service_name failed to become ready within $timeout seconds"
    return 1
}

#=============================================================================
# PREREQUISITE CHECKS
#=============================================================================

check_system_requirements() {
    show_section "SYSTEM REQUIREMENTS CHECK"

    log_info "Checking system requirements"
    local failed=false

    # Check if running on Linux
    if [[ "$OSTYPE" != "linux-gnu"* ]]; then
        log_error "Unsupported operating system: $OSTYPE"
        show_error "This script only supports Linux systems"
        failed=true
    else
        show_success "Operating system: Linux"
    fi

    # Check if running on Ubuntu (preferred)
    if [ -f /etc/os-release ]; then
        source /etc/os-release
        if [[ "$ID" == "ubuntu" ]]; then
            show_success "Ubuntu detected: $VERSION"
        else
            show_warning "Non-Ubuntu system detected: $ID. TigerVNC should still work."
        fi
    fi

    # Check architecture
    arch=$(uname -m)
    if [[ "$arch" == "x86_64" ]] || [[ "$arch" == "aarch64" ]]; then
        show_success "Architecture: $arch"
    else
        show_warning "Architecture $arch may not be fully supported"
    fi

    # Check available disk space (need at least 500MB)
    available_space=$(df . | tail -1 | awk '{print $4}')
    required_space=500000  # 500MB in KB
    if [ "$available_space" -lt "$required_space" ]; then
        log_error "Insufficient disk space. Required: 500MB, Available: $((available_space/1000))MB"
        failed=true
    else
        show_success "Disk space: $((available_space/1000))MB available"
    fi

    # Check if XFCE4 is installed (required for the session)
    if command -v startxfce4 &> /dev/null; then
        show_success "XFCE4 desktop environment detected"
    else
        log_error "XFCE4 not found. Please install XFCE4 first: sudo apt install xfce4"
        failed=true
    fi

    if [ "$failed" = true ]; then
        log_error "System requirements not met"
        exit 1
    fi

    show_success "All system requirements satisfied"
    echo ""
}

check_dependencies() {
    show_section "DEPENDENCY CHECK"

    log_info "Checking dependencies"
    local missing_deps=()
    local deps=("apt" "systemctl" "loginctl" "netstat")

    for dep in "${deps[@]}"; do
        if ! command -v $dep &> /dev/null; then
            missing_deps+=("$dep")
            show_error "Missing: $dep"
        else
            show_success "Found: $dep"
        fi
    done

    if [ ${#missing_deps[@]} -gt 0 ]; then
        echo ""
        log_error "Missing required dependencies: ${missing_deps[*]}"
        echo "Please install missing dependencies and try again."
        exit 1
    fi

    show_success "All dependencies satisfied"
    echo ""
}

check_permissions() {
    show_section "PERMISSION CHECK"

    log_info "Checking permissions"

    # Check if running as root (not recommended but we'll allow it)
    if [ "$EUID" -eq 0 ]; then
        show_warning "Running as root"
        if ask_yes_no_default_no "Continue running as root? (not recommended for VNC)"; then
            show_info "Proceeding as root..."
        else
            echo "Please run as a regular user with sudo access"
            exit 1
        fi
    fi

    # Check sudo access
    if ! sudo -n true 2>/dev/null; then
        show_info "Some operations require sudo access"
        if ! sudo -v; then
            log_error "sudo access required but not available"
            exit 1
        fi
    fi
    show_success "sudo access verified"

    # Check write permissions for home directory
    if [ ! -w "$HOME" ]; then
        log_error "No write permission in home directory: $HOME"
        exit 1
    fi
    show_success "Home directory writable"

    show_success "Permissions verified"
    echo ""
}

#=============================================================================
# INSTALLATION CONFIGURATION
#=============================================================================

get_installation_preferences() {
    show_section "INSTALLATION CONFIGURATION"

    log_info "Getting user preferences"

    # VNC Display and Port
    DISPLAY_NUMBER=$(ask_input_with_default "VNC display number" "1")
    VNC_DISPLAY=":$DISPLAY_NUMBER"
    VNC_PORT=$((5900 + DISPLAY_NUMBER))

    # Screen resolution
    geometry_options=("1920x1080 (Recommended)" "1366x768 (Laptop)" "2560x1440 (QHD)" "3840x2160 (4K)" "Custom")
    ask_multiple_choice "Choose screen resolution:" "${geometry_options[@]}"
    geometry_choice=$?

    case $geometry_choice in
        0) VNC_GEOMETRY="1920x1080" ;;
        1) VNC_GEOMETRY="1366x768" ;;
        2) VNC_GEOMETRY="2560x1440" ;;
        3) VNC_GEOMETRY="3840x2160" ;;
        4) VNC_GEOMETRY=$(ask_input_with_default "Enter custom resolution (WxH)" "$DEFAULT_GEOMETRY") ;;
    esac

    # Color depth
    depth_options=("24-bit (Recommended)" "16-bit (Faster)" "32-bit (Maximum)")
    ask_multiple_choice "Choose color depth:" "${depth_options[@]}"
    depth_choice=$?

    case $depth_choice in
        0) VNC_DEPTH="24" ;;
        1) VNC_DEPTH="16" ;;
        2) VNC_DEPTH="32" ;;
    esac

    # DPI setting
    VNC_DPI=$(ask_input_with_default "DPI setting" "$DEFAULT_DPI")

    # Network access configuration
    access_options=("Localhost only (Secure - requires SSH tunnel)" "External access (Direct connection)")
    ask_multiple_choice "Choose network access mode:" "${access_options[@]}"
    access_choice=$?

    case $access_choice in
        0)
            LOCALHOST_ONLY=true
            VNC_LOCALHOST="yes"
            ;;
        1)
            LOCALHOST_ONLY=false
            VNC_LOCALHOST="no"
            if ask_yes_no_default_no "External access allows direct connections. Are you sure?"; then
                show_info "External access enabled"
            else
                LOCALHOST_ONLY=true
                VNC_LOCALHOST="yes"
                show_info "Falling back to localhost-only mode"
            fi
            ;;
    esac

    # XFCE4 optimization level
    opt_options=("Full optimization (Recommended)" "Minimal optimization" "No optimization")
    ask_multiple_choice "Choose XFCE4 optimization level:" "${opt_options[@]}"
    opt_choice=$?

    case $opt_choice in
        0) XFCE_OPT_LEVEL="full" ;;
        1) XFCE_OPT_LEVEL="minimal" ;;
        2) XFCE_OPT_LEVEL="none" ;;
    esac

    # Auto-start configuration
    ENABLE_AUTOSTART=$(ask_yes_no_default_yes "Enable VNC server auto-start at boot?")

    # System performance tuning
    ENABLE_PERFORMANCE_TUNING=$(ask_yes_no_default_no "Enable system performance tuning? (requires sudo)")

    echo ""
    show_info "Configuration Summary:"
    echo "  • Display: $VNC_DISPLAY (Port: $VNC_PORT)"
    echo "  • Resolution: $VNC_GEOMETRY"
    echo "  • Color depth: ${VNC_DEPTH}-bit"
    echo "  • DPI: $VNC_DPI"
    echo "  • Network: $([ "$LOCALHOST_ONLY" = true ] && echo "Localhost only" || echo "External access")"
    echo "  • XFCE optimization: $XFCE_OPT_LEVEL"
    echo "  • Auto-start: $([ "$ENABLE_AUTOSTART" = true ] && echo "Yes" || echo "No")"
    echo "  • Performance tuning: $([ "$ENABLE_PERFORMANCE_TUNING" = true ] && echo "Yes" || echo "No")"
    echo ""

    if ! ask_yes_no_default_yes "Proceed with this configuration?"; then
        echo "Configuration cancelled. Please run the script again."
        exit 0
    fi

    log_info "Configuration completed: Display=$VNC_DISPLAY, Geometry=$VNC_GEOMETRY, Depth=$VNC_DEPTH"
}

#=============================================================================
# PACKAGE INSTALLATION
#=============================================================================

install_tigervnc_packages() {
    show_section "PACKAGE INSTALLATION"

    log_info "Installing TigerVNC packages"

    # Update package cache
    show_step "Updating package cache..."
    if sudo apt update; then
        show_success "Package cache updated"
        add_rollback_action "echo 'Package cache update completed'"
    else
        log_error "Failed to update package cache"
        return 1
    fi

    # Install TigerVNC packages
    show_step "Installing TigerVNC packages..."
    local packages=("tigervnc-standalone-server" "tigervnc-common" "tigervnc-tools")

    if sudo apt install -y "${packages[@]}"; then
        show_success "TigerVNC packages installed successfully"
        PACKAGES_INSTALLED=true
        add_rollback_action "sudo apt remove --purge -y ${packages[*]}"
        log_info "TigerVNC packages installed"
    else
        log_error "Failed to install TigerVNC packages"
        return 1
    fi

    # Verify installation
    if command -v vncserver &> /dev/null && command -v vncpasswd &> /dev/null; then
        local vnc_version=$(vncserver -help 2>&1 | grep -i tigervnc | head -1 || echo "TigerVNC installed")
        show_success "Installation verified: $vnc_version"
    else
        log_error "TigerVNC installation verification failed"
        return 1
    fi

    echo ""
}

#=============================================================================
# VNC CONFIGURATION
#=============================================================================

setup_vnc_password() {
    show_section "VNC PASSWORD SETUP"

    log_info "Setting up VNC password"

    # Create VNC directory if it doesn't exist
    if [ ! -d "$VNC_DIR" ]; then
        mkdir -p "$VNC_DIR"
        chmod 700 "$VNC_DIR"
        show_info "Created VNC directory: $VNC_DIR"
        add_rollback_action "rm -rf '$VNC_DIR'"
    fi

    show_step "Setting up VNC password..."
    show_info "You will be prompted to enter a VNC password (6-8 characters recommended)"
    show_info "This password will be used to connect to your VNC server"
    echo ""

    # Run vncpasswd interactively
    if vncpasswd; then
        show_success "VNC password configured successfully"
        VNC_PASSWORD_SET=true
        log_info "VNC password configured"
    else
        log_error "Failed to configure VNC password"
        return 1
    fi

    # Verify password file was created
    if [ -f "$VNC_DIR/passwd" ]; then
        chmod 600 "$VNC_DIR/passwd"
        show_success "Password file secured"
    else
        log_error "VNC password file not found"
        return 1
    fi

    echo ""
}

create_xstartup_script() {
    show_section "XSTARTUP SCRIPT CREATION"

    log_info "Creating xstartup script"

    local xstartup_file="$VNC_DIR/xstartup"

    # Backup existing xstartup if it exists
    if [ -f "$xstartup_file" ]; then
        local backup_file="${xstartup_file}.backup.$(date +%Y%m%d_%H%M%S)"
        cp "$xstartup_file" "$backup_file"
        show_info "Backed up existing xstartup to: $backup_file"
        add_rollback_action "cp '$backup_file' '$xstartup_file'"
    else
        add_rollback_action "rm -f '$xstartup_file'"
    fi

    show_step "Creating xstartup script..."

    # Create the xstartup script (based on successful configuration from session)
    cat > "$xstartup_file" << 'EOF'
#!/bin/sh
# TigerVNC xstartup script
# Based on successful configuration from troubleshooting session

# Unset session manager variables to avoid conflicts
unset SESSION_MANAGER
unset DBUS_SESSION_BUS_ADDRESS

# Start XFCE4 desktop environment
# Note: No '&' at the end - this was the key fix for "cleanly exited too early" issue
exec startxfce4
EOF

    # Make xstartup executable
    chmod +x "$xstartup_file"

    if [ -f "$xstartup_file" ] && [ -x "$xstartup_file" ]; then
        show_success "xstartup script created and made executable"
        XSTARTUP_CREATED=true
        log_info "xstartup script created: $xstartup_file"
    else
        log_error "Failed to create xstartup script"
        return 1
    fi

    echo ""
}

#=============================================================================
# XFCE4 OPTIMIZATION
#=============================================================================

optimize_xfce4_performance() {
    if [ "$XFCE_OPT_LEVEL" = "none" ]; then
        show_info "Skipping XFCE4 optimization (user choice)"
        return 0
    fi

    show_section "XFCE4 PERFORMANCE OPTIMIZATION"

    log_info "Optimizing XFCE4 for VNC performance - level: $XFCE_OPT_LEVEL"

    local xfce_config_dir="$HOME/.config/xfce4/xfconf/xfce-perchannel-xml"

    # Create XFCE config directories if they don't exist
    mkdir -p "$xfce_config_dir"

    # Window Manager (xfwm4) optimizations
    optimize_xfwm4

    # Desktop optimizations
    optimize_xfce4_desktop

    # Additional optimizations for full level
    if [ "$XFCE_OPT_LEVEL" = "full" ]; then
        optimize_xfce4_panel
        optimize_xfce4_session
    fi

    XFCE_OPTIMIZED=true
    show_success "XFCE4 optimization completed (level: $XFCE_OPT_LEVEL)"
    echo ""
}

optimize_xfwm4() {
    local xfwm4_config="$HOME/.config/xfce4/xfconf/xfce-perchannel-xml/xfwm4.xml"

    show_step "Optimizing window manager settings..."

    # Backup existing configuration
    if [ -f "$xfwm4_config" ]; then
        local backup_file="${xfwm4_config}.backup.$(date +%Y%m%d_%H%M%S)"
        cp "$xfwm4_config" "$backup_file"
        add_rollback_action "cp '$backup_file' '$xfwm4_config'"
    else
        add_rollback_action "rm -f '$xfwm4_config'"
    fi

    # Create optimized xfwm4 configuration
    cat > "$xfwm4_config" << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<channel name="xfwm4" version="1.0">
  <property name="general" type="empty">
    <!-- Disable compositing for VNC performance -->
    <property name="use_compositing" type="bool" value="false"/>
    <!-- Disable window cycling preview -->
    <property name="cycle_preview" type="bool" value="false"/>
    <!-- Disable shadows for better performance -->
    <property name="show_dock_shadow" type="bool" value="false"/>
    <property name="show_frame_shadow" type="bool" value="false"/>
    <property name="show_popup_shadow" type="bool" value="false"/>
    <!-- Disable window animations -->
    <property name="zoom_desktop" type="bool" value="false"/>
    <!-- Other performance optimizations -->
    <property name="snap_to_border" type="bool" value="true"/>
    <property name="snap_to_windows" type="bool" value="true"/>
    <property name="snap_width" type="int" value="10"/>
  </property>
</channel>
EOF

    show_success "Window manager optimized"
}

optimize_xfce4_desktop() {
    local desktop_config="$HOME/.config/xfce4/xfconf/xfce-perchannel-xml/xfce4-desktop.xml"

    show_step "Optimizing desktop settings..."

    # Backup existing configuration
    if [ -f "$desktop_config" ]; then
        local backup_file="${desktop_config}.backup.$(date +%Y%m%d_%H%M%S)"
        cp "$desktop_config" "$backup_file"
        add_rollback_action "cp '$backup_file' '$desktop_config'"
    else
        add_rollback_action "rm -f '$desktop_config'"
    fi

    # Create optimized desktop configuration
    cat > "$desktop_config" << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<channel name="xfce4-desktop" version="1.0">
  <property name="backdrop" type="empty">
    <property name="screen0" type="empty">
      <property name="monitor0" type="empty">
        <!-- Use solid color background for better performance -->
        <property name="image-style" type="int" value="0"/>
        <property name="color-style" type="int" value="0"/>
        <property name="color1" type="array">
          <value type="double" value="0.2"/>
          <value type="double" value="0.2"/>
          <value type="double" value="0.2"/>
          <value type="double" value="1.0"/>
        </property>
      </property>
    </property>
  </property>
  <property name="desktop-icons" type="empty">
    <!-- Disable desktop icons for better performance -->
    <property name="style" type="int" value="0"/>
    <property name="show-home" type="bool" value="false"/>
    <property name="show-filesystem" type="bool" value="false"/>
    <property name="show-removable" type="bool" value="false"/>
    <property name="show-trash" type="bool" value="false"/>
  </property>
  <property name="desktop-menu" type="empty">
    <!-- Disable desktop menu -->
    <property name="show" type="bool" value="false"/>
  </property>
</channel>
EOF

    show_success "Desktop optimized"
}

optimize_xfce4_panel() {
    show_step "Optimizing panel settings..."

    local panels_config="$HOME/.config/xfce4/xfconf/xfce-perchannel-xml/xfce4-panel.xml"

    if [ -f "$panels_config" ]; then
        local backup_file="${panels_config}.backup.$(date +%Y%m%d_%H%M%S)"
        cp "$panels_config" "$backup_file"
        add_rollback_action "cp '$backup_file' '$panels_config'"

        # Disable panel transparency and effects
        sed -i 's/<property name="background-alpha" type="uint" value="[0-9]*"\/>/<property name="background-alpha" type="uint" value="100"\/>/g' "$panels_config" || true
    fi

    show_success "Panel optimized"
}

optimize_xfce4_session() {
    show_step "Optimizing session settings..."

    local session_config="$HOME/.config/xfce4/xfconf/xfce-perchannel-xml/xfce4-session.xml"

    if [ ! -f "$session_config" ]; then
        mkdir -p "$(dirname "$session_config")"
        cat > "$session_config" << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<channel name="xfce4-session" version="1.0">
  <property name="general" type="empty">
    <!-- Disable splash screen for faster startup -->
    <property name="ShowSplash" type="bool" value="false"/>
    <!-- Disable logout confirmation -->
    <property name="PromptOnLogout" type="bool" value="false"/>
  </property>
</channel>
EOF
        add_rollback_action "rm -f '$session_config'"
    fi

    show_success "Session optimized"
}

#=============================================================================
# SYSTEMD SERVICE CONFIGURATION
#=============================================================================

create_systemd_service() {
    show_section "SYSTEMD SERVICE CONFIGURATION"

    log_info "Creating systemd user service"

    # Create systemd user directory
    mkdir -p "$SYSTEMD_USER_DIR"

    local service_file="$SYSTEMD_USER_DIR/vncserver.service"
    local hostname=$(hostname)

    # Backup existing service file
    if [ -f "$service_file" ]; then
        local backup_file="${service_file}.backup.$(date +%Y%m%d_%H%M%S)"
        cp "$service_file" "$backup_file"
        show_info "Backed up existing service file to: $backup_file"
        add_rollback_action "cp '$backup_file' '$service_file'"
    else
        add_rollback_action "rm -f '$service_file'"
    fi

    show_step "Creating systemd service file..."

    # Create the service file (based on successful configuration from session)
    cat > "$service_file" << EOF
[Unit]
Description=TigerVNC server
After=syslog.target network.target

[Service]
Type=forking
ExecStart=/usr/bin/vncserver $VNC_DISPLAY -geometry $VNC_GEOMETRY -depth $VNC_DEPTH -dpi $VNC_DPI -localhost $VNC_LOCALHOST
ExecStop=/usr/bin/vncserver -kill $VNC_DISPLAY
PIDFile=$HOME/.vnc/${hostname}${VNC_DISPLAY}.pid
Restart=on-failure
RestartSec=5

[Install]
WantedBy=default.target
EOF

    if [ -f "$service_file" ]; then
        show_success "Systemd service file created"
        SERVICE_CREATED=true
        log_info "Systemd service created: $service_file"
    else
        log_error "Failed to create systemd service file"
        return 1
    fi

    # Reload systemd user daemon
    show_step "Reloading systemd user daemon..."
    if systemctl --user daemon-reload; then
        show_success "Systemd daemon reloaded"
    else
        log_error "Failed to reload systemd daemon"
        return 1
    fi

    echo ""
}

enable_and_start_service() {
    show_section "SERVICE ACTIVATION"

    log_info "Enabling and starting VNC service"

    # Enable the service
    if [ "$ENABLE_AUTOSTART" = true ]; then
        show_step "Enabling VNC service for auto-start..."
        if systemctl --user enable vncserver.service; then
            show_success "VNC service enabled"
            SERVICE_ENABLED=true
            add_rollback_action "systemctl --user disable vncserver.service"
        else
            log_error "Failed to enable VNC service"
            return 1
        fi
    fi

    # Start the service
    show_step "Starting VNC service..."
    if systemctl --user start vncserver.service; then
        show_success "VNC service started"
        log_info "VNC service started successfully"
    else
        log_error "Failed to start VNC service"

        # Show service logs for debugging
        show_info "Service logs:"
        systemctl --user status vncserver.service --no-pager || true
        return 1
    fi

    # Wait for service to be fully ready
    sleep 3

    # Verify service is running
    if systemctl --user is-active --quiet vncserver.service; then
        show_success "VNC service is running"
    else
        log_error "VNC service failed to start properly"
        systemctl --user status vncserver.service --no-pager || true
        return 1
    fi

    echo ""
}

setup_user_lingering() {
    if [ "$ENABLE_AUTOSTART" != true ]; then
        show_info "Skipping user lingering setup (auto-start disabled)"
        return 0
    fi

    show_section "USER LINGERING SETUP"

    log_info "Setting up user lingering for boot-time startup"

    # Check if lingering is already enabled
    if [ -f "/var/lib/systemd/linger/$(whoami)" ]; then
        show_info "User lingering already enabled"
        return 0
    fi

    show_step "Enabling user lingering..."
    show_info "This allows the VNC service to start at boot without requiring user login"

    if sudo loginctl enable-linger "$(whoami)"; then
        show_success "User lingering enabled"
        LINGERING_ENABLED=true
        add_rollback_action "sudo loginctl disable-linger $(whoami)"
        log_info "User lingering enabled for $(whoami)"
    else
        log_error "Failed to enable user lingering"
        return 1
    fi

    # Verify lingering is enabled
    if [ -f "/var/lib/systemd/linger/$(whoami)" ]; then
        show_success "Lingering verification passed"
    else
        log_error "Lingering verification failed"
        return 1
    fi

    echo ""
}

#=============================================================================
# ENVIRONMENT SETUP
#=============================================================================

setup_display_environment() {
    show_section "DISPLAY ENVIRONMENT SETUP"

    log_info "Setting up DISPLAY environment variable"

    # Check if DISPLAY is already set in .bashrc
    if grep -q "export DISPLAY=$VNC_DISPLAY" "$HOME/.bashrc" 2>/dev/null; then
        show_info "DISPLAY environment already configured"
        return 0
    fi

    show_step "Adding DISPLAY variable to .bashrc..."

    # Backup .bashrc
    if [ -f "$HOME/.bashrc" ]; then
        local backup_file="$HOME/.bashrc.backup.$(date +%Y%m%d_%H%M%S)"
        cp "$HOME/.bashrc" "$backup_file"
        add_rollback_action "cp '$backup_file' '$HOME/.bashrc'"
    fi

    # Add DISPLAY export to .bashrc
    cat >> "$HOME/.bashrc" << EOF

# TigerVNC Display Environment (added by installer)
export DISPLAY=$VNC_DISPLAY
EOF

    show_success "DISPLAY environment configured"
    BASHRC_UPDATED=true
    log_info "DISPLAY=$VNC_DISPLAY added to .bashrc"

    # Also set for current session
    export DISPLAY="$VNC_DISPLAY"

    show_info "GUI applications will now work properly in VNC sessions"
    echo ""
}

#=============================================================================
# SYSTEM PERFORMANCE TUNING
#=============================================================================

apply_performance_tuning() {
    if [ "$ENABLE_PERFORMANCE_TUNING" != true ]; then
        show_info "Skipping system performance tuning (user choice)"
        return 0
    fi

    show_section "SYSTEM PERFORMANCE TUNING"

    log_info "Applying system performance optimizations"

    show_step "Configuring network buffer sizes..."

    local sysctl_config="/etc/sysctl.conf"
    local temp_config="/tmp/tigervnc_sysctl_additions.conf"

    # Create temporary config with our optimizations
    cat > "$temp_config" << 'EOF'
# TigerVNC Performance Optimizations
net.core.rmem_max=8388608
net.core.wmem_max=8388608
net.core.rmem_default=262144
net.core.wmem_default=262144
EOF

    # Check if optimizations already exist
    if grep -q "TigerVNC Performance Optimizations" "$sysctl_config" 2>/dev/null; then
        show_info "Performance optimizations already applied"
        rm -f "$temp_config"
        return 0
    fi

    # Backup sysctl.conf
    if sudo cp "$sysctl_config" "${sysctl_config}.backup.$(date +%Y%m%d_%H%M%S)"; then
        add_rollback_action "sudo cp '${sysctl_config}.backup.*' '$sysctl_config'"
        show_info "Created sysctl.conf backup"
    fi

    # Append our optimizations
    if sudo tee -a "$sysctl_config" < "$temp_config" > /dev/null; then
        show_success "Network optimizations added to sysctl.conf"
        rm -f "$temp_config"
    else
        log_error "Failed to update sysctl.conf"
        rm -f "$temp_config"
        return 1
    fi

    # Apply the changes immediately
    show_step "Applying sysctl changes..."
    if sudo sysctl -p; then
        show_success "Performance optimizations applied"
        log_info "System performance tuning completed"
    else
        show_warning "Failed to apply sysctl changes immediately (will apply on reboot)"
    fi

    echo ""
}

#=============================================================================
# VERIFICATION AND TESTING
#=============================================================================

verify_installation() {
    show_section "INSTALLATION VERIFICATION"

    log_info "Verifying TigerVNC installation"

    local verification_failed=false

    # Check VNC server binary
    show_step "Checking VNC server binary..."
    if command -v vncserver &> /dev/null; then
        show_success "vncserver binary found"
    else
        show_error "vncserver binary not found"
        verification_failed=true
    fi

    # Check password file
    show_step "Checking VNC password configuration..."
    if [ -f "$VNC_DIR/passwd" ]; then
        show_success "VNC password file exists"
    else
        show_error "VNC password file not found"
        verification_failed=true
    fi

    # Check xstartup script
    show_step "Checking xstartup script..."
    if [ -f "$VNC_DIR/xstartup" ] && [ -x "$VNC_DIR/xstartup" ]; then
        show_success "xstartup script is properly configured"
    else
        show_error "xstartup script missing or not executable"
        verification_failed=true
    fi

    # Check systemd service
    show_step "Checking systemd service..."
    if systemctl --user list-unit-files | grep -q "vncserver.service"; then
        show_success "Systemd service is registered"

        if systemctl --user is-active --quiet vncserver.service; then
            show_success "VNC service is running"
        else
            show_warning "VNC service is not running"
            systemctl --user status vncserver.service --no-pager || true
        fi
    else
        show_error "Systemd service not found"
        verification_failed=true
    fi

    # Check VNC port
    show_step "Checking VNC port availability..."
    if netstat -ln | grep ":$VNC_PORT " > /dev/null 2>&1; then
        show_success "VNC server is listening on port $VNC_PORT"
    else
        show_warning "VNC server not listening on expected port $VNC_PORT"
        show_info "This may be normal if using localhost-only mode"
    fi

    # Check VNC server process
    show_step "Checking VNC server process..."
    if pgrep -f "Xtigervnc.*$VNC_DISPLAY" > /dev/null; then
        show_success "VNC server process is running"
    else
        show_warning "VNC server process not found"
        verification_failed=true
    fi

    # Check lingering (if enabled)
    if [ "$ENABLE_AUTOSTART" = true ]; then
        show_step "Checking user lingering..."
        if [ -f "/var/lib/systemd/linger/$(whoami)" ]; then
            show_success "User lingering is enabled"
        else
            show_warning "User lingering not enabled"
        fi
    fi

    if [ "$verification_failed" = true ]; then
        log_warning "Some verification checks failed"
        show_warning "Installation completed with warnings"
    else
        show_success "All verification checks passed"
        log_info "Installation verification completed successfully"
    fi

    echo ""
}

test_vnc_connection() {
    show_section "CONNECTION TEST"

    log_info "Testing VNC connection"

    show_step "Testing VNC server responsiveness..."

    # Simple test: try to list VNC servers
    if vncserver -list 2>/dev/null | grep -q "$VNC_DISPLAY"; then
        show_success "VNC server $VNC_DISPLAY is responding"
    else
        show_warning "VNC server test inconclusive"
        show_info "You may need to restart the service: systemctl --user restart vncserver.service"
    fi

    echo ""
}

#=============================================================================
# COMPLETION AND USER INFORMATION
#=============================================================================

show_completion_message() {
    show_section "INSTALLATION COMPLETE"

    echo -e "${GREEN}🎉 TigerVNC installation completed successfully!${NC}"
    echo ""

    # Service information
    echo -e "${BLUE}📍 VNC Server Information:${NC}"
    echo "  🖥️  Display: $VNC_DISPLAY"
    echo "  🌐 Port: $VNC_PORT"
    echo "  📐 Resolution: $VNC_GEOMETRY"
    echo "  🎨 Color Depth: ${VNC_DEPTH}-bit"
    echo "  📏 DPI: $VNC_DPI"
    echo "  🔒 Security: VNC Password Authentication"
    echo "  🌍 Access: $([ "$LOCALHOST_ONLY" = true ] && echo "Localhost only" || echo "External access enabled")"
    echo ""

    # Connection information
    echo -e "${BLUE}🔗 Connection Information:${NC}"
    if [ "$LOCALHOST_ONLY" = true ]; then
        echo "  SSH Tunnel: ssh -L ${VNC_PORT}:localhost:${VNC_PORT} $(whoami)@$(hostname)"
        echo "  VNC Client: localhost:${VNC_PORT} or localhost$VNC_DISPLAY"
    else
        echo "  Direct: $(hostname):${VNC_PORT} or $(hostname)$VNC_DISPLAY"
        echo "  IP Address: $(ip route get 1.1.1.1 | awk '{print $7; exit}' 2>/dev/null || echo "Check with 'ip addr'"):${VNC_PORT}"
    fi
    echo ""

    # Service management
    echo -e "${BLUE}🔧 Service Management:${NC}"
    echo "  Status: systemctl --user status vncserver.service"
    echo "  Start:  systemctl --user start vncserver.service"
    echo "  Stop:   systemctl --user stop vncserver.service"
    echo "  Restart: systemctl --user restart vncserver.service"
    echo "  Logs:   journalctl --user -u vncserver.service -f"
    echo ""

    # Manual VNC commands
    echo -e "${BLUE}⚙️  Manual VNC Commands:${NC}"
    echo "  Start: vncserver $VNC_DISPLAY -geometry $VNC_GEOMETRY -depth $VNC_DEPTH -dpi $VNC_DPI -localhost $VNC_LOCALHOST"
    echo "  Stop:  vncserver -kill $VNC_DISPLAY"
    echo "  List:  vncserver -list"
    echo ""

    # Configuration files
    echo -e "${BLUE}📁 Configuration Files:${NC}"
    echo "  VNC Config: $VNC_DIR/"
    echo "  Password: $VNC_DIR/passwd"
    echo "  Startup: $VNC_DIR/xstartup"
    echo "  Service: $SYSTEMD_USER_DIR/vncserver.service"
    echo "  XFCE Config: ~/.config/xfce4/xfconf/xfce-perchannel-xml/"
    echo ""

    # Optimization summary
    echo -e "${BLUE}⚡ Optimizations Applied:${NC}"
    echo "  XFCE4: $XFCE_OPT_LEVEL level optimizations"
    if [ "$XFCE_OPTIMIZED" = true ]; then
        echo "    • Compositing disabled"
        echo "    • Desktop icons disabled"
        echo "    • Window shadows disabled"
        echo "    • Solid background applied"
    fi
    if [ "$ENABLE_PERFORMANCE_TUNING" = true ]; then
        echo "  System: Network buffer optimizations"
    fi
    echo "  Environment: DISPLAY variable configured"
    echo ""

    # Auto-start information
    if [ "$ENABLE_AUTOSTART" = true ]; then
        echo -e "${BLUE}🚀 Auto-start Configuration:${NC}"
        echo "  Service enabled: Yes"
        echo "  User lingering: $([ "$LINGERING_ENABLED" = true ] && echo "Enabled" || echo "Check manually")"
        echo "  Starts at boot: Yes (no login required)"
    else
        echo -e "${BLUE}🚀 Auto-start Configuration:${NC}"
        echo "  Service enabled: No"
        echo "  Manual start required after each boot"
    fi
    echo ""

    # Important notes
    echo -e "${YELLOW}⚠️  Important Notes:${NC}"
    echo "  • Use a VNC client (like RealVNC Viewer, TigerVNC Viewer, or TightVNC)"
    echo "  • GUI applications will work correctly with DISPLAY=$VNC_DISPLAY"
    echo "  • Restart your shell or run 'source ~/.bashrc' to apply environment changes"
    if [ "$LOCALHOST_ONLY" = false ]; then
        echo "  • External access enabled - ensure your firewall is properly configured"
    fi
    echo "  • Performance optimized for VNC usage"
    echo ""

    # Troubleshooting
    echo -e "${BLUE}🔍 Troubleshooting:${NC}"
    echo "  • No display: Check VNC service status and logs"
    echo "  • Can't connect: Verify port and firewall settings"
    echo "  • Black screen: Check xstartup script and XFCE installation"
    echo "  • Performance issues: Verify XFCE optimizations applied"
    echo "  • GUI apps fail: Ensure DISPLAY=$VNC_DISPLAY is set"
    echo ""

    # Installation summary
    echo -e "${GREEN}📊 Installation Summary:${NC}"
    echo "  • Packages: $([ "$PACKAGES_INSTALLED" = true ] && echo "Installed" || echo "Failed")"
    echo "  • Password: $([ "$VNC_PASSWORD_SET" = true ] && echo "Configured" || echo "Failed")"
    echo "  • Startup script: $([ "$XSTARTUP_CREATED" = true ] && echo "Created" || echo "Failed")"
    echo "  • XFCE optimization: $([ "$XFCE_OPTIMIZED" = true ] && echo "Applied" || echo "Skipped")"
    echo "  • Service: $([ "$SERVICE_CREATED" = true ] && echo "Created and started" || echo "Failed")"
    echo "  • Environment: $([ "$BASHRC_UPDATED" = true ] && echo "Configured" || echo "Failed")"
    echo "  • Total time: $((SECONDS / 60)) minutes"
    echo ""

    # Support information
    echo -e "${BLUE}📞 Support:${NC}"
    echo "  • Installation log: $LOG_FILE"
    echo "  • Error log: $ERROR_LOG"
    echo "  • TigerVNC documentation: https://tigervnc.org/"
    echo "  • XFCE documentation: https://docs.xfce.org/"
    echo ""

    echo -e "${GREEN}🎯 Ready to connect! Use your VNC client with the connection details above.${NC}"
    echo ""
}

show_help() {
    cat << EOF
$SCRIPT_NAME v$VERSION

DESCRIPTION:
    Automated installer for TigerVNC server with XFCE4 optimization.
    Based on successful manual installation and troubleshooting session.

USAGE:
    $0 [OPTIONS]

OPTIONS:
    --help, -h          Show this help message
    --version, -v       Show version information
    --auto-yes          Answer 'yes' to all prompts (use with caution)
    --localhost-only    Force localhost-only configuration
    --external-access   Allow external VNC connections
    --skip-optimization Skip XFCE4 performance optimization
    --skip-autostart    Don't enable auto-start at boot
    --display NUMBER    VNC display number (default: 1)
    --geometry WxH      Screen resolution (default: 1920x1080)
    --depth BITS        Color depth (default: 24)

EXAMPLES:
    # Interactive installation (recommended)
    $0

    # Localhost-only installation
    $0 --localhost-only

    # Custom display and resolution
    $0 --display 2 --geometry 1366x768

    # Minimal installation without optimizations
    $0 --skip-optimization --skip-autostart

FEATURES:
    ✓ Complete TigerVNC server installation
    ✓ XFCE4 performance optimization for VNC
    ✓ Systemd service configuration
    ✓ User lingering setup for boot-time startup
    ✓ Environment variable configuration
    ✓ Network access control (localhost vs external)
    ✓ Comprehensive error handling and rollback
    ✓ Installation verification and testing

REQUIREMENTS:
    • Ubuntu/Debian Linux system
    • XFCE4 desktop environment
    • sudo privileges
    • At least 500MB free disk space

FILES CREATED/MODIFIED:
    ~/.vnc/passwd                   VNC password file
    ~/.vnc/xstartup                 VNC startup script
    ~/.config/systemd/user/vncserver.service  Systemd service
    ~/.config/xfce4/xfconf/xfce-perchannel-xml/  XFCE config files
    ~/.bashrc                       DISPLAY environment variable
    /etc/sysctl.conf               System performance tuning (optional)

TROUBLESHOOTING:
    • Check logs: $LOG_FILE and $ERROR_LOG
    • Service status: systemctl --user status vncserver.service
    • Manual start: vncserver :1 -geometry 1920x1080 -depth 24 -localhost no
    • Test connection: vncserver -list

For more information, see the TigerVNC documentation at https://tigervnc.org/
EOF
}

#=============================================================================
# ARGUMENT PARSING
#=============================================================================

parse_arguments() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            --help|-h)
                show_help
                exit 0
                ;;
            --version|-v)
                echo "$SCRIPT_NAME v$VERSION"
                exit 0
                ;;
            --auto-yes)
                # For automation - dangerous, use with caution
                AUTO_YES=true
                shift
                ;;
            --localhost-only)
                FORCE_LOCALHOST=true
                shift
                ;;
            --external-access)
                FORCE_EXTERNAL=true
                shift
                ;;
            --skip-optimization)
                XFCE_OPT_LEVEL="none"
                shift
                ;;
            --skip-autostart)
                ENABLE_AUTOSTART=false
                shift
                ;;
            --display)
                DISPLAY_NUMBER="$2"
                shift 2
                ;;
            --geometry)
                VNC_GEOMETRY="$2"
                shift 2
                ;;
            --depth)
                VNC_DEPTH="$2"
                shift 2
                ;;
            *)
                echo "Unknown option: $1"
                echo "Use --help for usage information"
                exit 1
                ;;
        esac
    done
}

#=============================================================================
# MAIN INSTALLATION FLOW
#=============================================================================

main() {
    # Initialize
    register_cleanup
    log_info "Starting TigerVNC installation - version $VERSION"

    show_section "$SCRIPT_NAME v$VERSION"
    echo -e "${BLUE}Automated TigerVNC installation with XFCE4 optimization${NC}"
    echo -e "${BLUE}Based on successful manual troubleshooting session${NC}"
    echo ""

    # Parse command line arguments
    parse_arguments "$@"

    # Prerequisites and environment checks
    check_system_requirements
    check_dependencies
    check_permissions

    # Get user configuration preferences
    get_installation_preferences

    # Package installation
    install_tigervnc_packages

    # VNC configuration
    setup_vnc_password
    create_xstartup_script

    # XFCE4 optimization
    optimize_xfce4_performance

    # Systemd service setup
    create_systemd_service
    enable_and_start_service
    setup_user_lingering

    # Environment setup
    setup_display_environment

    # System performance tuning
    apply_performance_tuning

    # Verification
    verify_installation
    test_vnc_connection

    # Success
    show_completion_message

    log_info "TigerVNC installation completed successfully"
}

# Handle special command line options immediately
if [[ "$1" == "--help" ]] || [[ "$1" == "-h" ]]; then
    show_help
    exit 0
elif [[ "$1" == "--version" ]] || [[ "$1" == "-v" ]]; then
    echo "$SCRIPT_NAME v$VERSION"
    exit 0
fi

# Run main installation
main "$@"
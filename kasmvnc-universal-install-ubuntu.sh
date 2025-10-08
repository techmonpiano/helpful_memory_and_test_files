#!/bin/bash

# KasmVNC Universal Auto-Install Script for Ubuntu (All DEs)
# Created: July 4, 2025
# Supports: GNOME, KDE, XFCE, MATE, Cinnamon, LXDE, LXQt, Budgie
# 
# This script handles the desktop environment selection that KasmVNC prompts for
# and automatically configures the appropriate xstartup file with fixes for common issues

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

# Logging function
log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')] $1${NC}"
}

warn() {
    echo -e "${YELLOW}[WARNING] $1${NC}"
}

error() {
    echo -e "${RED}[ERROR] $1${NC}"
    exit 1
}

info() {
    echo -e "${BLUE}[INFO] $1${NC}"
}

highlight() {
    echo -e "${PURPLE}[HIGHLIGHT] $1${NC}"
}

# Check if running as root
if [ "$EUID" -eq 0 ]; then
    error "Please run this script as a normal user, not root. It will prompt for sudo when needed."
fi

# Detect OS and version
OS_ID=$(lsb_release -si 2>/dev/null || echo "Unknown")
OS_VERSION=$(lsb_release -sr 2>/dev/null || echo "Unknown")
OS_CODENAME=$(lsb_release -sc 2>/dev/null || echo "Unknown")

log "Starting KasmVNC Universal installation for $OS_ID $OS_VERSION ($OS_CODENAME)"

# Verify Ubuntu/Debian based system
if [[ ! "$OS_ID" =~ ^(Ubuntu|Zorin|Debian|LinuxMint|Pop)$ ]]; then
    warn "This script is designed for Ubuntu/Debian-based systems. Detected: $OS_ID"
    read -p "Continue anyway? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Function to detect installed desktop environments
detect_desktop_environments() {
    local des=()
    
    # Check for various desktop environments
    if dpkg -l | grep -q "gnome-session\|ubuntu-desktop\|zorin-desktop"; then
        des+=("GNOME/Ubuntu/Zorin")
    fi
    
    if dpkg -l | grep -q "kde-plasma-desktop\|kubuntu-desktop"; then
        des+=("KDE Plasma")
    fi
    
    if dpkg -l | grep -q "xfce4\|xubuntu-desktop"; then
        des+=("XFCE")
    fi
    
    if dpkg -l | grep -q "mate-desktop\|ubuntu-mate-desktop"; then
        des+=("MATE")
    fi
    
    if dpkg -l | grep -q "cinnamon-desktop-environment"; then
        des+=("Cinnamon")
    fi
    
    if dpkg -l | grep -q "lxde\|lubuntu-desktop"; then
        des+=("LXDE")
    fi
    
    if dpkg -l | grep -q "lxqt\|lubuntu-qt-desktop"; then
        des+=("LXQt")
    fi
    
    if dpkg -l | grep -q "budgie-desktop"; then
        des+=("Budgie")
    fi
    
    echo "${des[@]}"
}

# Function to install desktop environment packages
install_desktop_packages() {
    local de="$1"
    
    case "$de" in
        "gnome"|"ubuntu"|"zorin")
            log "Installing GNOME/Ubuntu desktop packages..."
            sudo apt install -y gnome-session gnome-panel gnome-settings-daemon metacity nautilus gnome-terminal ubuntu-desktop-minimal
            ;;
        "kde"|"plasma")
            log "Installing KDE Plasma packages..."
            sudo apt install -y kde-plasma-desktop plasma-workspace kwin-x11 dolphin konsole
            ;;
        "xfce")
            log "Installing XFCE packages..."
            sudo apt install -y xfce4 xfce4-goodies xfce4-terminal thunar
            ;;
        "mate")
            log "Installing MATE packages..."
            sudo apt install -y ubuntu-mate-desktop mate-session-manager caja mate-terminal
            ;;
        "cinnamon")
            log "Installing Cinnamon packages..."
            sudo apt install -y cinnamon-desktop-environment cinnamon-session nemo gnome-terminal
            ;;
        "lxde")
            log "Installing LXDE packages..."
            sudo apt install -y lxde-core lxterminal pcmanfm
            ;;
        "lxqt")
            log "Installing LXQt packages..."
            sudo apt install -y lxqt-core qterminal pcmanfm-qt
            ;;
        "budgie")
            log "Installing Budgie packages..."
            sudo apt install -y budgie-desktop budgie-desktop-environment gnome-terminal nautilus
            ;;
    esac
}

# Function to create xstartup for specific desktop environment
create_xstartup() {
    local de="$1"
    local hostname="$2"
    
    log "Creating xstartup file for $de desktop environment..."
    
    cat > ~/.vnc/xstartup << EOF
#!/bin/bash
# KasmVNC xstartup file for $de
# Auto-generated on $(date)

unset SESSION_MANAGER
unset DBUS_SESSION_BUS_ADDRESS
export XKL_XMODMAP_DISABLE=1
export XDG_SESSION_TYPE=x11
export DISPLAY=:3

# Create runtime directory
export XDG_RUNTIME_DIR=/tmp/runtime-\$(whoami)
mkdir -p \$XDG_RUNTIME_DIR
chmod 700 \$XDG_RUNTIME_DIR

# Optional: Disable keyring prompts for VNC session
# Uncomment these lines to disable keyring authorization prompts
# export GNOME_KEYRING_CONTROL=""
# export SSH_AUTH_SOCK=""

[ -r \$HOME/.Xresources ] && xrdb \$HOME/.Xresources
xsetroot -solid grey
vncconfig -iconic &

EOF

    case "$de" in
        "gnome"|"ubuntu")
            cat >> ~/.vnc/xstartup << 'EOF'
# Ubuntu GNOME Desktop Configuration
export XDG_CURRENT_DESKTOP=ubuntu:GNOME
export XDG_SESSION_DESKTOP=ubuntu
exec dbus-launch --exit-with-session gnome-session --session=ubuntu
EOF
            ;;
        "zorin")
            cat >> ~/.vnc/xstartup << 'EOF'
# Zorin Desktop Configuration
export XDG_CURRENT_DESKTOP=zorin:GNOME
export XDG_SESSION_DESKTOP=zorin
exec dbus-launch --exit-with-session gnome-session --session=zorin
EOF
            ;;
        "kde"|"plasma")
            cat >> ~/.vnc/xstartup << 'EOF'
# KDE Plasma Desktop Configuration
export XDG_CURRENT_DESKTOP=KDE
export XDG_SESSION_DESKTOP=KDE
export KDE_FULL_SESSION=true
export KDE_SESSION_VERSION=5
# Disable compositing for better VNC performance
export KWIN_COMPOSE=N
export KWIN_X11_NO_SYNC_TO_VBLANK=1
exec dbus-launch --exit-with-session startplasma-x11
EOF
            ;;
        "xfce")
            cat >> ~/.vnc/xstartup << 'EOF'
# XFCE Desktop Configuration
export XDG_CURRENT_DESKTOP=XFCE
export XDG_SESSION_DESKTOP=xfce
# Disable compositing for better VNC performance
export XFCE_DISABLE_COMPOSITING=1
exec dbus-launch --exit-with-session startxfce4
EOF
            ;;
        "mate")
            cat >> ~/.vnc/xstartup << 'EOF'
# MATE Desktop Configuration
export XDG_CURRENT_DESKTOP=MATE
export XDG_SESSION_DESKTOP=mate
# Disable compositing for better VNC performance
export MARCO_REDUCED_RESOURCES=1
exec dbus-launch --exit-with-session mate-session
EOF
            ;;
        "cinnamon")
            cat >> ~/.vnc/xstartup << 'EOF'
# Cinnamon Desktop Configuration
export XDG_CURRENT_DESKTOP=X-Cinnamon
export XDG_SESSION_DESKTOP=cinnamon
# Use 2D session for better VNC compatibility
exec dbus-launch --exit-with-session cinnamon-session --session=cinnamon2d
EOF
            ;;
        "lxde")
            cat >> ~/.vnc/xstartup << 'EOF'
# LXDE Desktop Configuration
export XDG_CURRENT_DESKTOP=LXDE
export XDG_SESSION_DESKTOP=LXDE
exec dbus-launch --exit-with-session startlxde
EOF
            ;;
        "lxqt")
            cat >> ~/.vnc/xstartup << 'EOF'
# LXQt Desktop Configuration
export XDG_CURRENT_DESKTOP=LXQt
export XDG_SESSION_DESKTOP=LXQt
exec dbus-launch --exit-with-session startlxqt
EOF
            ;;
        "budgie")
            cat >> ~/.vnc/xstartup << 'EOF'
# Budgie Desktop Configuration
export XDG_CURRENT_DESKTOP=Budgie:GNOME
export XDG_SESSION_DESKTOP=budgie-desktop
exec dbus-launch --exit-with-session budgie-desktop
EOF
            ;;
        *)
            # Fallback to generic GNOME
            cat >> ~/.vnc/xstartup << 'EOF'
# Generic GNOME Desktop Configuration (Fallback)
export XDG_CURRENT_DESKTOP=GNOME
export XDG_SESSION_DESKTOP=gnome
exec dbus-launch --exit-with-session gnome-session
EOF
            ;;
    esac
    
    chmod +x ~/.vnc/xstartup
}

# Main installation function
main_install() {
    # Update package lists
    log "Updating package lists..."
    sudo apt update

    # Install common dependencies
    log "Installing common dependencies..."
    sudo apt install -y \
        wget \
        curl \
        gnupg \
        software-properties-common \
        dbus-x11 \
        xorg \
        x11-xserver-utils

    # Detect existing desktop environments
    highlight "Detecting installed desktop environments..."
    detected_des=($(detect_desktop_environments))
    
    if [ ${#detected_des[@]} -gt 0 ]; then
        info "Detected desktop environments: ${detected_des[*]}"
    else
        warn "No desktop environments detected. You'll need to install one."
    fi

    # Download and install KasmVNC
    log "Downloading KasmVNC..."
    ARCH=$(dpkg --print-architecture)
    KASMVNC_VERSION="1.0.3"
    
    # Determine package based on Ubuntu version
    if [[ "$OS_VERSION" == "24.04" ]] || [[ "$OS_CODENAME" == "noble" ]]; then
        PACKAGE_BASE="jammy"  # Use Jammy package for Noble compatibility
    elif [[ "$OS_VERSION" == "22.04" ]] || [[ "$OS_CODENAME" == "jammy" ]]; then
        PACKAGE_BASE="jammy"
    elif [[ "$OS_VERSION" == "20.04" ]] || [[ "$OS_CODENAME" == "focal" ]]; then
        PACKAGE_BASE="focal"
    else
        PACKAGE_BASE="jammy"  # Default fallback
    fi
    
    KASMVNC_URL="https://github.com/kasmtech/KasmVNC/releases/download/v${KASMVNC_VERSION}/kasmvncserver_${PACKAGE_BASE}_${KASMVNC_VERSION}_${ARCH}.deb"

    TEMP_DIR=$(mktemp -d)
    cd "$TEMP_DIR"

    log "Downloading from: $KASMVNC_URL"
    wget "$KASMVNC_URL" -O kasmvnc.deb

    log "Installing KasmVNC package..."
    sudo dpkg -i kasmvnc.deb
    sudo apt-get install -f -y

    # Create VNC directory
    mkdir -p ~/.vnc

    # Set VNC password
    log "Setting up VNC password..."
    info "You will be prompted to set a VNC password (for vncuser1 access)"
    vncpasswd

    # Now KasmVNC will ask for desktop environment selection
    highlight "Starting initial VNC server to detect/select desktop environment..."
    info "KasmVNC will now ask you to select a desktop environment."
    info "The script will automatically configure the xstartup file based on your selection."
    
    # Start vncserver to trigger DE selection
    if vncserver :3; then
        log "VNC server started successfully"
        vncserver -kill :3  # Stop it so we can configure properly
    else
        error "Failed to start VNC server initially"
    fi

    # Detect hostname for PID file configuration
    HOSTNAME=$(hostname)
    log "Detected hostname: $HOSTNAME"

    # Read the generated xstartup to determine selected DE
    if [ -f ~/.vnc/xstartup ]; then
        log "Analyzing generated xstartup file to determine selected desktop environment..."
        
        # Detect which DE was selected based on xstartup content
        if grep -q "zorin" ~/.vnc/xstartup; then
            SELECTED_DE="zorin"
        elif grep -q "ubuntu.*gnome\|gnome-session.*ubuntu" ~/.vnc/xstartup; then
            SELECTED_DE="ubuntu"
        elif grep -q "startplasma\|startkde\|kde" ~/.vnc/xstartup; then
            SELECTED_DE="kde"
        elif grep -q "startxfce4\|xfce" ~/.vnc/xstartup; then
            SELECTED_DE="xfce"
        elif grep -q "mate-session\|mate" ~/.vnc/xstartup; then
            SELECTED_DE="mate"
        elif grep -q "cinnamon" ~/.vnc/xstartup; then
            SELECTED_DE="cinnamon"
        elif grep -q "startlxde\|lxde" ~/.vnc/xstartup; then
            SELECTED_DE="lxde"
        elif grep -q "startlxqt\|lxqt" ~/.vnc/xstartup; then
            SELECTED_DE="lxqt"
        elif grep -q "budgie" ~/.vnc/xstartup; then
            SELECTED_DE="budgie"
        else
            SELECTED_DE="gnome"  # fallback
        fi
        
        log "Detected selected desktop environment: $SELECTED_DE"
        
        # Install packages for selected DE if needed
        install_desktop_packages "$SELECTED_DE"
        
        # Create optimized xstartup file for the selected DE
        create_xstartup "$SELECTED_DE" "$HOSTNAME"
        
    else
        warn "No xstartup file found. Creating default GNOME configuration."
        create_xstartup "gnome" "$HOSTNAME"
    fi

    # Create systemd service file with correct PID path
    log "Creating systemd service configuration..."
    sudo tee /etc/systemd/system/kasmvnc@.service > /dev/null << EOF
[Unit]
Description=KasmVNC Server for %i
After=syslog.target network.target

[Service]
Type=forking
User=%i
Group=%i
WorkingDirectory=/home/%i
PIDFile=/home/%i/.vnc/${HOSTNAME}:3.pid
ExecStartPre=/bin/sh -c '/usr/bin/vncserver -kill :3 > /dev/null 2>&1 || :'
ExecStart=/usr/bin/vncserver :3
ExecStop=/usr/bin/vncserver -kill :3
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

    # Reload systemd and enable service
    log "Configuring systemd service..."
    sudo systemctl daemon-reload
    sudo systemctl enable kasmvnc@$(whoami).service

    # Start the service
    log "Starting KasmVNC service with optimized configuration..."
    sudo systemctl start kasmvnc@$(whoami).service

    # Wait for service to start
    sleep 5

    # Check service status
    log "Checking service status..."
    if sudo systemctl is-active --quiet kasmvnc@$(whoami).service; then
        log "✅ KasmVNC service is running successfully with $SELECTED_DE desktop!"
    else
        warn "Service may not be running properly. Checking status..."
        sudo systemctl status kasmvnc@$(whoami).service
    fi

    # Get local IP address
    LOCAL_IP=$(hostname -I | awk '{print $1}')

    # Display connection information
    echo
    echo "=========================================="
    echo -e "${GREEN}🎉 KasmVNC Universal Installation Complete! 🎉${NC}"
    echo "=========================================="
    echo
    echo -e "${BLUE}Configuration Summary:${NC}"
    echo "  • Desktop Environment: $SELECTED_DE"
    echo "  • Hostname: $HOSTNAME"
    echo "  • VNC Display: :3"
    echo "  • PID File: ~/.vnc/${HOSTNAME}:3.pid"
    echo
    echo -e "${BLUE}Connection Information:${NC}"
    echo "  • URL: https://${LOCAL_IP}:8446"
    echo "  • Username: vncuser1"
    echo "  • Password: [The password you set during installation]"
    echo
    echo -e "${BLUE}Service Management:${NC}"
    echo "  • Status: sudo systemctl status kasmvnc@$(whoami).service"
    echo "  • Stop:   sudo systemctl stop kasmvnc@$(whoami).service"
    echo "  • Start:  sudo systemctl start kasmvnc@$(whoami).service"
    echo "  • Logs:   journalctl -u kasmvnc@$(whoami).service -f"
    echo
    echo -e "${BLUE}Configuration Files:${NC}"
    echo "  • xstartup: ~/.vnc/xstartup (optimized for $SELECTED_DE)"
    echo "  • Service:  /etc/systemd/system/kasmvnc@.service"
    echo "  • Logs:     ~/.vnc/${HOSTNAME}:3.log"
    echo
    echo -e "${YELLOW}Desktop Environment Specific Features:${NC}"
    case "$SELECTED_DE" in
        "kde"|"plasma")
            echo "  • Compositing disabled for better VNC performance"
            echo "  • KDE-specific environment variables configured"
            ;;
        "xfce")
            echo "  • XFCE compositing disabled for better performance"
            echo "  • Lightweight desktop optimized for VNC"
            ;;
        "mate")
            echo "  • MATE compositing optimizations applied"
            echo "  • Traditional desktop interface"
            ;;
        "cinnamon")
            echo "  • Cinnamon 2D session for VNC compatibility"
            echo "  • Hardware acceleration safely disabled"
            ;;
        *)
            echo "  • Standard desktop environment configuration"
            ;;
    esac
    echo
    echo -e "${YELLOW}Keyring Configuration (Optional):${NC}"
    echo "If you get authorization prompts:"
    echo "1. Enter your user password when prompted, OR"
    echo "2. Edit ~/.vnc/xstartup and uncomment the GNOME_KEYRING_CONTROL lines"
    echo "3. Or disable keyring password globally via 'Passwords and Keys' app"
    echo
    echo -e "${GREEN}Available Features:${NC}"
    echo "  ✅ Full $SELECTED_DE desktop environment"
    echo "  ✅ Application menus and panels"
    echo "  ✅ Right-click context menus"
    echo "  ✅ File manager integration"
    echo "  ✅ Terminal access"
    echo "  ✅ Desktop environment optimizations"
    echo "  ✅ Automatic PID file configuration"
    echo

    # Cleanup
    cd /
    rm -rf "$TEMP_DIR"

    log "Universal installation completed successfully!"
    log "Access your $SELECTED_DE desktop at: https://${LOCAL_IP}:8446"
}

# Check if KasmVNC is already installed
if command -v vncserver >/dev/null 2>&1; then
    warn "VNC server already detected on system."
    read -p "Continue with installation anyway? This will reconfigure existing setup. (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Run main installation
main_install

exit 0
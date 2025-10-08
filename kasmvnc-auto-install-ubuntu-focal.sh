#!/bin/bash

# KasmVNC Auto-Install Script for Ubuntu Focal (20.04) and Derivatives
# Created: July 4, 2025
# Based on successful Zorin OS setup session
# 
# This script automatically installs and configures KasmVNC with full desktop functionality
# Includes fixes for common issues: PID file paths, desktop environment configuration, keyring handling

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
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

# Check if running as root
if [ "$EUID" -eq 0 ]; then
    error "Please run this script as a normal user, not root. It will prompt for sudo when needed."
fi

# Detect OS and version
OS_ID=$(lsb_release -si 2>/dev/null || echo "Unknown")
OS_VERSION=$(lsb_release -sr 2>/dev/null || echo "Unknown")
OS_CODENAME=$(lsb_release -sc 2>/dev/null || echo "Unknown")

log "Starting KasmVNC installation for $OS_ID $OS_VERSION ($OS_CODENAME)"

# Verify Ubuntu/Debian based system
if [[ ! "$OS_ID" =~ ^(Ubuntu|Zorin|Debian|LinuxMint)$ ]]; then
    warn "This script is designed for Ubuntu/Debian-based systems. Detected: $OS_ID"
    read -p "Continue anyway? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Check if KasmVNC is already installed
if command -v vncserver >/dev/null 2>&1; then
    warn "VNC server already detected on system."
    read -p "Continue with installation anyway? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Update package lists
log "Updating package lists..."
sudo apt update

# Install required dependencies
log "Installing required dependencies..."
sudo apt install -y \
    wget \
    gnupg \
    software-properties-common \
    dbus-x11 \
    gnome-panel \
    gnome-settings-daemon \
    metacity \
    nautilus \
    gnome-terminal \
    gnome-session \
    ubuntu-desktop-minimal

# Download and install KasmVNC
log "Downloading KasmVNC..."

# Determine architecture
ARCH=$(dpkg --print-architecture)
log "Detected architecture: $ARCH"

# KasmVNC download URL (update version as needed)
KASMVNC_VERSION="1.0.3"
if [ "$ARCH" = "amd64" ]; then
    KASMVNC_URL="https://github.com/kasmtech/KasmVNC/releases/download/v${KASMVNC_VERSION}/kasmvncserver_focal_${KASMVNC_VERSION}_amd64.deb"
elif [ "$ARCH" = "arm64" ]; then
    KASMVNC_URL="https://github.com/kasmtech/KasmVNC/releases/download/v${KASMVNC_VERSION}/kasmvncserver_focal_${KASMVNC_VERSION}_arm64.deb"
else
    error "Unsupported architecture: $ARCH"
fi

# Create temporary directory
TEMP_DIR=$(mktemp -d)
cd "$TEMP_DIR"

log "Downloading from: $KASMVNC_URL"
wget "$KASMVNC_URL" -O kasmvnc.deb

# Install KasmVNC
log "Installing KasmVNC package..."
sudo dpkg -i kasmvnc.deb

# Fix any dependency issues
sudo apt-get install -f -y

# Create VNC directory
log "Setting up VNC configuration..."
mkdir -p ~/.vnc

# Set VNC password
log "Setting up VNC password..."
info "You will be prompted to set a VNC password (for vncuser1 access)"
vncpasswd

# Detect hostname for PID file configuration
HOSTNAME=$(hostname)
log "Detected hostname: $HOSTNAME"

# Create optimized xstartup file
log "Creating optimized xstartup configuration..."
cat > ~/.vnc/xstartup << 'EOF'
#!/bin/sh
unset SESSION_MANAGER
unset DBUS_SESSION_BUS_ADDRESS
export XKL_XMODMAP_DISABLE=1

# Auto-detect desktop environment
if [ -f /usr/share/gnome-session/sessions/zorin.session ]; then
    # Zorin OS detected
    export XDG_CURRENT_DESKTOP=zorin:GNOME
    export XDG_SESSION_DESKTOP=zorin
    SESSION_TYPE="zorin"
elif [ -f /usr/share/gnome-session/sessions/ubuntu.session ]; then
    # Ubuntu detected
    export XDG_CURRENT_DESKTOP=ubuntu:GNOME
    export XDG_SESSION_DESKTOP=ubuntu
    SESSION_TYPE="ubuntu"
else
    # Generic GNOME fallback
    export XDG_CURRENT_DESKTOP=GNOME
    export XDG_SESSION_DESKTOP=gnome
    SESSION_TYPE="gnome"
fi

export XDG_SESSION_TYPE=x11
export DISPLAY=:3

# Create runtime directory
export XDG_RUNTIME_DIR=/tmp/runtime-$(whoami)
mkdir -p $XDG_RUNTIME_DIR
chmod 700 $XDG_RUNTIME_DIR

# Optional: Disable keyring prompts for VNC session
# Uncomment these lines to disable keyring authorization prompts
# export GNOME_KEYRING_CONTROL=""
# export SSH_AUTH_SOCK=""

[ -r $HOME/.Xresources ] && xrdb $HOME/.Xresources
xsetroot -solid grey
vncconfig -iconic &

# Disable screen lock and screensaver for VNC session
gsettings set org.gnome.desktop.screensaver lock-enabled false
gsettings set org.gnome.desktop.screensaver idle-activation-enabled false
gsettings set org.gnome.desktop.session idle-delay 0

# Start appropriate desktop session
exec dbus-launch --exit-with-session gnome-session --session=$SESSION_TYPE
EOF

# Make xstartup executable
chmod +x ~/.vnc/xstartup

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
log "Starting KasmVNC service..."
sudo systemctl start kasmvnc@$(whoami).service

# Wait a moment for service to start
sleep 3

# Check service status
log "Checking service status..."
if sudo systemctl is-active --quiet kasmvnc@$(whoami).service; then
    log "✅ KasmVNC service is running successfully!"
else
    warn "Service may not be running properly. Checking status..."
    sudo systemctl status kasmvnc@$(whoami).service
fi

# Get local IP address
LOCAL_IP=$(hostname -I | awk '{print $1}')

# Display connection information
echo
echo "=========================================="
echo -e "${GREEN}🎉 KasmVNC Installation Complete! 🎉${NC}"
echo "=========================================="
echo
echo -e "${BLUE}Connection Information:${NC}"
echo "  • URL: https://${LOCAL_IP}:8446"
echo "  • Alternative: https://localhost:8446 (if local)"
echo "  • Username: vncuser1"
echo "  • Password: [The password you set during installation]"
echo "  • VNC Display: :3"
echo
echo -e "${BLUE}Service Management:${NC}"
echo "  • Status: sudo systemctl status kasmvnc@$(whoami).service"
echo "  • Stop:   sudo systemctl stop kasmvnc@$(whoami).service"
echo "  • Start:  sudo systemctl start kasmvnc@$(whoami).service"
echo "  • Logs:   journalctl -u kasmvnc@$(whoami).service -f"
echo
echo -e "${BLUE}Configuration Files:${NC}"
echo "  • xstartup: ~/.vnc/xstartup"
echo "  • Service:  /etc/systemd/system/kasmvnc@.service"
echo "  • Logs:     ~/.vnc/${HOSTNAME}:3.log"
echo
echo -e "${YELLOW}Optional Keyring Configuration:${NC}"
echo "If you get authorization prompts, you can:"
echo "1. Enter your user password when prompted, OR"
echo "2. Disable keyring prompts by editing ~/.vnc/xstartup"
echo "   (uncomment the GNOME_KEYRING_CONTROL lines)"
echo "3. Or disable keyring password globally via 'Passwords and Keys' app"
echo
echo -e "${GREEN}Desktop Features Available:${NC}"
echo "  ✅ Full desktop environment"
echo "  ✅ Application menus and panels"
echo "  ✅ Right-click context menus"
echo "  ✅ File manager integration"
echo "  ✅ Terminal access"
echo

# Cleanup
cd /
rm -rf "$TEMP_DIR"

log "Installation script completed successfully!"
log "You can now access your desktop at https://${LOCAL_IP}:8446"

exit 0
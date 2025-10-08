#!/bin/bash

# Docker CE and Portainer CE Auto-Installation Script
# Created: 2025-09-24
# Description: Automates complete Docker CE and Portainer CE installation on Ubuntu

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to check if user is in docker group
user_in_docker_group() {
    groups "$USER" | grep -q docker
}

# Function to prompt for sudo password upfront
get_sudo_access() {
    print_status "This script requires sudo privileges for Docker installation."
    print_status "You may be prompted for your password..."

    # Test sudo access and keep it alive
    if ! sudo -v; then
        print_error "Failed to obtain sudo privileges. Exiting."
        exit 1
    fi

    # Keep sudo alive throughout the script
    while true; do
        sudo -n true
        sleep 60
        kill -0 "$$" || exit
    done 2>/dev/null &
}

# Function to detect architecture
detect_arch() {
    case $(uname -m) in
        x86_64) echo "amd64" ;;
        aarch64|arm64) echo "arm64" ;;
        armv7l) echo "armhf" ;;
        *) echo "amd64" ;;  # Default fallback
    esac
}

# Function to get Ubuntu codename
get_ubuntu_codename() {
    lsb_release -cs
}

# Main installation function
main() {
    print_status "Starting Docker CE and Portainer CE installation..."
    print_status "Detected OS: $(lsb_release -d | cut -f2)"
    print_status "Architecture: $(detect_arch)"

    # Get sudo access upfront
    get_sudo_access

    # Step 1: Update package lists and install prerequisites
    print_status "Step 1: Installing prerequisites..."
    sudo apt update
    sudo apt install -y \
        apt-transport-https \
        ca-certificates \
        curl \
        gnupg \
        lsb-release \
        software-properties-common
    print_success "Prerequisites installed successfully"

    # Step 2: Add Docker's official GPG key
    print_status "Step 2: Adding Docker's official GPG key..."
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
    print_success "Docker GPG key added successfully"

    # Step 3: Add Docker repository
    print_status "Step 3: Adding Docker repository..."
    ARCH=$(detect_arch)
    CODENAME=$(get_ubuntu_codename)

    echo "deb [arch=${ARCH} signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu ${CODENAME} stable" | \
        sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
    print_success "Docker repository added successfully"

    # Step 4: Update package lists again
    print_status "Step 4: Updating package lists with Docker repository..."
    sudo apt update
    print_success "Package lists updated successfully"

    # Step 5: Install Docker CE
    print_status "Step 5: Installing Docker CE and components..."
    sudo apt install -y \
        docker-ce \
        docker-ce-cli \
        containerd.io \
        docker-buildx-plugin \
        docker-compose-plugin
    print_success "Docker CE installed successfully"

    # Step 6: Start and enable Docker service
    print_status "Step 6: Starting and enabling Docker service..."
    sudo systemctl start docker
    sudo systemctl enable docker
    print_success "Docker service started and enabled"

    # Step 7: Add current user to docker group
    print_status "Step 7: Adding user '$USER' to docker group..."
    sudo usermod -aG docker "$USER"
    print_success "User '$USER' added to docker group"

    # Step 8: Create new group session for docker group
    print_status "Step 8: Refreshing group membership..."
    print_warning "Note: You may need to log out and back in for full group membership"

    # Step 9: Test Docker installation (with newgrp to activate docker group)
    print_status "Step 9: Testing Docker installation..."
    if newgrp docker <<EOF
docker --version
docker compose version
EOF
    then
        print_success "Docker installation test passed"
    else
        print_warning "Docker test failed - you may need to restart your session"
    fi

    # Step 10: Install Portainer CE
    print_status "Step 10: Installing Portainer CE..."

    # Create Portainer data volume
    if newgrp docker <<EOF
docker volume create portainer_data
EOF
    then
        print_success "Portainer data volume created"
    else
        print_error "Failed to create Portainer volume"
        return 1
    fi

    # Run Portainer container
    if newgrp docker <<EOF
docker run -d \\
    -p 8000:8000 \\
    -p 9443:9443 \\
    --name portainer \\
    --restart=always \\
    -v /var/run/docker.sock:/var/run/docker.sock \\
    -v portainer_data:/data \\
    portainer/portainer-ce:latest
EOF
    then
        print_success "Portainer CE container started successfully"
    else
        print_error "Failed to start Portainer container"
        return 1
    fi

    # Step 11: Verification
    print_status "Step 11: Verifying installations..."

    # Check Docker
    if command_exists docker; then
        DOCKER_VERSION=$(docker --version 2>/dev/null || echo "Version check failed")
        print_success "Docker CE: $DOCKER_VERSION"
    else
        print_error "Docker command not found"
    fi

    # Check Docker Compose
    if docker compose version >/dev/null 2>&1; then
        COMPOSE_VERSION=$(docker compose version 2>/dev/null || echo "Version check failed")
        print_success "Docker Compose: $COMPOSE_VERSION"
    else
        print_error "Docker Compose not working"
    fi

    # Check Portainer container
    if newgrp docker <<EOF
docker ps --filter "name=portainer" --format "table {{.Names}}\t{{.Status}}" | grep -q portainer
EOF
    then
        print_success "Portainer CE container is running"
    else
        print_error "Portainer container not running"
    fi

    # Final success message
    echo ""
    print_success "======================================"
    print_success "  INSTALLATION COMPLETED SUCCESSFULLY  "
    print_success "======================================"
    echo ""
    print_status "Docker CE and Portainer CE have been installed successfully!"
    echo ""
    print_status "Access Information:"
    echo "  • Portainer Web UI (HTTPS): https://localhost:9443"
    echo "  • Portainer Web UI (HTTP):  http://localhost:8000"
    echo ""
    print_warning "Important Notes:"
    echo "  • Create your Portainer admin account on first login"
    echo "  • You may need to log out and back in to use Docker without sudo"
    echo "  • Alternatively, run: newgrp docker"
    echo ""
    print_status "Docker Commands Test:"
    echo "  docker --version"
    echo "  docker compose version"
    echo "  docker ps"
    echo ""
}

# Function to handle script interruption
cleanup() {
    print_warning "Script interrupted. Cleaning up..."
    # Kill the sudo keepalive background process
    jobs -p | xargs -r kill
    exit 1
}

# Set trap for cleanup
trap cleanup SIGINT SIGTERM

# Check if running on Ubuntu
if ! command_exists lsb_release || [[ $(lsb_release -si) != "Ubuntu" ]]; then
    print_error "This script is designed for Ubuntu systems only."
    exit 1
fi

# Check if Docker is already installed
if command_exists docker; then
    print_warning "Docker appears to be already installed."
    read -p "Do you want to continue anyway? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        print_status "Installation cancelled."
        exit 0
    fi
fi

# Show disclaimer
echo ""
print_warning "DISCLAIMER:"
echo "This script will install Docker CE and Portainer CE on your system."
echo "It will make changes to your system packages and configuration."
echo ""
read -p "Do you want to continue? (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    print_status "Installation cancelled."
    exit 0
fi

# Run main installation
main

# Clean up background sudo keepalive
jobs -p | xargs -r kill >/dev/null 2>&1 || true

print_success "Script completed successfully!"
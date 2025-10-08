#!/bin/bash

# Claude Desktop Multiple Instances Install Script
# Automatically sets up multiple Claude Desktop instances on Linux
# Created: September 5, 2025
# Compatible with: Ubuntu, Debian, and derivatives

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
INSTANCES=("main" "work" "personal")
BIN_DIR="$HOME/bin"
CONFIG_BASE="$HOME/.config"
DESKTOP_DIR="$HOME/.local/share/applications"

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

# Main installation function
main() {
    print_status "Starting Claude Desktop Multiple Instances Installation..."
    echo "=================================================="
    
    # Check prerequisites
    check_prerequisites
    
    # Create directory structure
    create_directories
    
    # Create launcher scripts
    create_launcher_scripts
    
    # Configure MCP settings
    configure_mcp_settings
    
    # Create desktop entries
    create_desktop_entries
    
    # Update PATH
    update_path
    
    # Final verification
    verify_installation
    
    print_success "Installation completed successfully!"
    show_usage_instructions
}

check_prerequisites() {
    print_status "Checking prerequisites..."
    
    if ! command_exists claude-desktop; then
        print_error "Claude Desktop is not installed. Please install it first."
        print_status "You can install it from: https://github.com/aaddrick/claude-desktop-debian"
        exit 1
    fi
    
    print_success "Claude Desktop found at $(which claude-desktop)"
    
    # Check if Claude Desktop is currently running
    if pgrep -f "claude-desktop" >/dev/null; then
        print_warning "Claude Desktop is currently running. You may want to close it first."
        read -p "Continue anyway? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            print_status "Installation cancelled."
            exit 0
        fi
    fi
}

create_directories() {
    print_status "Creating directory structure..."
    
    # Create bin directory
    mkdir -p "$BIN_DIR"
    print_success "Created $BIN_DIR"
    
    # Create config directories for each instance
    for instance in "${INSTANCES[@]}"; do
        config_dir="$CONFIG_BASE/Claude-${instance^}"
        mkdir -p "$config_dir"
        print_success "Created $config_dir"
    done
    
    # Create desktop entries directory
    mkdir -p "$DESKTOP_DIR"
    print_success "Created $DESKTOP_DIR"
}

create_launcher_scripts() {
    print_status "Creating launcher scripts..."
    
    # Main instance
    cat > "$BIN_DIR/claude-main" << 'EOF'
#!/bin/bash
# Claude Desktop Main Instance Launcher
# Uses default configuration location

echo "Starting Claude Desktop - Main Instance..."
exec claude-desktop --user-data-dir="$HOME/.config/Claude-Main" --no-single-instance-lock "$@"
EOF
    
    # Work instance
    cat > "$BIN_DIR/claude-work" << 'EOF'
#!/bin/bash
# Claude Desktop Work Instance Launcher
# For work-related projects and MCP configurations

echo "Starting Claude Desktop - Work Instance..."
exec claude-desktop --user-data-dir="$HOME/.config/Claude-Work" --no-single-instance-lock "$@"
EOF
    
    # Personal instance
    cat > "$BIN_DIR/claude-personal" << 'EOF'
#!/bin/bash
# Claude Desktop Personal Instance Launcher  
# For personal projects and experiments

echo "Starting Claude Desktop - Personal Instance..."
exec claude-desktop --user-data-dir="$HOME/.config/Claude-Personal" --no-single-instance-lock "$@"
EOF
    
    # Make scripts executable
    chmod +x "$BIN_DIR/claude-main" "$BIN_DIR/claude-work" "$BIN_DIR/claude-personal"
    print_success "Created and configured launcher scripts"
}

configure_mcp_settings() {
    print_status "Configuring MCP settings for each instance..."
    
    # Check if existing MCP config exists
    existing_config=""
    if [[ -f "$CONFIG_BASE/chromium/claude_desktop_config.json" ]]; then
        existing_config="$CONFIG_BASE/chromium/claude_desktop_config.json"
    elif [[ -f "$CONFIG_BASE/Claude/claude_desktop_config.json" ]]; then
        existing_config="$CONFIG_BASE/Claude/claude_desktop_config.json"
    fi
    
    # Main instance configuration
    cat > "$CONFIG_BASE/Claude-Main/claude_desktop_config.json" << 'EOF'
{
  "serverConfig": {
    "command": "/bin/sh",
    "args": [
      "-c"
    ]
  },
  "autoApprove": {
    "mcpServers": ["desktop-commander", "context7-mcp", "tess"]
  },
  "mcpServers": {
    "desktop-commander": {
      "command": "/usr/bin/npx",
      "args": [
        "-y",
        "@wonderwhy-er/desktop-commander@latest"
      ]
    },
    "context7-mcp": {
      "command": "/usr/bin/npx",
      "args": [
        "-y",
        "@smithery/cli@latest",
        "run",
        "@upstash/context7-mcp",
        "--key",
        "dc11188a-2261-4821-be80-14793124eb38"
      ]
    },
    "tess": {
      "command": "/usr/bin/npx",
      "args": [
        "-y",
        "mcp-tess"
      ],
      "env": {
        "TESS_API_KEY": "${TESS_API_KEY}"
      }
    }
  }
}
EOF
    
    # Work instance configuration (with Playwright)
    cat > "$CONFIG_BASE/Claude-Work/claude_desktop_config.json" << 'EOF'
{
  "serverConfig": {
    "command": "/bin/sh",
    "args": [
      "-c"
    ]
  },
  "autoApprove": {
    "mcpServers": ["desktop-commander", "context7-mcp", "tess", "playwright"]
  },
  "mcpServers": {
    "desktop-commander": {
      "command": "/usr/bin/npx",
      "args": [
        "-y",
        "@wonderwhy-er/desktop-commander@latest"
      ]
    },
    "context7-mcp": {
      "command": "/usr/bin/npx",
      "args": [
        "-y",
        "@smithery/cli@latest",
        "run",
        "@upstash/context7-mcp",
        "--key",
        "dc11188a-2261-4821-be80-14793124eb38"
      ]
    },
    "tess": {
      "command": "/usr/bin/npx",
      "args": [
        "-y",
        "mcp-tess"
      ],
      "env": {
        "TESS_API_KEY": "${TESS_API_KEY}"
      }
    },
    "playwright": {
      "command": "/usr/bin/npx",
      "args": [
        "-y",
        "@playwright/cli@latest",
        "mcp"
      ]
    }
  }
}
EOF
    
    # Personal instance configuration (minimal)
    cat > "$CONFIG_BASE/Claude-Personal/claude_desktop_config.json" << 'EOF'
{
  "serverConfig": {
    "command": "/bin/sh",
    "args": [
      "-c"
    ]
  },
  "autoApprove": {
    "mcpServers": ["desktop-commander", "context7-mcp"]
  },
  "mcpServers": {
    "desktop-commander": {
      "command": "/usr/bin/npx",
      "args": [
        "-y",
        "@wonderwhy-er/desktop-commander@latest"
      ]
    },
    "context7-mcp": {
      "command": "/usr/bin/npx",
      "args": [
        "-y",
        "@smithery/cli@latest",
        "run",
        "@upstash/context7-mcp",
        "--key",
        "dc11188a-2261-4821-be80-14793124eb38"
      ]
    }
  }
}
EOF
    
    print_success "MCP configurations created for all instances"
    
    if [[ -n "$existing_config" ]]; then
        print_status "Found existing MCP config at: $existing_config"
        print_status "You may want to customize the new configs with your specific settings"
    fi
}

create_desktop_entries() {
    print_status "Creating desktop entries..."
    
    # Find Claude Desktop icon
    icon_path="/usr/lib/claude-desktop/resources/app.asar.unpacked/assets/claude-app-icon.png"
    if [[ ! -f "$icon_path" ]]; then
        # Fallback icon search
        icon_path=$(find /usr -name "*claude*icon*" 2>/dev/null | head -1)
        if [[ -z "$icon_path" ]]; then
            icon_path="claude-desktop"  # Use system icon name
        fi
    fi
    
    # Main instance desktop entry
    cat > "$DESKTOP_DIR/claude-main.desktop" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=Claude Desktop (Main)
Comment=Main Claude Desktop instance with full MCP tools
Exec=$BIN_DIR/claude-main
Icon=$icon_path
Terminal=false
StartupNotify=true
Categories=Office;Development;
EOF
    
    # Work instance desktop entry
    cat > "$DESKTOP_DIR/claude-work.desktop" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=Claude Desktop (Work)
Comment=Work-focused Claude Desktop instance with Playwright and MCP tools
Exec=$BIN_DIR/claude-work
Icon=$icon_path
Terminal=false
StartupNotify=true
Categories=Office;Development;
EOF
    
    # Personal instance desktop entry
    cat > "$DESKTOP_DIR/claude-personal.desktop" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=Claude Desktop (Personal)
Comment=Personal Claude Desktop instance for experiments and learning
Exec=$BIN_DIR/claude-personal
Icon=$icon_path
Terminal=false
StartupNotify=true
Categories=Office;Development;
EOF
    
    # Make desktop entries executable
    chmod +x "$DESKTOP_DIR"/claude-*.desktop
    
    # Update desktop database
    if command_exists update-desktop-database; then
        update-desktop-database "$DESKTOP_DIR" 2>/dev/null || true
        print_success "Desktop database updated"
    fi
    
    print_success "Desktop entries created"
}

update_path() {
    print_status "Updating PATH configuration..."
    
    # Check if ~/bin is already in PATH
    if [[ ":$PATH:" != *":$BIN_DIR:"* ]]; then
        # Add to .bashrc if it exists
        if [[ -f "$HOME/.bashrc" ]]; then
            echo '' >> "$HOME/.bashrc"
            echo '# Added by Claude Desktop Multiple Instances installer' >> "$HOME/.bashrc"
            echo 'export PATH="$HOME/bin:$PATH"' >> "$HOME/.bashrc"
            print_success "Added $BIN_DIR to PATH in .bashrc"
        fi
        
        # Add to .profile as fallback
        if [[ -f "$HOME/.profile" ]]; then
            echo '' >> "$HOME/.profile"
            echo '# Added by Claude Desktop Multiple Instances installer' >> "$HOME/.profile"
            echo 'export PATH="$HOME/bin:$PATH"' >> "$HOME/.profile"
            print_success "Added $BIN_DIR to PATH in .profile"
        fi
        
        # Export for current session
        export PATH="$BIN_DIR:$PATH"
        print_status "PATH updated for current session"
    else
        print_status "PATH already includes $BIN_DIR"
    fi
}

verify_installation() {
    print_status "Verifying installation..."
    
    # Check launcher scripts
    for instance in "${INSTANCES[@]}"; do
        script_path="$BIN_DIR/claude-${instance}"
        if [[ -x "$script_path" ]]; then
            print_success "✓ Launcher script: claude-${instance}"
        else
            print_error "✗ Launcher script missing: claude-${instance}"
        fi
    done
    
    # Check config files
    for instance in "${INSTANCES[@]}"; do
        config_path="$CONFIG_BASE/Claude-${instance^}/claude_desktop_config.json"
        if [[ -f "$config_path" ]]; then
            print_success "✓ Config file: Claude-${instance^}/claude_desktop_config.json"
        else
            print_error "✗ Config file missing: Claude-${instance^}/claude_desktop_config.json"
        fi
    done
    
    # Check desktop entries
    for instance in "${INSTANCES[@]}"; do
        desktop_path="$DESKTOP_DIR/claude-${instance}.desktop"
        if [[ -f "$desktop_path" ]]; then
            print_success "✓ Desktop entry: claude-${instance}.desktop"
        else
            print_error "✗ Desktop entry missing: claude-${instance}.desktop"
        fi
    done
}

show_usage_instructions() {
    echo ""
    echo "=================================================="
    print_success "Claude Desktop Multiple Instances Setup Complete!"
    echo "=================================================="
    echo ""
    echo -e "${BLUE}Usage:${NC}"
    echo "  Command line:"
    echo "    claude-main      # Launch main instance"
    echo "    claude-work      # Launch work instance"
    echo "    claude-personal  # Launch personal instance"
    echo ""
    echo "  Desktop:"
    echo "    Look for 'Claude Desktop (Main/Work/Personal)' in your application menu"
    echo ""
    echo -e "${BLUE}Features:${NC}"
    echo "  • Main: Full MCP suite (desktop-commander, context7, tess)"
    echo "  • Work: Enhanced with Playwright for browser automation"
    echo "  • Personal: Minimal setup (desktop-commander, context7 only)"
    echo ""
    echo -e "${BLUE}Configuration locations:${NC}"
    echo "  • Main: ~/.config/Claude-Main/"
    echo "  • Work: ~/.config/Claude-Work/"
    echo "  • Personal: ~/.config/Claude-Personal/"
    echo ""
    echo -e "${YELLOW}Note:${NC} You may need to restart your terminal or run:"
    echo "  source ~/.bashrc"
    echo ""
    print_status "To test the installation, try running: claude-main"
}

# Handle script arguments
case "${1:-}" in
    -h|--help)
        echo "Claude Desktop Multiple Instances Installer"
        echo ""
        echo "Usage: $0 [options]"
        echo ""
        echo "Options:"
        echo "  -h, --help    Show this help message"
        echo "  -y, --yes     Skip confirmation prompts"
        echo ""
        echo "This script will:"
        echo "  1. Create launcher scripts for 3 Claude Desktop instances"
        echo "  2. Configure separate MCP settings for each instance"
        echo "  3. Create desktop entries for easy launching"
        echo "  4. Update PATH to include launcher scripts"
        exit 0
        ;;
    -y|--yes)
        # Skip confirmations
        ;;
    *)
        # Interactive mode
        echo "This script will set up multiple Claude Desktop instances."
        echo "It will create launcher scripts, desktop entries, and MCP configurations."
        echo ""
        read -p "Continue with installation? (Y/n): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Nn]$ ]]; then
            print_status "Installation cancelled."
            exit 0
        fi
        ;;
esac

# Run main installation
main
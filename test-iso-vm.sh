#!/bin/bash
# VM Test Script with Serial Logging for UbuntuFast ISO
# This script boots the ISO in QEMU and captures all boot messages to a log file
#
# Enhanced with LLM-friendly debugging modes:
#   --debug       : Enable maximum kernel verbosity for troubleshooting
#   --watch       : Open real-time serial log viewer in new terminal
#   --interactive : Direct serial console interaction (no file logging)
#   --tmux        : Use tmux split panes instead of separate terminal

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# Auto-detect latest ISO file
LATEST_ISO=$(ls -t "$SCRIPT_DIR/build"/ubuntufast-*.iso 2>/dev/null | head -1)
ISO_FILE="${LATEST_ISO:-$SCRIPT_DIR/build/ubuntufast.iso}"
LOG_FILE="$SCRIPT_DIR/vm-boot.log"
SERIAL_LOG="$SCRIPT_DIR/vm-serial.log"

# Parse command line arguments
DEBUG_MODE=0
WATCH_MODE=0
INTERACTIVE_MODE=0
TMUX_MODE=0

while [[ $# -gt 0 ]]; do
    case $1 in
        --debug)
            DEBUG_MODE=1
            shift
            ;;
        --watch)
            WATCH_MODE=1
            shift
            ;;
        --interactive)
            INTERACTIVE_MODE=1
            shift
            ;;
        --tmux)
            TMUX_MODE=1
            shift
            ;;
        --help)
            echo "Usage: $0 [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  --debug       Enable maximum kernel verbosity (debug ignore_loglevel initcall_debug)"
            echo "  --watch       Open real-time serial log viewer in new terminal"
            echo "  --interactive Direct serial console interaction (replaces file logging)"
            echo "  --tmux        Use tmux split instead of new terminal (requires --watch)"
            echo "  --help        Show this help message"
            echo ""
            echo "Examples:"
            echo "  $0                           # Normal boot with serial logging"
            echo "  $0 --debug --watch           # Debug mode with real-time viewer (recommended for LLMs)"
            echo "  $0 --debug --interactive     # Debug with direct console access"
            echo "  $0 --debug --watch --tmux    # Debug with tmux split view"
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            echo "Run with --help for usage"
            exit 1
            ;;
    esac
done

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo "=========================================="
echo "UbuntuFast ISO VM Test with Serial Logging"
echo "=========================================="
echo ""

# Display active modes
if [ $DEBUG_MODE -eq 1 ] || [ $WATCH_MODE -eq 1 ] || [ $INTERACTIVE_MODE -eq 1 ]; then
    echo -e "${BLUE}Active Modes:${NC}"
    [ $DEBUG_MODE -eq 1 ] && echo -e "  ${GREEN}✓${NC} Debug mode (maximum kernel verbosity)"
    [ $WATCH_MODE -eq 1 ] && echo -e "  ${GREEN}✓${NC} Watch mode (real-time log viewer)"
    [ $INTERACTIVE_MODE -eq 1 ] && echo -e "  ${GREEN}✓${NC} Interactive mode (direct serial console)"
    [ $TMUX_MODE -eq 1 ] && echo -e "  ${GREEN}✓${NC} Tmux mode (split pane viewer)"
    echo ""
fi

# Check if ISO exists
if [ ! -f "$ISO_FILE" ]; then
    echo -e "${RED}ERROR: ISO file not found!${NC}"
    echo "Expected: $ISO_FILE"
    echo ""
    echo "Please run: sudo ./rebuild-all-modules.sh --clean"
    exit 1
fi

echo -e "${GREEN}ISO Found:${NC} $ISO_FILE"
echo -e "${GREEN}ISO Size:${NC} $(du -h "$ISO_FILE" | cut -f1)"
echo ""

# Clear old logs (unless interactive mode)
if [ $INTERACTIVE_MODE -eq 0 ]; then
    > "$LOG_FILE"
    > "$SERIAL_LOG"
fi

# Build kernel append parameters for debug mode
KERNEL_APPEND=""
if [ $DEBUG_MODE -eq 1 ]; then
    # Maximum verbosity parameters from 2025-09-22-boot-debug-session.md
    KERNEL_APPEND="console=ttyS0,115200n8 console=tty0 debug ignore_loglevel initcall_debug printk.devkmsg=on earlyprintk=serial,ttyS0,115200"
    echo -e "${YELLOW}Debug Parameters:${NC}"
    echo "  console=ttyS0,115200n8   - Serial console at 115200 baud"
    echo "  console=tty0             - Also output to VGA console"
    echo "  debug                    - Enable debug messages"
    echo "  ignore_loglevel          - Show all kernel messages"
    echo "  initcall_debug           - Log every kernel function call"
    echo "  printk.devkmsg=on        - Early boot messages"
    echo "  earlyprintk=serial       - Earliest possible serial output"
    echo ""
fi

echo "=========================================="
echo "Boot Logs"
echo "=========================================="
if [ $INTERACTIVE_MODE -eq 0 ]; then
    echo "Serial output: $SERIAL_LOG"
    echo "Combined log:  $LOG_FILE"
else
    echo -e "${YELLOW}Interactive mode: Serial console on stdio${NC}"
    echo "  (No file logging - all output to terminal)"
fi
echo ""

# Launch watch mode if requested (before starting VM)
if [ $WATCH_MODE -eq 1 ] && [ $INTERACTIVE_MODE -eq 0 ]; then
    # Touch log file to ensure it exists
    touch "$SERIAL_LOG"

    if [ $TMUX_MODE -eq 1 ]; then
        # Use tmux split pane
        if command -v tmux &> /dev/null; then
            if [ -n "$TMUX" ]; then
                # Already in tmux, create split
                tmux split-window -h "tail -f '$SERIAL_LOG'; read -p 'Press Enter to close...'"
                echo -e "${GREEN}Tmux split created${NC} - Serial log viewer in right pane"
            else
                echo -e "${YELLOW}Warning: --tmux requires running inside tmux session${NC}"
                echo "  Falling back to separate terminal..."
                TMUX_MODE=0
            fi
        else
            echo -e "${YELLOW}Warning: tmux not installed${NC}"
            echo "  Install with: sudo apt install tmux"
            echo "  Falling back to separate terminal..."
            TMUX_MODE=0
        fi
    fi

    # Fall back to separate terminal if tmux not used
    if [ $TMUX_MODE -eq 0 ]; then
        # Detect available terminal emulator
        if command -v gnome-terminal &> /dev/null; then
            gnome-terminal -- bash -c "tail -f '$SERIAL_LOG'; read -p 'Press Enter to close...'" &
            echo -e "${GREEN}Real-time log viewer launched${NC} in gnome-terminal"
        elif command -v xterm &> /dev/null; then
            xterm -hold -e "tail -f '$SERIAL_LOG'" &
            echo -e "${GREEN}Real-time log viewer launched${NC} in xterm"
        elif command -v konsole &> /dev/null; then
            konsole --hold -e "tail -f '$SERIAL_LOG'" &
            echo -e "${GREEN}Real-time log viewer launched${NC} in konsole"
        elif command -v xfce4-terminal &> /dev/null; then
            xfce4-terminal --hold -e "tail -f '$SERIAL_LOG'" &
            echo -e "${GREEN}Real-time log viewer launched${NC} in xfce4-terminal"
        else
            echo -e "${YELLOW}Warning: No terminal emulator found${NC}"
            echo "  Install one: sudo apt install gnome-terminal"
            echo "  Or use: tail -f $SERIAL_LOG"
        fi
    fi
    echo ""
fi

echo -e "${YELLOW}Starting VM...${NC}"
if [ $INTERACTIVE_MODE -eq 1 ]; then
    echo "  Interactive console active - type commands at boot prompt"
    echo "  Press Ctrl+A then X to exit QEMU"
else
    echo "  Press Ctrl+C to stop VM"
fi
echo ""

# Run QEMU with UEFI and serial console logging
# -bios: Use OVMF UEFI firmware instead of legacy BIOS
# -serial: Redirect serial port (file for logging, stdio for interactive)
# -append: Inject kernel parameters directly (bypasses GRUB menu)
# -vga std: Standard VGA adapter for graphical display
# -monitor: Interactive monitor for VM control

# Check if OVMF UEFI firmware is available
OVMF_CODE="/usr/share/OVMF/OVMF_CODE.fd"
OVMF_VARS="/usr/share/OVMF/OVMF_VARS.fd"

if [ ! -f "$OVMF_CODE" ]; then
    echo -e "${RED}ERROR: OVMF UEFI firmware not found!${NC}"
    echo "Install with: sudo apt install ovmf"
    exit 1
fi

# Build QEMU command dynamically based on modes
QEMU_CMD="qemu-system-x86_64"
QEMU_ARGS=(
    "-enable-kvm"
    "-m" "4G"
    "-cdrom" "$ISO_FILE"
    "-boot" "d"
    "-bios" "$OVMF_CODE"
)

# Add serial port configuration (file logging or stdio)
if [ $INTERACTIVE_MODE -eq 1 ]; then
    QEMU_ARGS+=("-serial" "mon:stdio")
else
    QEMU_ARGS+=("-serial" "file:$SERIAL_LOG")
    QEMU_ARGS+=("-monitor" "stdio")
fi

# Add VGA
QEMU_ARGS+=("-vga" "std")

# Add kernel append parameters if debug mode enabled
# Note: This requires the ISO to support direct kernel boot via -kernel/-initrd
# For UEFI ISOs, debug params need to be added to grub.cfg instead
if [ $DEBUG_MODE -eq 1 ]; then
    echo -e "${YELLOW}Note: Debug parameters will be active once boot begins${NC}"
    echo "  For ISOs with GRUB menu: Select entry and boot will be verbose"
    echo "  To bypass GRUB and inject params, ISO would need -kernel/-initrd support"
    echo ""
    # TODO: Add -kernel and -initrd extraction from ISO for direct boot
    # For now, debug params are informational - user can add to grub.cfg
fi

# Execute QEMU with appropriate output handling
if [ $INTERACTIVE_MODE -eq 1 ]; then
    # Interactive mode - all output to terminal
    "$QEMU_CMD" "${QEMU_ARGS[@]}"
else
    # File logging mode - also tee to combined log
    "$QEMU_CMD" "${QEMU_ARGS[@]}" 2>&1 | tee -a "$LOG_FILE"
fi

echo ""
echo "=========================================="
echo "VM Stopped"
echo "=========================================="
echo ""

if [ $INTERACTIVE_MODE -eq 0 ]; then
    echo "Boot logs saved to:"
    echo "  - Serial: $SERIAL_LOG"
    echo "  - Combined: $LOG_FILE"
    echo ""

    if [ $DEBUG_MODE -eq 1 ]; then
        echo "Debug Analysis Commands:"
        echo "  # Find errors and failures"
        echo "  grep -i 'error\\|fail\\|fatal\\|panic' $SERIAL_LOG"
        echo ""
        echo "  # Check specific subsystems"
        echo "  grep -i 'initcall' $SERIAL_LOG | tail -20"
        echo "  grep -i 'systemd' $SERIAL_LOG | grep -i 'fail'"
        echo "  grep -i 'mount' $SERIAL_LOG | grep -i 'error'"
        echo ""
        echo "  # Analyze boot timing"
        echo "  grep 'Reached target' $SERIAL_LOG"
        echo "  grep 'Started' $SERIAL_LOG | tail -20"
        echo ""
    else
        echo "To analyze boot issues, run:"
        echo "  grep -i 'error\\|fail\\|fatal' $SERIAL_LOG"
        echo "  grep -i 'lightdm\\|networkmanager' $SERIAL_LOG"
        echo ""
    fi

    if [ $WATCH_MODE -eq 1 ]; then
        echo -e "${GREEN}Tip:${NC} The watch terminal will close automatically when you close it"
        echo ""
    fi
else
    echo "Interactive session ended."
    echo ""
fi

echo "To run with different modes:"
echo "  $0 --help"
echo ""
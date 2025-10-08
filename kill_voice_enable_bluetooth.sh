#!/bin/bash

echo "Killing voice-typer processes..."
# Kill any voice-related processes
pkill -f voice-typer
pkill -f voice_typer

# Show any remaining voice processes
VOICE_PROCS=$(ps aux | grep -i voice | grep -v grep)
if [ ! -z "$VOICE_PROCS" ]; then
    echo "Found remaining voice processes:"
    echo "$VOICE_PROCS"
    # Kill them by PID
    ps aux | grep -i voice | grep -v grep | awk '{print $2}' | xargs -r kill
fi

echo "Enabling bluetooth..."
# Unblock bluetooth
sudo rfkill unblock bluetooth

# Reload bluetooth USB module
sudo modprobe -r btusb
sudo modprobe btusb

# Restart bluetooth service
sudo systemctl restart bluetooth

# Wait a moment for service to start
sleep 2

# Power on bluetooth
bluetoothctl power on

echo "Done! Bluetooth should now be enabled."
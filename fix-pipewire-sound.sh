#!/bin/bash
# Fix PipeWire sound when no output devices show in GUI
# Run this script if sound suddenly stops working on ZorinOS/Ubuntu

echo "Fixing PipeWire sound issue..."

# Remove system-wide masks that prevent PipeWire from starting
sudo rm -f /etc/xdg/systemd/user/pipewire.service /etc/xdg/systemd/user/pipewire.socket

# Reload systemd, enable and start PipeWire services
systemctl --user daemon-reload
systemctl --user enable pipewire.service pipewire.socket
systemctl --user start pipewire.service
systemctl --user restart pipewire-pulse.service

echo "PipeWire services restarted. Check your sound settings - output devices should now be available."
echo "To test: speaker-test -t sine -f 1000 -l 1"
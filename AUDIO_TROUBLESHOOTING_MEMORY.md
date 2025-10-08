# Audio Troubleshooting Memory Bank

## PipeWire "No Output Devices" Fix (June 2025)

### Problem
- Sound suddenly stopped working on ZorinOS (Ubuntu-based)
- Sound GUI showed no output devices in dropdown
- System was using PipeWire

### Root Cause
- `pipewire.service` was masked (linked to `/dev/null`)
- `pipewire.socket` was also masked
- Only `pipewire-pulse` was running, but main PipeWire service couldn't start

### Solution Script
Location: `/home/user1/fix-pipewire-sound.sh`

**Single command fix:**
```bash
sudo rm -f /etc/xdg/systemd/user/pipewire.service /etc/xdg/systemd/user/pipewire.socket && systemctl --user daemon-reload && systemctl --user enable pipewire.service pipewire.socket && systemctl --user start pipewire.service && systemctl --user restart pipewire-pulse.service
```

### Diagnostic Commands
- Check what's running: `ps aux | grep -E "(pulse|pipewire)" | grep -v grep`
- Check service status: `systemctl --user status pipewire pipewire-pulse`
- List audio devices: `pactl list short sinks`
- Test audio: `speaker-test -t sine -f 1000 -l 1`

### Key Insight
When PipeWire services are masked at the system level (`/etc/xdg/systemd/user/`), user-level commands won't work. Must remove the masks first with sudo, then restart services at user level.

### Success Indicators
- `pactl list short sinks` shows multiple audio devices
- Sound GUI dropdown shows available output devices
- `systemctl --user status pipewire` shows "active (running)"
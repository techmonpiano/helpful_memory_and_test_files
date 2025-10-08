# Goose Desktop Installation & Troubleshooting Session

## Date: June 27, 2025

## Problem Summary
- Installed Goose desktop .deb package from https://block.github.io/goose/docs/getting-started/installation
- Desktop app wouldn't launch - "Goosed server failed to start" error
- Root cause: GLIBC version mismatch (system had 2.35, app required 2.38/2.39)

## System Info
- OS: Ubuntu-based (Zorin OS)
- GLIBC Version: 2.35
- Display: Wayland with Xwayland support
- Docker: Available and working

## Initial Attempts
1. **CLI Installation**: Successfully installed Goose CLI v1.0.29
2. **Desktop Installation**: .deb package installed but GUI wouldn't launch
3. **Error Analysis**: 
   - Tray icon appeared but no main window
   - Internal "goosed" server failed to start on various ports
   - Running `/usr/lib/goose/resources/bin/goosed` revealed GLIBC dependency issue

## Solution: Distrobox Container Approach

### Step 1: Install Distrobox
```bash
curl -s https://raw.githubusercontent.com/89luca89/distrobox/main/install | sh -s -- --prefix ~/.local
```

### Step 2: Configure Docker Backend
```bash
echo 'export DBX_CONTAINER_MANAGER="docker"' >> ~/.bashrc
source ~/.bashrc
```

### Step 3: Create Ubuntu 24.04 Container
```bash
~/.local/bin/distrobox create --name goose-ubuntu --image ubuntu:24.04
```
- Ubuntu 24.04 has GLIBC 2.39 (compatible with Goose requirements)

### Step 4: Wayland Display Setup
```bash
xhost +local:docker
```

### Step 5: Working Launch Command
```bash
~/.local/bin/distrobox enter goose-ubuntu -- env WAYLAND_DISPLAY=$WAYLAND_DISPLAY XDG_RUNTIME_DIR=$XDG_RUNTIME_DIR DISPLAY=$DISPLAY goose --enable-features=UseOzonePlatform --ozone-platform=wayland --no-sandbox
```

## Configuration Details

### API Key Configuration
- Provider: OpenRouter
- API Key: `OPENROUTER_API_KEY=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`
- Model: `openai/gpt-4.1-mini`
- Config File: `/home/user1/.config/goose/config.yaml`

### Updated Desktop Entry
Created `/tmp/goose-distrobox.desktop`:
```ini
[Desktop Entry]
Name=Goose
Comment=Goose AI Agent - Running in Distrobox
GenericName=Goose
Exec=/home/user1/.local/bin/distrobox enter goose-ubuntu -- env WAYLAND_DISPLAY=$WAYLAND_DISPLAY XDG_RUNTIME_DIR=$XDG_RUNTIME_DIR DISPLAY=$DISPLAY goose --enable-features=UseOzonePlatform --ozone-platform=wayland --no-sandbox %U
Icon=goose
Type=Application
StartupNotify=true
Categories=GNOME;GTK;Utility;
```

### Backup Files
- Original desktop file backed up as: `/usr/share/applications/goose.desktop.backup`

## Alternative: Web Interface
Goose also provides a web interface via CLI:
```bash
goose web --port 3060 --open
```
- Requires CLI installation and proper API key configuration
- Documentation: https://block.github.io/goose/docs/guides/goose-cli-commands/

## Key Learnings
1. **GLIBC compatibility** is critical for modern applications
2. **Distrobox** is excellent for running apps requiring newer system libraries
3. **Wayland support** requires specific flags: `--enable-features=UseOzonePlatform --ozone-platform=wayland`
4. **Docker backend** needs explicit configuration: `DBX_CONTAINER_MANAGER="docker"`
5. **Container GUI apps** need proper display forwarding and X11/Wayland permissions

## Files Modified
- `/home/user1/.bashrc` - Added OPENROUTER_API_KEY and DBX_CONTAINER_MANAGER
- `/home/user1/.config/goose/config.yaml` - Goose configuration
- `/usr/share/applications/goose.desktop` - Updated desktop entry (backup available)

## Container Details
- Container Name: `goose-ubuntu`
- Base Image: `ubuntu:24.04`
- GLIBC Version: 2.39-0ubuntu8.4
- Status: Running and functional

## Success Criteria Met
✅ Goose desktop GUI launches successfully  
✅ No GLIBC errors  
✅ Wayland compatibility working  
✅ OpenRouter API integration functional  
✅ Desktop menu integration available  
✅ GPT-4.1-mini model configured  

## Future Reference
- To update Goose: Update inside the distrobox container
- To modify config: Use CLI commands or edit config files directly
- To troubleshoot: Check container status and display environment variables
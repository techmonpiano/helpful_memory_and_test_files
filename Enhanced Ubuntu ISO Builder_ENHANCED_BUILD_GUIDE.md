# Enhanced Ubuntu ISO Builder - Quick Guide

## New Features

### 1. **Persistent Package Caching**
- Downloads are cached in `~/.cache/ustandard-build/`
- Debootstrap packages cached separately
- APT packages cached for reuse
- Saves ~1.1GB bandwidth on rebuilds

### 2. **Build Stage Tracking**
The build is divided into 4 stages:
- **Stage 1**: Debootstrap base system (~200MB)
- **Stage 2**: Install system packages (~800MB)
- **Stage 3**: Install desktop environment (~300MB)
- **Stage 4**: Create ISO image

Each completed stage is tracked, allowing resume on failure.

### 3. **Resume Capability**
If a build fails, you can resume from the last successful stage without re-downloading everything.

## Usage Examples

### First Build
```bash
./build_custom_enhanced.sh
```

### Build Failed? Resume It
```bash
./build_custom_enhanced.sh --resume
```

### Rebuild Keeping Downloads
```bash
./build_custom_enhanced.sh --keep-cache
```

### Clean Everything and Start Fresh
```bash
./build_custom_enhanced.sh --clean-cache
```

### View Help
```bash
./build_custom_enhanced.sh --help
```

## Cache Management

### Check Cache Size
```bash
du -sh ~/.cache/ustandard-build/
```

### Manual Cache Cleanup
```bash
rm -rf ~/.cache/ustandard-build/
```

## Build Scenarios

### Scenario 1: Build Failed During Desktop Install
```bash
# Resume from where it failed
./build_custom_enhanced.sh --resume --keep-cache
```

### Scenario 2: Want to Try Different Desktop
```bash
# Edit custom_config.sh to change DESKTOP_ENV
nano custom_config.sh
# Rebuild reusing base packages
./build_custom_enhanced.sh --keep-cache
```

### Scenario 3: Monthly Rebuild with Updates
```bash
# Clean cache to get latest packages
./build_custom_enhanced.sh --clean-cache
```

## Performance Comparison

| Build Type | Time | Bandwidth |
|------------|------|-----------|
| First build | 30-60 min | ~1.1GB |
| Cached rebuild | 10-20 min | ~50MB |
| Resume from Stage 2 | 15-25 min | ~300MB |

## Troubleshooting

### "No space left on device"
- Check cache size: `du -sh ~/.cache/ustandard-build/`
- Clean cache: `./build_custom_enhanced.sh --clean-cache`
- Or manually: `rm -rf ~/.cache/ustandard-build/apt/*.deb`

### Build Still Fails at Same Point
- Try without resume: `./build_custom_enhanced.sh` (no --resume)
- Check error messages for missing packages
- Ensure you have the Ubuntu 25.04 fixes applied

### Want to Start Completely Fresh
```bash
./build_custom_enhanced.sh --clean-cache
rm -rf ~/uStandard/ustandardbuild/
```

## Technical Details

- Cache location: `~/.cache/ustandard-build/`
- Stage markers: `~/.cache/ustandard-build/stages/.stage*_complete`
- Debootstrap cache: Reuses base system downloads
- APT cache: Preserves .deb files between builds
- No modification to original uStandard.sh needed
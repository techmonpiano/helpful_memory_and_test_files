# Systemd to Non-Systemd Init Conversion Tools Guide

## Overview
This guide documents available tools and methods for automatically converting systemd service files to other init systems (OpenRC, SysVInit) on Ubuntu/Debian systems without systemd.

## Available Conversion Tools

### 1. initify - Systemd to OpenRC Converter
- **GitHub**: https://github.com/goose121/initify
- **Alternative Fork**: https://github.com/artixnous/initify
- **Purpose**: Converts simple systemd services to OpenRC init-scripts
- **Usage**: Can be piped from stdin or used with files
- **Note**: Service name will initially be "(fill in)" when piping from stdin

### 2. systemd-to-sysvinit-converter
- **GitHub**: https://github.com/akhilvij/systemd-to-sysvinit-converter
- **Origin**: Debian project from Google Summer of Code 2012
- **Language**: Python
- **Usage**: `python converter.py /location/of/systemd/conf_file`
- **Features**:
  - Produces basic and clean init scripts
  - Warns about systemd options without SysV equivalents
  - Reduces code duplication

### 3. openrc.run - Web-based Converter
- **Website**: http://openrc.run/
- **Purpose**: Online service for converting systemd units to OpenRC
- **Usage**: Paste systemd service unit and get OpenRC script

### 4. systemd-unit-converter (WIP)
- **GitHub**: https://github.com/ShadowKyogre/systemd-unit-converter
- **Status**: Work in progress, not fully functional
- **Goal**: Convert systemd units to various init systems

## Systemd's Built-in Compatibility

### systemd-sysv-generator
- Systemd includes backward compatibility for SysV init scripts
- Automatically converts init scripts on the fly
- Runs at boot and when systemd reloads configuration
- Creates service units from /etc/init.d scripts if no native unit exists

## Semi-Automatic Conversion Solution

### Custom dpkg Hook Approach
Create a post-install hook that automatically converts new systemd services:

```bash
#!/bin/bash
# /etc/dpkg/dpkg.cfg.d/systemd-converter

# Create the hook configuration
cat > /etc/dpkg/dpkg.cfg.d/50-systemd-converter << 'EOF'
DPkg::Post-Invoke {
    "find /lib/systemd/system -name '*.service' -newer /var/lib/dpkg/status | while read service; do
        # Convert using initify for OpenRC
        if command -v initify >/dev/null 2>&1; then
            initify $service > /etc/init.d/$(basename $service .service)
            chmod +x /etc/init.d/$(basename $service .service)
            update-rc.d $(basename $service .service) defaults
        fi
        # Alternative: Use systemd-to-sysvinit-converter
        # python /path/to/converter.py $service
    done"
};
EOF
```

### Implementation Steps:
1. Install conversion tool (initify or systemd-to-sysvinit-converter)
2. Create dpkg hook file
3. New packages will have their systemd services auto-converted
4. Converted scripts placed in /etc/init.d/
5. Services enabled with update-rc.d

## Systemd-Free Distribution Alternatives

### Devuan
- **Website**: https://www.devuan.org
- **Description**: Debian fork without systemd
- **Init Systems**: sysvinit (default), openrc, runit
- **Benefit**: Maintains Debian package compatibility
- **Philosophy**: "Init Freedom" - restoring choice in PID1

### MX Linux
- **Base**: Debian stable
- **Init**: Systemd included but optional
- **Control**: User can enable/disable systemd as needed

### Other Options
- Void Linux (runit, xbps)
- AntiX (sysvinit)
- Artix Linux (OpenRC, runit, or s6)

## Manual Service Management Without Systemd

### Traditional SysV Commands:
```bash
# Enable service
update-rc.d servicename defaults

# Disable service
update-rc.d -f servicename remove

# Start/stop service
service servicename start|stop|restart

# GUI tool for service management
sudo apt install rcconf
rcconf  # Text-based UI for managing services
```

### Converting Services Manually:
1. Read systemd service file from `/lib/systemd/system/`
2. Extract key information:
   - ExecStart (main command)
   - ExecStop (stop command)
   - Environment variables
   - Dependencies
3. Create init script in `/etc/init.d/`
4. Make executable: `chmod +x /etc/init.d/servicename`
5. Enable: `update-rc.d servicename defaults`

## Limitations and Considerations

1. **No Perfect Solution**: No fully automatic, seamless converter exists that intercepts all package installations
2. **Complex Services**: Some systemd features don't translate directly:
   - Socket activation
   - Complex dependencies
   - Resource limits
   - Namespace isolation
3. **Manual Tweaking**: Converted scripts often need manual adjustments
4. **Maintenance**: Need to re-convert after package updates

## Best Practices

1. **Test Converted Services**: Always test after conversion
2. **Keep Original**: Save systemd service files for reference
3. **Document Changes**: Track which services were converted
4. **Monitor Logs**: Check syslog for service startup issues
5. **Consider Devuan**: For production systems, consider using Devuan instead

## Resources

- Devuan Init Freedom: https://www.devuan.org/os/init-freedom
- nosystemd.org: https://nosystemd.org/
- Without Systemd Wiki: https://www.without-systemd.org/wiki/index.php/Main_Page/
- Artix Linux Forums: https://forum.artixlinux.org/

## Summary

While there's no perfect drop-in solution for automatic systemd-to-init conversion during package installation, the combination of conversion tools and dpkg hooks can provide a semi-automatic workflow. For users seeking a completely systemd-free experience with minimal manual intervention, switching to Devuan or similar distributions may be the most practical solution.
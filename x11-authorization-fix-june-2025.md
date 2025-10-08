# X11 Authorization Error Fix - June 2025

## Issue Description
On June 28, 2025, the Python text expander started failing with X11 authorization errors:
```
ImportError: this platform is not supported: ('failed to acquire X connection: Can\'t connect to display ":0": b\'Authorization required, but no authorization protocol specified\\n\'', DisplayConnectionError(':0', b'Authorization required, but no authorization protocol specified\n'))
```

## Root Cause
Critical X11 security updates were installed on **June 21, 2025** that patched 7 CVEs and tightened X11 authentication mechanisms.

### Security Updates Applied
- `xserver-xorg-core`: 2:21.1.4-2ubuntu1.7~22.04.14 → 2:21.1.4-2ubuntu1.7~22.04.15
- `xserver-xorg-legacy`: 2:21.1.4-2ubuntu1.7~22.04.14 → 2:21.1.4-2ubuntu1.7~22.04.15
- `xserver-common`: 2:21.1.4-2ubuntu1.7~22.04.14 → 2:21.1.4-2ubuntu1.7~22.04.15
- `xwayland`: 2:22.1.1-1ubuntu0.18 → 2:22.1.1-1ubuntu0.19

### CVEs Patched
- **CVE-2025-49175**: Out-of-bounds access in X Rendering extension
- **CVE-2025-49176**: Integer overflow in Big Requests Extension
- **CVE-2025-49177**: Data leak in XFIXES Extension 6
- **CVE-2025-49178**: Unprocessed client request vulnerability
- **CVE-2025-49179**: Integer overflow in X Record extension
- **CVE-2025-49180**: Integer overflow in RandR extension
- **CVE-2025-26594**: Use-after-free of the root cursor

## Solution Applied

### Immediate Fix
```bash
xhost +local:
```
This allows local connections to the X server without network access.

### Permanent Fix
Added to `~/.bashrc`:
```bash
# Allow local X11 connections for pynput (text expander)
if [ -n "$DISPLAY" ]; then
    xhost +local: 2>/dev/null
fi
```

## Why This Happened
The security updates made X11 more restrictive about which processes can connect without proper authentication. While this improves security, it broke applications like pynput that need X11 access for keyboard/mouse control.

## Additional Context
- System is running Wayland with XWayland for X11 compatibility
- PAM modules and Python 3.10 were also updated on the same day
- The fix maintains reasonable security by only allowing local apps, not network connections

## Future Considerations
After major system security updates, especially those affecting X11/Wayland, test GUI applications that rely on display access to catch authentication issues early.
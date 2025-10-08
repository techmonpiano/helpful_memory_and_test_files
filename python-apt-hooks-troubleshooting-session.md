# Python/APT Hooks Troubleshooting Session - July 7, 2025

## Problem Summary
System experiencing multiple Python-related errors after Python 3.11 installation:
- `apt update` failing with `ModuleNotFoundError: No module named 'apt_pkg'`
- `gnome-terminal` failing with gi module circular import error

## Root Cause Analysis
The core issue was that `/usr/bin/python3` symlink was changed from Python 3.10 to Python 3.11 on July 3rd, 2025. Ubuntu 22.04 system packages were compiled for Python 3.10, causing compatibility issues.

## What Are APT Hooks?
APT hooks are scripts that run automatically during package management operations. They're defined in `/etc/apt/apt.conf.d/` files and execute at predefined stages:
- Pre-Invoke: Before main apt command
- Post-Invoke: After completion
- Post-Invoke-Success: Only after successful completion

The failing hook was:
```
APT::Update::Post-Invoke-Success 'if /usr/bin/test -w /var/lib/command-not-found/ -a -e /usr/lib/cnf-update-db; then /usr/lib/cnf-update-db > /dev/null; fi'
```

This is a **default Ubuntu hook** (not custom) from the `command-not-found` package that updates the database for command suggestions.

## Solution Applied
1. **Identified the problem**: Python 3.11 was set as default instead of Python 3.10
2. **Restored original symlink**: 
   ```bash
   sudo ln -sf python3.10 /usr/bin/python3
   ```
3. **Cleaned up temporary workaround**: Removed the apt_pkg.so symlink that was no longer needed

## System State After Fix
- `python3` → Python 3.10 (system default)
- `python3.11` → Python 3.11 (available for specific use)
- System packages (apt, gnome-terminal) working correctly

## Python Virtual Environment Best Practices
Added alias to .bashrc for convenience:
```bash
alias activate='source venv/bin/activate'
```

### Standard Virtual Environment Workflow
- **One venv per project/repo** is standard practice
- Provides dependency isolation and clean environments
- Structure: `project/venv/` (add to .gitignore)
- Commands: `python3 -m venv venv`, `source venv/bin/activate`, `deactivate`

### Disk Space Considerations
- Virtual environments do use more disk space due to duplicated packages
- Typical overhead: 50-200MB per venv for common packages
- Trade-off is usually worth it for reliability and clean dependency management
- Modern tools (pipenv, poetry, conda) offer better caching strategies

## Key Lessons
1. **Don't change system Python symlinks** - Use virtual environments instead
2. **APT hooks are part of Ubuntu's package management system** - They serve important functions
3. **System packages are compiled for specific Python versions** - Mixing versions breaks compatibility
4. **Virtual environments are the proper way to manage different Python versions** for development

## Files Modified
- `/home/user1/.bashrc` - Added `activate` alias for virtual environments
- `/usr/bin/python3` - Restored symlink to point to python3.10
- Removed temporary `/usr/lib/python3/dist-packages/apt_pkg.so` symlink

## Prevention
- Use `python3.11 script.py` for Python 3.11 projects
- Create virtual environments: `python3.11 -m venv myproject_env`
- Keep system Python unchanged for stability
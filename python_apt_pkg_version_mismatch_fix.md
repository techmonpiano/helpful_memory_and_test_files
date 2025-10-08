# Python apt_pkg Version Mismatch Fix

## Problem Description
When system Python version (e.g., 3.11) differs from the version that `python3-apt` was compiled for (e.g., 3.10), you get:

```
ModuleNotFoundError: No module named 'apt_pkg'
```

This breaks APT package management scripts and system tools.

## Root Cause
- System Python points to `/usr/bin/python3.11`
- But `apt_pkg.cpython-310-x86_64-linux-gnu.so` was compiled for Python 3.10
- The compiled module is version-specific and can't be imported by different Python versions

## Diagnosis Commands
```bash
# Check Python version
python3 --version

# Check what python3 symlink points to
ls -la /usr/bin/python3

# Test apt_pkg import
python3 -c "import apt_pkg; print('Working')" 2>&1 || echo "Broken"

# Test with specific Python versions
python3.10 -c "import apt_pkg; print('Python 3.10 works')"
python3.11 -c "import apt_pkg; print('Python 3.11 works')"

# Check compiled module versions
ls -la /usr/lib/python3/dist-packages/apt_pkg*
```

## Solution: Temporary Python Version Switch

### Method 1: Temporary Symlink Switch
```bash
# 1. Temporarily point python3 to python3.10
sudo ln -sf /usr/bin/python3.10 /usr/bin/python3

# 2. Configure broken packages
sudo dpkg --configure -a

# 3. Restore python3 to original version
sudo ln -sf /usr/bin/python3.11 /usr/bin/python3
```

### Method 2: Force Reinstall (Preferred)
```bash
# This should rebuild apt_pkg for current Python version
sudo apt install --reinstall python3-apt
```

## Verification
```bash
# Test that apt_pkg works with current Python
python3 -c "import apt_pkg; print('✅ apt_pkg working!')"

# Test APT update works without errors
sudo apt update

# Test that system scripts work
sudo dpkg --configure -a
```

## When This Happens
- After installing different Python versions (e.g., from deadsnakes PPA)
- When system Python gets updated but apt packages don't get rebuilt
- After running problematic setup.py scripts that mess with system Python

## Prevention
- Avoid running setup.py scripts that modify system Python packages
- Use virtual environments for application-specific Python packages
- Be careful when installing alternative Python versions

## Related Issues Fixed
This fix resolves:
- `E: Problem executing scripts APT::Update::Post-Invoke-Success`
- Update notifier configuration failures
- Command-not-found database update errors
- System package manager breakage

---
*Created: 2025-08-01*
*Context: Fixed after handy-expander setup.py broke system apt_pkg*
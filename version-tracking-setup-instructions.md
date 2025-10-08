# Version Tracking and Setup.py Instructions

## Critical Version Update Requirements

**NEVER FORGET**: After ANY code changes/fixes/enhancements, you MUST update version numbers in ALL relevant files.

### Files to Update
1. **Primary version file** (`version.py`, `__init__.py`, or main app file)
2. **setup.py** (VERSION or fallback version)
3. **pyproject.toml** (if present)
4. **Package metadata files** (if applicable)

**ALWAYS check project-specific CLAUDE.md for exact file locations and update procedures.**

## Semantic Versioning
Use semantic versioning: increment PATCH for bug fixes, MINOR for features, MAJOR for breaking changes.

## Setup.py Installer Updates (MANDATORY)

### Key Requirements
- **ALWAYS** check if project has setup.py after making changes/fixes/enhancements
- **MUST** update setup.py to handle new files, dependencies, or features
- **MUST** ensure setup.py includes all new components for fresh installs
- **MUST** verify setup.py can update existing installs with new logic
- Follow installer best practices: cross-platform paths, version tracking, rollback capability

## Version Management Protocol (MANDATORY)

### Update Checklist
- **MUST** increment version number for ANY changes/fixes/enhancements
- **MUST** check project-specific CLAUDE.md for exact files to update
- **MUST** update version in ALL project-specific locations consistently:
  - Primary version file (version.py, __init__.py, or main app file)
  - setup.py version parameter or fallback version
  - Desktop entry files (.desktop Version field, if applicable)
  - Package metadata (pyproject.toml, requirements.txt, etc.)
  - Application manifests (Info.plist, package.json, etc.)
- **MUST** test installation after version updates: `python setup.py --user` or equivalent
- **MUST** display version in GUI title bars: "AppName v1.2.3"
- **MUST** display version in console output on app startup
- **MUST** use semantic versioning (MAJOR.MINOR.PATCH)
- **MUST** include version number in commit messages

## Auto-Update Implementation for Python Apps

### Requirements
- **MUST** implement auto-update check on app startup for production apps
- **MUST** compare app version with installed version and auto-upgrade if outdated
- **MUST** run `python setup.py install --user` automatically when update needed
- **MUST** continue to main app after successful update, exit gracefully on failure

### Auto-update Pattern for Main App Entry Point

```python
import subprocess
import sys
import os
from pathlib import Path

def check_and_update():
    """Check if app needs update and auto-install if needed"""
    try:
        # Define current app version (update this with each release)
        APP_VERSION = "1.2.0"
        
        # Check installed version (from setup.py or version file)
        installed_version = get_installed_version()  # Implement based on your versioning
        
        if version_is_older(installed_version, APP_VERSION):
            print(f"Updating from {installed_version} to {APP_VERSION}...")
            
            # Run setup.py install --user automatically
            setup_path = Path(__file__).parent / "setup.py"
            if setup_path.exists():
                result = subprocess.run([
                    sys.executable, str(setup_path), "install", "--user"
                ], capture_output=True, text=True)
                
                if result.returncode == 0:
                    print("Update completed successfully")
                    return True
                else:
                    print(f"Update failed: {result.stderr}")
                    return False
        return True
    except Exception as e:
        print(f"Update check failed: {e}")
        return True  # Continue with app launch

# In main app startup
if __name__ == "__main__":
    if check_and_update():
        # Launch main application
        main()
    else:
        sys.exit(1)
```

## Summary

Remember: Version tracking is CRITICAL and MANDATORY for every code change. This ensures users always have the latest fixes and features, and enables proper auto-update functionality.
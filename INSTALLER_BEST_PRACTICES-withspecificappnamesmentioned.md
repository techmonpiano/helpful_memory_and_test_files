# Python App Installer Best Practices Guide

## Executive Summary

This consolidated guide combines insights from the installer enhancement plan and summary to provide authoritative best practices for Python application installers. Based on analysis of handy-terminal (gold standard), kilo-terminal, and FriendlyReminders installers.

## Core Principles

### 1. **Cross-Platform Python Implementation**
- Use Python as the primary installer language (not bash/shell)
- Implement platform-specific features through Python conditionals
- Provide shell script wrappers for user convenience
- Support Linux, macOS, and Windows natively

### 2. **Modular Architecture**
- Separate concerns into focused functions
- Clear separation between installation logic and UI
- Reusable components across different installation types
- Maintainable and testable code structure

### 3. **Professional Installation Lifecycle**
- Support both user-level and system-wide installations
- Implement proper version tracking and update detection
- Provide complete uninstaller with configuration options
- Include rollback mechanisms for failed installations

## Implementation Standards

### Command-Line Interface
```python
parser.add_argument('--user', action='store_true', 
                   help='Install for current user only (no sudo required)')
parser.add_argument('--uninstall', action='store_true',
                   help='Uninstall the application')
parser.add_argument('--help-install', action='store_true',
                   help='Show detailed installation help')
parser.add_argument('--force', action='store_true',
                   help='Force reinstallation')
parser.add_argument('--verbose', action='store_true',
                   help='Enable verbose output')
parser.add_argument('--dry-run', action='store_true',
                   help='Show what would be done without executing')
parser.add_argument('--version', action='version', version=f'{APP_NAME} v{VERSION}')
```

### Platform-Specific Paths
```python
def get_install_paths(user_install=False):
    """Get platform-specific installation paths"""
    system = platform.system()
    
    if system == "Linux":
        if user_install:
            return {
                'app_dir': os.path.join(home, f'.local/share/{EXECUTABLE_NAME}'),
                'bin_dir': os.path.join(home, '.local/bin'),
                'desktop_dir': os.path.join(home, '.local/share/applications'),
                'icon_dir': os.path.join(home, '.local/share/icons/hicolor'),
                'config_dir': os.path.join(home, f'.config/{EXECUTABLE_NAME}'),
                'autostart_dir': os.path.join(home, '.config/autostart')
            }
        else:
            return {
                'app_dir': f'/opt/{EXECUTABLE_NAME}',
                'bin_dir': '/usr/local/bin',
                'desktop_dir': '/usr/share/applications',
                'icon_dir': '/usr/share/icons/hicolor',
                'config_dir': os.path.expanduser(f'~/.config/{EXECUTABLE_NAME}'),
                'autostart_dir': os.path.expanduser('~/.config/autostart')
            }
    elif system == "Darwin":  # macOS
        return {
            'app_dir': f'/Applications/{APP_NAME}.app/Contents/MacOS',
            'bin_dir': '/usr/local/bin',
            'desktop_dir': '/Applications',
            'icon_dir': f'/Applications/{APP_NAME}.app/Contents/Resources',
            'config_dir': os.path.expanduser(f'~/Library/Application Support/{APP_NAME}'),
            'autostart_dir': os.path.expanduser('~/Library/LaunchAgents')
        }
    else:  # Windows
        program_files = os.environ.get('PROGRAMFILES', 'C:\\Program Files')
        return {
            'app_dir': os.path.join(program_files, APP_NAME),
            'bin_dir': os.path.join(program_files, APP_NAME),
            'desktop_dir': os.path.join(os.environ.get('APPDATA', ''), 'Microsoft', 'Windows', 'Start Menu', 'Programs'),
            'icon_dir': os.path.join(program_files, APP_NAME, 'icons'),
            'config_dir': os.path.join(os.environ.get('APPDATA', ''), APP_NAME),
            'autostart_dir': os.path.join(os.environ.get('APPDATA', ''), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
        }
```

### Version Tracking System
```python
def get_version_info():
    """Get current version information"""
    return {
        'version': VERSION,
        'app_name': APP_NAME,
        'executable': EXECUTABLE_NAME,
        'description': DESCRIPTION,
        'install_date': datetime.now().isoformat(),
        'python_version': sys.version,
        'platform': platform.system()
    }

def check_existing_installation(paths):
    """Check if app is already installed and get version"""
    version_file = os.path.join(paths['app_dir'], 'version.json')
    if os.path.exists(version_file):
        try:
            with open(version_file, 'r') as f:
                return json.load(f)
        except:
            return None
    return None
```

### Desktop Integration Best Practices

#### Linux Desktop Entry with Actions
```python
def create_desktop_entry_linux(paths, icon_path):
    """Create Linux desktop entry with actions"""
    desktop_content = f"""[Desktop Entry]
Name={APP_NAME}
GenericName={GENERIC_NAME}
Comment={DESCRIPTION}
Exec={EXECUTABLE_NAME}
Icon={EXECUTABLE_NAME}
Terminal=false
Type=Application
Categories=Utility;Accessibility;Office;
StartupNotify=true
Keywords=text;expansion;keyboard;automation;
MimeType=text/yaml;application/x-yaml;
StartupWMClass={EXECUTABLE_NAME}
Actions=configure;viewlogs;

[Desktop Action configure]
Name=Configure
Exec={EXECUTABLE_NAME} --configure
Icon={EXECUTABLE_NAME}

[Desktop Action viewlogs]
Name=View Logs
Exec={EXECUTABLE_NAME} --view-logs
Icon={EXECUTABLE_NAME}
"""
    
    desktop_file = os.path.join(paths['desktop_dir'], f'{EXECUTABLE_NAME}.desktop')
    os.makedirs(paths['desktop_dir'], exist_ok=True)
    
    with open(desktop_file, 'w') as f:
        f.write(desktop_content)
    
    os.chmod(desktop_file, 0o644)
    print(f"Created desktop entry: {desktop_file}")
```

#### Windows Integration
```python
def create_windows_shortcut(paths):
    """Create Windows Start Menu shortcut"""
    try:
        import win32com.client
        
        shell = win32com.client.Dispatch("WScript.Shell")
        shortcut = shell.CreateShortCut(os.path.join(paths['desktop_dir'], f'{APP_NAME}.lnk'))
        shortcut.Targetpath = os.path.join(paths['bin_dir'], f'{EXECUTABLE_NAME}.bat')
        shortcut.WorkingDirectory = paths['app_dir']
        shortcut.IconLocation = os.path.join(paths['icon_dir'], f'{EXECUTABLE_NAME}.ico')
        shortcut.Description = DESCRIPTION
        shortcut.save()
        print(f"Created Windows shortcut: {shortcut.FullName}")
    except ImportError:
        print("Could not create Windows shortcut (win32com not available)")
```

#### macOS App Bundle
```python
def create_macos_app_bundle(paths):
    """Create macOS app bundle"""
    app_bundle = f"/Applications/{APP_NAME}.app"
    contents_dir = os.path.join(app_bundle, "Contents")
    macos_dir = os.path.join(contents_dir, "MacOS")
    resources_dir = os.path.join(contents_dir, "Resources")
    
    os.makedirs(macos_dir, exist_ok=True)
    os.makedirs(resources_dir, exist_ok=True)
    
    # Create Info.plist
    info_plist = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleExecutable</key>
    <string>{EXECUTABLE_NAME}</string>
    <key>CFBundleIdentifier</key>
    <string>com.{EXECUTABLE_NAME.replace('-', '')}.{EXECUTABLE_NAME}</string>
    <key>CFBundleName</key>
    <string>{APP_NAME}</string>
    <key>CFBundleVersion</key>
    <string>{VERSION}</string>
    <key>CFBundleShortVersionString</key>
    <string>{VERSION}</string>
    <key>CFBundleIconFile</key>
    <string>{EXECUTABLE_NAME}.icns</string>
    <key>LSApplicationCategoryType</key>
    <string>public.app-category.utilities</string>
    <key>NSHighResolutionCapable</key>
    <true/>
</dict>
</plist>
"""
    
    with open(os.path.join(contents_dir, "Info.plist"), 'w') as f:
        f.write(info_plist)
    
    print(f"Created macOS app bundle: {app_bundle}")
```

### Error Handling and Recovery
```python
def install_with_rollback(user_install=False):
    """Install with rollback capability"""
    paths = get_install_paths(user_install)
    backup_paths = []
    
    try:
        # Backup existing files
        if os.path.exists(paths['app_dir']):
            backup_path = f"{paths['app_dir']}.backup.{int(time.time())}"
            shutil.move(paths['app_dir'], backup_path)
            backup_paths.append(backup_path)
        
        # Perform installation
        install_application(paths)
        
        # Verify installation
        verify_installation(paths)
        
        # Clean up backups on success
        for backup_path in backup_paths:
            if os.path.exists(backup_path):
                shutil.rmtree(backup_path)
        
        print("Installation completed successfully!")
        
    except Exception as e:
        print(f"Installation failed: {e}")
        
        # Rollback changes
        if os.path.exists(paths['app_dir']):
            shutil.rmtree(paths['app_dir'])
        
        for backup_path in backup_paths:
            if os.path.exists(backup_path):
                original_path = backup_path.split('.backup.')[0]
                shutil.move(backup_path, original_path)
                print(f"Restored backup: {original_path}")
        
        raise InstallerError(f"Installation failed and was rolled back: {e}")
```

### Installation Verification
```python
def verify_installation(paths):
    """Verify installation was successful"""
    # Check if executable exists
    executable = os.path.join(paths['bin_dir'], EXECUTABLE_NAME)
    if not os.path.exists(executable):
        raise InstallerError(f"Executable not found: {executable}")
    
    # Test app launch
    try:
        result = subprocess.run([executable, '--version'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode != 0:
            raise InstallerError("App failed to launch")
    except subprocess.TimeoutExpired:
        raise InstallerError("App launch timed out")
    
    # Check desktop integration
    if platform.system() == "Linux":
        desktop_file = os.path.join(paths['desktop_dir'], f'{EXECUTABLE_NAME}.desktop')
        if not os.path.exists(desktop_file):
            raise InstallerError(f"Desktop entry not found: {desktop_file}")
    
    print("✅ Installation verification passed")
```

## File Structure Standards

### Required Files
```
your-app/
├── setup.py                    # Main installer
├── install.sh                  # Linux/macOS wrapper
├── install.bat                 # Windows wrapper
├── uninstall.py               # Standalone uninstaller
├── requirements.txt           # Dependencies
├── create_icon.py            # Icon generation
├── icons/                    # Generated icons
├── your_app.py              # Main application
└── scripts/                 # Platform-specific helpers
    ├── install_linux.sh
    ├── install_macos.sh
    └── install_windows.bat
```

### Success Metrics
- [ ] Cross-platform compatibility (Linux, Windows, macOS)
- [ ] User vs system installation options
- [ ] Complete uninstaller with configuration preservation
- [ ] Version tracking and update detection
- [ ] Professional desktop integration
- [ ] Comprehensive error handling and rollback
- [ ] Command-line interface with full options
- [ ] Installation verification system

## Common Pitfalls to Avoid

1. **Platform-specific code without detection**
2. **Hardcoded paths that don't work cross-platform**
3. **No rollback mechanism on failed installs**
4. **Overwriting user config without backup**
5. **No version tracking for updates**
6. **Incomplete uninstaller cleanup**
7. **Missing desktop integration**
8. **Poor error messages without solutions**

This guide represents the consolidated best practices for professional Python application installers.
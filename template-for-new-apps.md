# 🚀 Complete App Development Template

## 📍 Version Management System

### **Single Source of Truth**
**All version information is centralized in one file:**
```
src/your_app_name/version.py
```

### **Create Version Module:**
```python
"""
Your App Version Management
Single source of truth for version information
"""

__version__ = "1.0.0"
__version_info__ = (1, 0, 0)

# Additional version metadata
VERSION_MAJOR = 1
VERSION_MINOR = 0
VERSION_PATCH = 0
VERSION_BUILD = "2025.01.22"  # Build date
VERSION_CODENAME = "Your Codename"

# Full version string for display
FULL_VERSION = f"{__version__} ({VERSION_CODENAME})"
BUILD_INFO = f"v{__version__} - Build {VERSION_BUILD}"

# API version for compatibility
API_VERSION = "1.0"

def get_version():
    """Return the current version string"""
    return __version__

def get_version_info():
    """Return version as tuple (major, minor, patch)"""
    return __version_info__

def get_full_version():
    """Return full version string with codename"""
    return FULL_VERSION

def get_build_info():
    """Return build information string"""
    return BUILD_INFO
```

### **Update Package __init__.py:**
```python
"""
Your App Name

Description of your application
"""

from .version import __version__, get_version, get_full_version, get_build_info

__all__ = ['__version__', 'get_version', 'get_full_version', 'get_build_info']
```

### **Configure pyproject.toml:**
```toml
[project]
name = "your-app-name"
dynamic = ["version"]
description = "Your app description"
authors = [{name = "Your Team", email = "team@example.com"}]
license = {text = "MIT"}
readme = "README.md"
requires-python = ">=3.8"

dependencies = [
    # Your dependencies here
]

[tool.setuptools.dynamic]
version = {attr = "your_app_name.version.__version__"}

[build-system]
requires = ["setuptools", "wheel"]
build-backend = "setuptools.build_meta"
```

## 🎨 Professional Icon Creation

### **Create Icon Generator Script:**
```python
#!/usr/bin/env python3
"""
Professional Icon Generator
Creates multi-size icons for desktop integration
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_app_icon(size=128):
    """Create a professional application icon"""
    
    # Create image with transparent background
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Define your color scheme
    primary_color = (44, 93, 63)    # Main color
    accent_color = (74, 144, 164)   # Accent color
    text_color = (255, 255, 255)    # White text
    highlight_color = (40, 167, 69) # Success color
    
    # Draw main background circle
    margin = size // 8
    draw.ellipse([margin, margin, size-margin, size-margin], 
                fill=primary_color, outline=accent_color, width=3)
    
    # Add your app's distinctive visual elements here
    # Example: Letters, symbols, shapes that represent your app
    
    # Center text (app initials)
    try:
        font_size = size // 3
        font = ImageFont.load_default()
        text = "YA"  # Your App initials
        
        # Get text bounding box for centering
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        text_x = (size - text_width) // 2
        text_y = (size - text_height) // 2
        
        draw.text((text_x, text_y), text, font=font, fill=text_color)
    except:
        # Fallback if font loading fails
        pass
    
    return img

def create_all_icon_sizes(base_name="your-app-icon"):
    """Create all standard icon sizes"""
    print(f"🎨 Creating {base_name} icons...")
    
    sizes = [16, 32, 48, 64, 128]
    
    for size in sizes:
        icon = create_app_icon(size)
        filename = f"{base_name}-{size}.png" if size != 128 else f"{base_name}.png"
        icon.save(filename, "PNG")
        print(f"✅ Icon created: {filename}")
    
    return f"{base_name}.png"

if __name__ == "__main__":
    create_all_icon_sizes("your-app-icon")
```

### **Icon Size Standards:**
- **16px** - System tray, small UI elements
- **32px** - Standard small icon
- **48px** - Standard medium icon  
- **64px** - Large icon
- **128px** - Main application icon, desktop launchers

## 🖥️ Desktop Integration System

### **Create Desktop Launcher (.desktop file):**
```ini
[Desktop Entry]
Version=1.0
Type=Application
Name=Your App Name - Interactive Interface
Comment=Description of your application
Exec=/path/to/your/app/launch-your-app.sh
Icon=/path/to/your/app/your-app-icon.png
Terminal=true
Categories=Development;Utility;YourCategory;
Keywords=keyword1;keyword2;keyword3;
StartupNotify=true
```

### **Create Launch Script (launch-your-app.sh):**
```bash
#!/bin/bash
# Your App Launcher Script
# Automatically launches your application

# Configuration - Edit these values as needed
DEFAULT_ARG1="default_value"
DEFAULT_ARG2="another_default"
DEFAULT_PORT="8080"

# Get current directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Get version information
VERSION=$(PYTHONPATH=src python -c "from your_app_name.version import get_full_version; print(get_full_version())" 2>/dev/null || echo "Version Unknown")

echo "🚀 Starting Your Application..."
echo "📦 $VERSION"
echo "📁 Working directory: $SCRIPT_DIR"
echo "🌐 Arguments: $DEFAULT_ARG1, $DEFAULT_ARG2"
echo "🔗 Port: $DEFAULT_PORT"
echo ""

# Change to the script directory
cd "$SCRIPT_DIR"

# Launch your application
PYTHONPATH=src python -m your_app_name.main \
  "$DEFAULT_ARG1" \
  --arg2 "$DEFAULT_ARG2" \
  --port "$DEFAULT_PORT"

# Keep terminal open on exit
echo ""
echo "Application has stopped. Press Enter to close this window..."
read
```

### **Make Files Executable:**
```bash
chmod +x your-app.desktop
chmod +x launch-your-app.sh
```

### **Desktop Integration Commands:**
```bash
# Add to applications menu
cp your-app.desktop ~/.local/share/applications/
update-desktop-database ~/.local/share/applications/

# Add to desktop
cp your-app.desktop ~/Desktop/
chmod +x ~/Desktop/your-app.desktop
```

## 🔧 Version Control Setup

### **Initialize Git Repository:**
```bash
# Initialize repo
git init
git branch -m main

# Create .gitignore
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# Virtual environments
venv/
env/
ENV/
.venv/
.env/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Logs
*.log
logs/

# Testing
.pytest_cache/
.coverage
htmlcov/
.tox/
.nox/

# App specific
debug_sessions/
*.backup
temp_files/

# Browser automation
.playwright/
screenshots/
EOF
```

### **First Commit Template:**
```bash
git add .
git commit -m "feat: Initial application setup with complete infrastructure

🎯 Core Features:
- [List your main features]
- Professional desktop integration
- Centralized version management
- Complete development infrastructure

🖥️ Desktop Integration:
- One-click launcher (.desktop file)  
- Professional icon set (5 sizes: 16px to 128px)
- Configurable launch script
- System integration ready

📦 Version Management:
- Single source of truth in version.py
- Automatic propagation to all components
- Professional version display system
- Semantic versioning ready

🔧 Infrastructure:
- Complete project structure
- Git repository with proper .gitignore
- Package configuration (pyproject.toml)
- Documentation and templates

🔧 Generated with Claude Code
Co-Authored-By: Claude <noreply@anthropic.com>"
```

## 📋 CLI Integration Template

### **Add Version to CLI:**
```python
# In your main CLI module
from your_app_name.version import __version__, get_full_version, get_build_info

def create_parser():
    parser = argparse.ArgumentParser(
        prog='your-app-cli',
        description='Your Application - Description'
    )
    
    # Add version argument
    parser.add_argument(
        '--version', '-v',
        action='version',
        version=f'Your App {get_full_version()}\n{get_build_info()}'
    )
    
    # Add your other arguments
    return parser
```

### **Web Interface Integration:**
```python
# In FastAPI app
from your_app_name.version import __version__, get_full_version, get_build_info

app = FastAPI(
    title="Your Application",
    description="Your app description",
    version=__version__
)

@app.get("/")
async def dashboard(request: Request):
    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "version": __version__,
            "full_version": get_full_version(),
            "build_info": get_build_info()
        }
    )
```

## 📁 Complete Project Structure Template

```
your-app-name/                      # Root directory
├── .git/                          # Git repository
├── .gitignore                     # Git ignore rules
├── README.md                      # Main documentation
├── pyproject.toml                 # Package configuration
├── requirements.txt               # Python dependencies
├── LICENSE                        # License file
│
├── your-app.desktop              # Desktop launcher
├── launch-your-app.sh            # Launch script
├── your-app-icon.png             # Main icon (128px)
├── your-app-icon-64.png          # Medium icon
├── your-app-icon-48.png          # Standard icon
├── your-app-icon-32.png          # Small icon
├── your-app-icon-16.png          # Tiny icon
├── create_icon.py                # Icon generator script
│
├── src/                          # Source code
│   └── your_app_name/
│       ├── __init__.py           # Package init with version
│       ├── version.py            # VERSION CONTROL CENTER
│       ├── main.py               # Main application
│       ├── cli.py                # Command line interface
│       │
│       ├── core/                 # Core functionality
│       ├── utils/                # Utilities
│       ├── web/                  # Web interface (if applicable)
│       │   ├── templates/        # HTML templates
│       │   └── static/           # CSS/JS files
│       └── tests/                # Test files
│
├── docs/                         # Documentation
│   ├── USAGE.md                  # Usage instructions
│   ├── DESKTOP_INTEGRATION.md    # Desktop setup guide
│   └── API.md                    # API documentation (if applicable)
│
└── scripts/                      # Development scripts
    ├── build.sh                  # Build script
    ├── test.sh                   # Test script
    └── release.sh                # Release script
```

## 🎯 Development Workflow

### **Version Update Process:**
1. Edit `src/your_app_name/version.py` - ONLY place to change version
2. Test: `python -c "from your_app_name import __version__; print(__version__)"`
3. Test CLI: `python -m your_app_name --version`
4. Commit: `git commit -m "bump: Update version to v1.1.0"`
5. Tag: `git tag -a v1.1.0 -m "Release version 1.1.0"`

### **Icon Update Process:**
1. Modify `create_icon.py` design elements
2. Run: `python create_icon.py`
3. Test desktop launcher double-click functionality
4. Commit updated icons

### **Desktop Integration Testing:**
```bash
# Test launcher script
./launch-your-app.sh

# Test desktop file (on Linux)
desktop-file-validate your-app.desktop

# Install to system
cp your-app.desktop ~/.local/share/applications/
```

## 🚀 Benefits of This Template

### **Professional Standards:**
- ✅ Single source of truth for versions
- ✅ Professional icon set (multiple sizes)
- ✅ Desktop integration ready
- ✅ Version control best practices
- ✅ Semantic versioning support
- ✅ Complete development infrastructure

### **Easy Maintenance:**
- ✅ One place to change version numbers
- ✅ Automatic version propagation
- ✅ Professional release process
- ✅ Standardized project structure
- ✅ Complete documentation

### **Cross-Platform Ready:**
- ✅ Linux desktop integration (.desktop files)
- ✅ Windows compatibility (launch scripts)
- ✅ macOS support (icon standards)
- ✅ Professional icon sizes for all platforms

## 📚 Usage for Future Apps

1. **Copy this template** to new project directory
2. **Replace "your-app-name"** with actual app name throughout
3. **Replace "YA"** in icon generator with your app initials
4. **Customize colors** in icon generator for your brand
5. **Update descriptions** and categories in .desktop file
6. **Modify launch script** arguments for your specific needs
7. **Follow version update process** for releases

---

**This template provides enterprise-grade application infrastructure that can be followed by any LLM or developer for consistent, professional app development! 🎯**
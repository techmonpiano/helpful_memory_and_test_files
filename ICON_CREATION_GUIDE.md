# Simple Icon Creation Guide for Python

This guide covers creating simple icons programmatically using Python's PIL/Pillow library, following Linux desktop standards.

## System Requirements

✅ **Available on this system:**
- Python 3 (`/usr/bin/python3`)  
- PIL/Pillow version 9.0.1
- ImageDraw module
- ImageMagick convert utility

## Standard Linux Desktop Icon Sizes

Based on freedesktop.org Icon Theme Specification:
- **Standard sizes**: 8x8, 16x16, 20x20, 22x22, 24x24, 28x28, 32x32, 36x36, 40x40, 42x42, 48x48, 64x64, 72x72, 96x96, 128x128, 256x256, 512x512
- **Minimum requirement**: 48x48 PNG in hicolor theme
- **Format**: PNG (recommended), SVG (scalable), XPM (legacy)
- **Shape**: Perfect square (width = height)
- **Location**: `$HOME/.icons`, `/usr/share/icons`, `/usr/share/pixmaps`

## Existing System Icons

Found these relevant system icons in `/usr/share/icons/Adwaita/`:
- **Alarm icons**: Available in 16x16 through 96x96 plus scalable SVG
- **Notification icons**: Multiple sizes for system notifications
- **Time-related icons**: preferences-system-time-symbolic

## Creating Icons with PIL/Pillow

### Basic Setup
```python
from PIL import Image, ImageDraw
import math
import os

# Create transparent background image
img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
draw = ImageDraw.Draw(img)
```

### Drawing Geometric Shapes
- **Circles**: `draw.ellipse(bbox, outline=color, width=line_width)`
- **Lines**: `draw.line([x1, y1, x2, y2], fill=color, width=line_width)`
- **Polygons**: `draw.polygon(points_list, outline=color, width=line_width)`
- **Rectangles**: `draw.rectangle(bbox, outline=color, width=line_width)`

### Icon Design Tips
1. **Use relative sizing**: Calculate dimensions as percentages of icon size
2. **Scale line widths**: Use `max(1, size//16)` for proper scaling
3. **Center elements**: Use `center = size // 2` as reference point
4. **Maintain proportions**: Keep shapes recognizable at small sizes

## Practical Examples

### Clock Icon
```python
def create_clock_icon(size=48, color='#2e3436'):
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    center = size // 2
    radius = int(size * 0.4)
    
    # Clock face circle
    circle_bbox = [center - radius, center - radius, center + radius, center + radius]
    draw.ellipse(circle_bbox, outline=color, width=max(1, size//16))
    
    # Clock hands
    draw.line([center, center, center + radius//2, center], fill=color, width=max(1, size//20))  # Hour
    draw.line([center, center, center, center - int(radius * 0.8)], fill=color, width=max(1, size//24))  # Minute
    
    return img
```

### Bell Icon
```python
def create_bell_icon(size=48, color='#2e3436'):
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    center_x = size // 2
    # Draw trapezoid bell shape using polygon
    bell_points = [
        (center_x - size//8, size//5),      # Top left
        (center_x + size//8, size//5),      # Top right  
        (center_x + size//4, size//5 + size//2),  # Bottom right
        (center_x - size//4, size//5 + size//2),  # Bottom left
    ]
    draw.polygon(bell_points, outline=color, width=max(1, size//16))
    
    return img
```

## Free Icon Resources

### Public Domain & CC0 Libraries
- **CC0 Icons**: GitHub repository with no attribution required
- **Aiconica.net**: 1000+ free creative commons icons
- **Rawpixel**: Vintage clock/bell icons with CC0 licensing
- **Flaticon**: 179,477+ clock icons (various licenses)

### Creative Commons Resources
- **Creative Commons Icons**: 39 solid icons under MIT License
- **Bootstrap Icons**: Bell/notification icons under MIT, Apache, CC0 licenses

## System Icon Utilities

Available command-line tools:
- **ImageMagick**: `convert` - Format conversion and editing
- **Icon conversion**: `icontopbm`, `pbmtoicon`, `ppmtowinicon`, `winicontoppm`
- **GTK tools**: `gtk-update-icon-cache`, `gtk4-update-icon-cache`
- **XDG tools**: `xdg-icon-resource`, `xdg-desktop-icon`

## Complete Icon Creation Script

The included `create_simple_icons.py` provides:
- Functions to create clock, bell, and reminder icons
- Standard size generation (16x16 through 256x256)
- Customizable colors and backgrounds
- Batch creation of icon sets
- PNG output with transparency

### Usage Examples
```python
# Create single 48x48 icon
icon = create_clock_icon(48, color='#1f5582')
icon.save('my_clock.png')

# Create complete icon set in all standard sizes
save_icon_set(create_bell_icon, "bell", output_dir="my_icons")

# Create custom colored versions
blue_clock = lambda size: create_clock_icon(size, color='#1f5582')
save_icon_set(blue_clock, "clock_blue")
```

## Installation in Linux Desktop

1. **User icons**: Place in `~/.icons/hicolor/48x48/apps/`
2. **System icons**: Place in `/usr/share/icons/hicolor/48x48/apps/`
3. **Update cache**: Run `gtk-update-icon-cache ~/.icons/hicolor/`
4. **Desktop files**: Reference icon by filename (without extension)

## Best Practices

1. **Start with 48x48**: Most commonly used size, easiest to design
2. **Test at 16x16**: Ensure icon remains recognizable when small  
3. **Use system colors**: Default `#2e3436` matches system theme
4. **Provide multiple sizes**: Better scaling and performance
5. **Keep it simple**: Complex details disappear at small sizes
6. **Use consistent style**: Match existing system icon aesthetic

This guide provides everything needed to create professional-looking icons programmatically using Python, following Linux desktop standards and best practices.
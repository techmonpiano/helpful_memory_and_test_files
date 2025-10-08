# PyQt Focus-Free Floating Menus: Implementation patterns and working code

Creating floating menus in PyQt5/PyQt6 that don't steal focus requires specific window flags, attributes, and platform-aware implementations. This research uncovered multiple working repositories demonstrating effective patterns for non-intrusive overlays, context menus, and floating widgets.

## Platform-specific window flag combinations prove most effective

The most reliable approach varies by operating system, with successful implementations using conditional logic to apply appropriate flags. **Qt.WindowDoesNotAcceptFocus** works explicitly on Windows, while Linux and macOS benefit from **Qt.ToolTip** or **Qt.Tool** flags that inherently avoid focus stealing.

Recent repositories demonstrate this pattern effectively. The **manateelazycat/popweb** project implements popup web windows for Emacs using PyQt6 with platform detection:

```python
if platform.system() == "Windows":
    self.setWindowFlags(Qt.WindowType.FramelessWindowHint | 
                       Qt.WindowType.WindowStaysOnTopHint | 
                       Qt.WindowType.Tool | 
                       Qt.WindowType.WindowDoesNotAcceptFocus)
else:
    self.setWindowFlags(Qt.WindowType.FramelessWindowHint | 
                       Qt.WindowType.WindowStaysOnTopHint | 
                       Qt.WindowType.ToolTip)
```

This conditional approach addresses the reality that focus behavior differs significantly across platforms. Windows requires explicit focus prevention through **WindowDoesNotAcceptFocus**, while Unix-like systems achieve the same result through window type hints.

## Transparent input overlays enable advanced non-intrusive interfaces

Gaming overlays and HUD applications demonstrate particularly sophisticated focus management. The **PythonOverlayLib** repository implements a comprehensive overlay system using **Qt.WindowTransparentForInput**, which passes mouse events through the window entirely:

```python
self.setWindowFlags(QtCore.Qt.FramelessWindowHint | 
                   QtCore.Qt.WindowTransparentForInput | 
                   QtCore.Qt.WindowStaysOnTopHint)
self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
```

This pattern appears frequently in gaming overlays like the **Rust-Recoil-Script** crosshair overlay, where maintaining game input responsiveness is critical. The **WindowTransparentForInput** flag creates truly non-interfering overlays that can display information without intercepting any user input.

## Widget attributes complement window flags for complete focus prevention

Beyond window flags, specific widget attributes provide additional focus control. **Qt.WA_ShowWithoutActivating** prevents window activation when shown, while **Qt.WA_X11DoNotAcceptFocus** offers Linux-specific focus prevention:

```python
class NonFocusFloatingMenu(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Core window flags
        self.setWindowFlags(Qt.Tool | Qt.FramelessWindowHint | 
                           Qt.WindowStaysOnTopHint | Qt.WindowDoesNotAcceptFocus)
        
        # Essential attributes
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setAttribute(Qt.WA_ShowWithoutActivating, True)
        
        # Platform-specific enhancements
        if hasattr(Qt, 'WA_X11DoNotAcceptFocus'):
            self.setAttribute(Qt.WA_X11DoNotAcceptFocus, True)
```

The **zhiyiYo/PyQt-Frameless-Window** library and its PySide6 port **rayzchen/PySide6-Frameless-Window** implement cross-platform frameless windows with comprehensive focus management, supporting Windows, Linux, and macOS with platform-specific optimizations.

## System tray applications naturally avoid focus conflicts

Multiple repositories implement system tray applications with context menus that inherently don't steal focus. The **PyQt5/PyQt** repository includes QQMenu.py, which creates translucent context menus using a combination of transparency attributes and frameless hints:

```python
self.context_menu.setAttribute(Qt.WA_TranslucentBackground)
self.context_menu.setWindowFlags(
    self.context_menu.windowFlags() | 
    Qt.FramelessWindowHint | 
    Qt.NoDropShadowWindowHint
)
```

System tray menus benefit from operating system conventions that prevent them from disrupting the active application. Projects like **god233012yamil/PyQt5_How_to_show_an_icon_in_the_system_tray** and various clipboard managers leverage this behavior for non-intrusive popup menus.

## Focus policy management extends to child widgets

Comprehensive focus prevention requires managing not just the window but all interactive elements within it. Setting **Qt.NoFocus** on child widgets prevents them from accepting keyboard focus:

```python
def setup_ui(self):
    layout = QVBoxLayout(self)
    
    # All interactive elements must have NoFocus policy
    for i in range(3):
        btn = QPushButton(f"Menu Item {i+1}")
        btn.setFocusPolicy(Qt.NoFocus)
        layout.addWidget(btn)
```

The floating button implementation from **gist.github.com/namuan/e34387e53e62b52c6aea2146108a92c7** demonstrates an alternative approach where widgets remain within their parent container, avoiding focus issues through hierarchical relationships rather than window flags.

## Event handling patterns preserve focus state

Advanced implementations store and restore focus state when displaying floating menus. This pattern appears in tooltip widgets and context-sensitive menus:

```python
def showEvent(self, event):
    # Store currently focused widget before showing menu
    self.previous_focus_widget = QApplication.focusWidget()
    super().showEvent(event)

def focusInEvent(self, event):
    # Immediately transfer focus back to previous widget
    if self.previous_focus_widget:
        self.previous_focus_widget.setFocus()
    super().focusInEvent(event)
```

The **pyqt-tooltip-widget** repository implements hover-based tooltips with methods like **setStillOpenWhenCursorLeaveFromToolTipWidget()** for fine-grained control over menu persistence without focus interference.

## Complete working implementations demonstrate practical applications

Screenshot tools provide particularly relevant examples. **SnapTrace** (Jiyath5516F/SnapTrace) implements professional screenshot annotation with non-intrusive overlay menus. Clipboard managers like **Clipboard-Pro** (ferbcn/Clipboard-Pro) use PyQt6 with system tray integration to display floating history menus without disrupting workflow.

The most comprehensive pattern combines multiple techniques:

```python
class ContextFloatingMenu(QWidget):
    def __init__(self):
        super().__init__()
        
        # Configure as truly non-intrusive
        self.setWindowFlags(Qt.Tool | Qt.FramelessWindowHint | 
                           Qt.WindowStaysOnTopHint | Qt.WindowDoesNotAcceptFocus)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setAttribute(Qt.WA_ShowWithoutActivating, True)
        
        # Ensure no child widgets can take focus
        self.setFocusPolicy(Qt.NoFocus)
```

## Platform limitations require defensive programming

Research reveals significant platform-specific challenges. Windows may require additional Win32 API calls for complete focus prevention, while X11 behavior varies by window manager. The **Qt.X11BypassWindowManagerHint** flag provides additional control on Linux systems but isn't universally supported.

Recent activity shows continued development in this area. Projects updated within the last three years consistently adopt the window flag combination approach, with increasing use of **WindowTransparentForInput** for overlay applications. The gaming and productivity tool sectors drive innovation in non-intrusive UI patterns.

## Conclusion

Creating non-focus-stealing floating menus in PyQt requires combining appropriate window flags, widget attributes, and platform-aware code. The most reliable implementations use **Qt.Tool | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint** as a base, adding **Qt.WindowDoesNotAcceptFocus** on Windows or **Qt.ToolTip** on other platforms. Transparent input overlays using **Qt.WindowTransparentForInput** provide the most complete focus avoidance for overlay applications. These patterns, demonstrated in numerous active repositories, enable developers to create professional floating interfaces that enhance rather than interrupt user workflows.
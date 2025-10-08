# Terminal Keyboard Shortcuts Research Session - 2025-09-26

## Session Overview
User inquiry about advanced cursor movement and text selection capabilities in terminal applications, specifically asking about keyboard shortcuts similar to those in standard text editors (Ctrl+Shift+arrows, Ctrl+arrows, Shift+Home/End).

## Key Findings

### Standard Terminal Cursor Movement
Most terminal applications support these universal shortcuts:

**Basic Movement:**
- `Ctrl+A` - Move to beginning of line
- `Ctrl+E` - Move to end of line
- `Ctrl+B` or `←` - Move back one character
- `Ctrl+F` or `→` - Move forward one character

**Word-Level Movement:**
- `Alt+B` or `Ctrl+←` - Move back one word
- `Alt+F` or `Ctrl+→` - Move forward one word

### Text Selection in Terminals
**Limited native support:** Most terminals don't support keyboard-based text selection natively.

**Modern terminals with selection support:**
- `Shift+←/→` - Select character by character
- `Shift+Ctrl+←/→` - Select word by word
- `Shift+Home/End` - Select to beginning/end of line

### Terminal Emulator Capabilities

#### Advanced Selection Support:
- **kitty** - Full keyboard selection support ✅
- **Alacritty** - Limited selection support ⚠️
- **GNOME Terminal** - Basic selection support ⚠️
- **iTerm2** (macOS) - Extensive selection support ✅

#### Alternative Solutions:
- `Ctrl+X Ctrl+E` - Opens current command in default editor (bash/zsh)
- **tmux copy mode** - `Ctrl+B [` for vim-like text selection
- **screen copy mode** - Similar functionality to tmux

## Research: Kitty Terminal Open Source Status

### License Information
**Kitty terminal emulator is fully open source:**
- **License:** GNU General Public License version 3.0 (GPLv3)
- **Repository:** https://github.com/kovidgoyal/kitty
- **Platform:** Cross-platform (Linux, macOS, BSD)
- **Features:** GPU-accelerated, extensive keyboard shortcuts

### Important Distinction
**Two different "Kitty" projects exist:**
1. **kitty** (lowercase) - GPU-accelerated terminal emulator (GPLv3)
2. **KiTTY** (uppercase) - Windows PuTTY fork (also GPL)

## Recommendations

### For Advanced Text Editing in Terminal:
1. **Use kitty terminal** - Best keyboard selection support
2. **Configure tmux** - Powerful copy/paste with vim-like keys
3. **Editor integration** - Use `Ctrl+X Ctrl+E` for complex editing
4. **iTerm2 on macOS** - Excellent selection capabilities

### Key Limitations:
- Most terminals prioritize shell shortcuts over text editor conventions
- Keyboard selection varies significantly between terminal emulators
- Standard copy/paste (Ctrl+Shift+C/V) is more universally supported

## Session Notes
- **No troubleshooting required** - Informational query only
- **Research successful** - Comprehensive answer provided
- **Additional research** - Verified kitty's open source status (GPLv3)

## Technical Context
- Session conducted in Claude Code environment
- User working in `/home/user1/shawndev1/friendlyterm` directory
- Platform: Linux 6.8.0-83-generic
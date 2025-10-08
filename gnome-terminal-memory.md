# GNOME Terminal Configuration Memory Bank

## Ctrl+Backspace Word Deletion Issue

### The Core Problem
- Older gnome-terminal versions send identical character codes for Backspace and Ctrl+Backspace
- This makes them indistinguishable to applications running in the terminal
- Fixed in vte-0.42 (GNOME 3.18+) but still affects many systems
- The "Backspace key generates" setting affects what character is sent

### Diagnostic Steps
1. Test what your terminal sends: Press `Ctrl+V` then `Ctrl+Backspace`
2. Common results:
   - `^H` (Control-H character)
   - `^?` (ASCII DEL character)  
   - Same as regular Backspace (problematic)

### Solutions

#### Option 1: ~/.inputrc Configuration
Add to `~/.inputrc` file:

For direct word deletion:
```
"\C-H": backward-kill-word
```

For mapping to existing Ctrl+W:
```
"\C-H": "\C-w"
```

For punctuation-aware deletion (like Ctrl+Left/Right):
```
"\C-H": "\e\b"
```

#### Option 2: stty Command
Add to `~/.bashrc`:
```bash
# For systems where Ctrl+Backspace sends ^H
stty werase '^H'

# For systems where Ctrl+Backspace sends ^?
stty werase '^?'
```

#### Option 3: GNOME Terminal Settings
- Navigate to: Edit → Preferences → Profiles → [Profile] → Compatibility
- "Backspace key generates" options:
  - ASCII DEL (default, often problematic)
  - Control-H (may work better for Ctrl+Backspace)
  - Escape sequence

### Alternative Workarounds
- **Alt+Backspace**: Works by default for word deletion in most terminals
- **Ctrl+W**: Standard unix word deletion command
- **Ctrl+Alt+Backspace**: Some terminals use this instead

### Testing Your Configuration
1. Open new terminal after making changes
2. Type: `hello world test`
3. Press Ctrl+Backspace - should delete "test"
4. If not working, try Alt+Backspace to confirm word deletion works

### Historical Context
- Backspace key behavior is inconsistent due to historical terminal variations
- Different terminals send different character sequences
- Applications must be configured to recognize the specific sequence your terminal sends
- No universal standard exists for Ctrl+Backspace behavior
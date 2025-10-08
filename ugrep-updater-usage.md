# ugrep Section Auto-Updater Usage Guide

## Overview
The `update_claude_ugrep_section.py` script automatically updates ugrep sections in CLAUDE documentation files from a master template.

## Files Created
1. **Master Template**: `/home/user1/shawndev1/ugrep_master_template.md`
   - Contains the authoritative ugrep section
   - Single source of truth for all updates

2. **Update Script**: `/home/user1/shawndev1/update_claude_ugrep_section.py`
   - Python script to update CLAUDE files
   - Creates backups before changes
   - Can restore from backups

3. **Updated Files**:
   - `/home/user1/shawndev1/CLAUDE.md`
   - `/home/user1/shawndev1/CLAUDE_UNIVERSAL.md`

## Usage

### Basic Update (applies changes to all target files)
```bash
python3 /home/user1/shawndev1/update_claude_ugrep_section.py
```

### Dry Run (preview changes without applying)
```bash
python3 /home/user1/shawndev1/update_claude_ugrep_section.py --dry-run
```

### List Available Backups
```bash
python3 /home/user1/shawndev1/update_claude_ugrep_section.py --list-backups
```

### Restore from Backup
```bash
# Restore specific backup
python3 /home/user1/shawndev1/update_claude_ugrep_section.py --restore CLAUDE.md.backup_20250904_141323

# Restore to different file
python3 /home/user1/shawndev1/update_claude_ugrep_section.py --restore backup_name --restore-to target_file
```

### Add New Target File
```bash
python3 /home/user1/shawndev1/update_claude_ugrep_section.py --add-file /path/to/new/CLAUDE.md
```

## Workflow for Adding New ugrep Patterns

1. **Edit Master Template**:
   ```bash
   nano /home/user1/shawndev1/ugrep_master_template.md
   ```

2. **Test Changes** (dry run):
   ```bash
   python3 /home/user1/shawndev1/update_claude_ugrep_section.py --dry-run
   ```

3. **Apply Updates**:
   ```bash
   python3 /home/user1/shawndev1/update_claude_ugrep_section.py
   ```

4. **Verify Updates**:
   ```bash
   ugrep -n "CRITICAL:" /home/user1/shawndev1/CLAUDE*.md
   ```

## Key Features

- **Automatic Backups**: Every update creates timestamped backups in `/home/user1/shawndev1/claude_backups/`
- **Smart Section Detection**: Finds ugrep sections by header patterns
- **Preserves File Structure**: Only replaces ugrep section, leaves rest intact
- **Dry Run Mode**: Preview changes before applying
- **Restore Capability**: Can rollback to any backup

## New Issues Documented

### Issues Found (2025-01-04):
1. **Backslash-pipe (`\|`) doesn't work for OR** - Use plain pipe `|`
2. **Parentheses need `-F` flag for literal matching**
3. **File path errors** - Always use full paths or verify current directory
4. **Unnecessary `-r` flag on single files**

### Quick Reference Table Added:

| Pattern Type | Wrong ❌ | Right ✅ |
|-------------|----------|----------|
| OR patterns | `"pat1\|pat2"` | `"pat1|pat2"` |
| Literal parentheses | `"func\(\)"` or `"func()"` | `ugrep -F "func()"` |
| Directory search | `ugrep "pat" .` | `ugrep -r "pat" .` |
| Single file | `ugrep -r "pat" file` | `ugrep "pat" file` |
| Special chars | `"array[0]"` | `ugrep -F "array[0]"` |
| File paths | `"pat" file.sh` | `"pat" /full/path/file.sh` |

## Testing New Patterns

When you discover new failing patterns, test them first:

```bash
# Test the failing pattern
ugrep -n "failing\|pattern" file.py 2>&1

# Find the fix
ugrep -n "failing|pattern" file.py

# Add to master template
nano /home/user1/shawndev1/ugrep_master_template.md

# Update all CLAUDE files
python3 /home/user1/shawndev1/update_claude_ugrep_section.py
```

---
*Created: January 4, 2025*
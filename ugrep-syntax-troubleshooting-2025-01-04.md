# ugrep Syntax Troubleshooting Session - January 4, 2025

## Session Overview
This document captures findings from a troubleshooting session analyzing why certain ugrep commands were failing when used by an LLM following the CLAUDE_UNIVERSAL.md instructions.

## Key Discoveries

### 1. Primary Issue: OR Pattern Syntax
**CRITICAL FINDING:** ugrep uses plain pipe `|` for OR patterns, NOT backslash-pipe `\|`

- ❌ **WRONG:** `"pattern1\|pattern2"` (causes "Error: Error")
- ✅ **CORRECT:** `"pattern1|pattern2"`

This was the main cause of most failures. The LLM was using grep/sed style escaped pipes, but ugrep expects unescaped pipes.

### 2. Recursive Flag Usage
**FINDING:** The `-r` flag should only be used when searching directories, not single files

- ❌ **WRONG:** `ugrep -r -n "pattern" single-file.sh`
- ✅ **CORRECT:** `ugrep -n "pattern" single-file.sh`
- ✅ **CORRECT:** `ugrep -r -n "pattern" /directory/path/`

### 3. File Path Truncation
Some commands failed because file paths were truncated (ending with `...`). Always use complete paths.

## Failed Commands Analysis

### Case 1: Find with xargs (FAILED)
```bash
# Original (FAILED) - backslash-pipe issue
find /home/user1/shawndev1/kilocode -name "*.ts" -o -name "*.js" | \
  xargs ugrep -l "claude.*code.*provider\|ClaudeCodeProvider" 2>/dev/null

# Corrected (WORKS)
find /home/user1/shawndev1/kilocode -name "*.ts" -o -name "*.js" | \
  xargs ugrep -l "claude.*code.*provider|ClaudeCodeProvider" 2>/dev/null
```

### Case 2: Recursive search with OR (FAILED)
```bash
# Original (FAILED) - backslash-pipe issue
ugrep -r -l "claude.*code.*provider\|ClaudeCodeProvider" /home/user1/shawndev1/kilocode/src/ 2>/dev/null

# Corrected (WORKS)
ugrep -r -l "claude.*code.*provider|ClaudeCodeProvider" /home/user1/shawndev1/kilocode/src/ 2>/dev/null
```

### Case 3: Multiple OR patterns (FAILED)
```bash
# Original (FAILED) - backslash-pipe issue
ugrep -r -n "runProcess\|--disallowedTools" /home/user1/shawndev1/kilocode/src/integrations/ 2>/dev/null

# Corrected (WORKS)
ugrep -r -n "runProcess|--disallowedTools" /home/user1/shawndev1/kilocode/src/integrations/ 2>/dev/null
```

### Case 4: Context search with OR on single file (FAILED)
```bash
# Original (FAILED) - both backslash-pipe AND unnecessary -r flag
ugrep -r -n -A5 -B5 "sgdisk.*--new.*2\|parted.*mkpart.*2\|set.*2.*esp" enhanced-build-system-complete.sh 2>/dev/null

# Corrected (WORKS)
ugrep -n -A5 -B5 "sgdisk.*--new.*2|parted.*mkpart.*2|set.*2.*esp" enhanced-build-system-complete.sh 2>/dev/null
```

### Case 5: Simple pattern on single file (FAILED)
```bash
# Original (FAILED) - unnecessary -r flag for single file
ugrep -r -n "sgdisk.*--new.*2" enhanced-build-system-complete.sh 2>/dev/null

# Corrected (WORKS)
ugrep -n "sgdisk.*--new.*2" enhanced-build-system-complete.sh 2>/dev/null
```

### Case 6: Truncated path (FAILED)
```bash
# Original (FAILED) - path truncated with "..."
ugrep -n "get_available_tools_documentation\|generate_tool_documentation" \
  /home/user1/shawndev1/kilo-terminal/src/kilo_terminal/api/simplified_claude_code_provi...

# Corrected (WORKS) - use full path
ugrep -n "get_available_tools_documentation|generate_tool_documentation" \
  /home/user1/shawndev1/kilo-terminal/src/kilo_terminal/api/simplified_claude_code_provider.py
```

### Case 7: Complex OR pattern (WORKED after fix)
```bash
# Original (FAILED) - backslash-pipe and unnecessary -r
ugrep -r -n -A10 -B5 "fstab.*vfat\|EFI.*vfat\|umask.*fmask\|proc.*sysfs.*tmpfs" enhanced-build-system-complete.sh 2>/dev/null

# Corrected (WORKS)
ugrep -n -A10 -B5 "fstab.*vfat|EFI.*vfat|umask.*fmask|proc.*sysfs.*tmpfs" enhanced-build-system-complete.sh 2>/dev/null
```

## Successful Commands (For Reference)

### Case 1: Basic recursive search (WORKED)
```bash
ugrep -r -n "get_available_tools_documentation" /home/user1/shawndev1/kilo-terminal/src/ 2>/dev/null
```
✅ Correct use of `-r` for directory search

### Case 2: Complex OR with regex (WORKED after removing backslash)
```bash
# Note: This likely worked because it was searching a single file
ugrep -r -n -B5 -A10 "delete.*vm.*disk|DELETE_EXISTING_VM|existing.*vm.*disk" enhanced-build-system-complete.sh 2>/dev/null
```

## Best Practices and Correct Syntax

### Basic Searches
```bash
# Single file
ugrep -n "pattern" file.py

# Directory (recursive)
ugrep -r -n "pattern" /path/to/directory/

# With line numbers and context
ugrep -n -B3 -A3 "pattern" file.py

# Case insensitive
ugrep -i -n "pattern" file.py
```

### OR Patterns (Multiple Alternatives)
```bash
# Method 1: Using pipe (|) - NO BACKSLASH
ugrep -n "pattern1|pattern2|pattern3" file.py

# Method 2: Using multiple -e flags (cleaner for many patterns)
ugrep -n -e "pattern1" -e "pattern2" -e "pattern3" file.py

# Method 3: Boolean syntax (advanced)
ugrep --bool "pattern1 OR pattern2 OR pattern3" file.py
```

### Complex Patterns
```bash
# Multi-line patterns (spanning multiple lines)
ugrep -r -n --multiline "pattern1.*pattern2.*pattern3" /directory/

# Boolean AND queries (all terms must exist, any order)
ugrep -r -n --bool "term1 AND term2 AND term3" /directory/

# Exclude files/directories
ugrep -r -n --exclude='*.backup' --exclude='*.txt' "pattern" /directory/

# Limit results
ugrep -n -m5 "pattern" file.py  # Stop after 5 matches
```

### Common Flags Reference
- `-r` : Recursive search (ONLY for directories)
- `-n` : Show line numbers
- `-l` : List files with matches only
- `-i` : Case insensitive
- `-A NUM` : Show NUM lines after match
- `-B NUM` : Show NUM lines before match
- `-C NUM` : Show NUM lines before and after
- `-m NUM` : Stop after NUM matches
- `-e PATTERN` : Specify pattern (can use multiple)
- `--multiline` : Enable multi-line matching
- `--bool` : Use Boolean query syntax

## Error Patterns to Avoid

1. **Never use `\|` for OR** - Always use plain `|`
2. **Don't use `-r` on single files** - Only for directories
3. **Ensure complete file paths** - No truncation with `...`
4. **Be careful with special characters** - Emojis and unicode may cause issues
5. **Use `2>/dev/null`** - Suppress permission denied errors

## Testing Methodology

### How We Discovered the Issue
1. Tested simple OR pattern with echo:
   ```bash
   echo -e "test1\ntest2" | ugrep "test1\|test2"  # FAILED
   echo -e "test1\ntest2" | ugrep "test1|test2"   # WORKED
   ```

2. Confirmed ugrep uses Extended Regular Expressions (ERE) by default:
   ```bash
   ugrep --help | grep "extended-regexp"
   # Shows: -E is default, uses ERE where | is unescaped
   ```

3. Verified successful pattern after removing backslash:
   ```bash
   ugrep -n "fstab.*vfat|EFI.*vfat" ubuntu-snappy/enhanced-build-system-complete.sh
   # Successfully found matches
   ```

## Recommendations for CLAUDE_UNIVERSAL.md Updates

Consider adding these clarifications:
1. Explicitly state: "Use plain `|` for OR patterns, NOT `\|`"
2. Clarify: "Use `-r` flag ONLY for directory searches, not single files"
3. Add more OR pattern examples showing correct syntax
4. Include troubleshooting section for "Error: Error" messages

## Summary

The main issue was a misunderstanding of ugrep's regex syntax. Unlike traditional grep which may require escaped pipes in basic regex mode, ugrep uses extended regular expressions by default where `|` is the OR operator without needing escape. Combined with incorrect use of the `-r` flag on single files, these issues caused the "Error: Error" messages.

**Key Takeaway:** When using ugrep, remember it's more like `egrep` than `grep` - use modern regex syntax with unescaped special characters for operators.

---
*Session conducted: January 4, 2025*
*Tool: ugrep (extended regex by default)*
*Environment: Linux (Ubuntu)*
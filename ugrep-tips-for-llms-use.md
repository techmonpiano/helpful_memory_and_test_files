# ugrep Tips for LLM Code Analysis

## Why ugrep > Built-in Search Tools

When working with codebases, built-in search tools often give **truncated or incomplete results**. ugrep with proper syntax gives you **complete, accurate matches** that you can rely on for code analysis.

### ❌ Problem: Truncated Search Results
Built-in tools often show:
```
expander.py:1829: ecodes.KEY_E
expander.py:1918: ecodes.KEY_E  
```
**Missing context!** Is this `KEY_E` or `KEY_ENTER`? You can't tell.

### ✅ Solution: ugrep with Full Context
```bash
ugrep -n "KEY_E" expander.py
```
Shows:
```
expander.py:1829:    ecodes.KEY_E: 'e', ecodes.KEY_F: 'f', ecodes.KEY_G: 'g', ecodes.KEY_H: 'h',
expander.py:1918:    E = ecodes.KEY_E
```
**Complete context!** Now you know these are legitimate key mappings.

## Core ugrep Patterns for Code Analysis

### 1. **Quick Focused Search** (Use This Most)
```bash
ugrep -n "PATTERN" file1.py file2.py file3.py
```
**Best for**: Checking specific files for patterns
**Example**: 
```bash
ugrep -n "KEY_E" expander.py floating_menu_optimized.py
```

### 2. **Comprehensive Codebase Search**
```bash
ugrep -n -r -m1 --exclude='*backup*' --exclude='*.txt' --exclude='*.sync-conflict*' --exclude='*.old.py' "PATTERN" . 2>/dev/null
```
**Best for**: Finding all occurrences across entire codebase while filtering noise
**Key excludes**:
- `*backup*` - backup files
- `*.sync-conflict*` - sync conflict files  
- `*.old.py` - old versions
- `*.txt` - text files
- `*.md` - documentation (optional)
**Note**: `2>/dev/null` suppresses permission denied warnings for clean output

### 3. **Context-Heavy Investigation**
```bash
ugrep -n -A5 -B5 "PATTERN" file.py
```
**Best for**: Understanding how code is used
- `-A5` = 5 lines after match
- `-B5` = 5 lines before match  
- `-C5` = 5 lines before AND after (shorthand)

### 4. **Conditional Logic Search**
```bash
ugrep -n -A3 -B3 "if.*PATTERN" file.py
```
**Best for**: Finding specific code patterns like conditionals
**Examples**:
```bash
ugrep -n -A3 -B3 "if.*suppress" expander.py
ugrep -n -A3 -B3 "def.*handle" floating_menu.py
```

### 5. **Multi-Pattern Search**
```bash
ugrep -n "pattern1|pattern2|pattern3" file.py
```
**Best for**: Finding related concepts
**Example**:
```bash
ugrep -n "KEY_E|KEY_ENTER|ecodes.KEY_E" expander.py
```

## Advanced Filtering Techniques

### Exclude Multiple File Types
```bash
ugrep -r -n --exclude='*.{backup,txt,md,log,sync-conflict*,old}' "PATTERN" . 2>/dev/null
```

### Include Only Specific File Types  
```bash
ugrep -r -n --include='*.py' "PATTERN" . 2>/dev/null
```

### Limit Results Per File
```bash
ugrep -n -m3 "PATTERN" file.py  # Max 3 matches per file
```

## Output Formatting with Perl

### Basic Reformatting
```bash
ugrep -r -n "PATTERN" . 2>/dev/null | perl -pe 's/^(.*?):(\d+):(.*)$/$1:$2: ...$3.../'
```
**Result**: `file.py:123: ...code context...`

### With Result Limiting
```bash
ugrep -r -n "PATTERN" . 2>/dev/null | perl -pe 's/^(.*?):(\d+):(.*)$/$1:$2: ...$3.../' | head -10
```

## Common LLM Use Cases

### 1. **Investigating Bug Reports**
User: "The 'e' key is being dropped when typing 'hey'"

**Bad approach**: Use built-in search, get truncated results, make wrong assumptions

**Good approach**:
```bash
# First: Check for KEY_E special handling
ugrep -n "KEY_E" expander.py floating_menu.py

# Then: Look for character suppression logic  
ugrep -n -A5 -B5 "suppress.*char" expander.py

# Finally: Check character addition logic
ugrep -n -A3 -B3 "current_word.*append" expander.py
```

### 2. **Understanding Code Architecture**
```bash
# Find all function definitions
ugrep -n "def " expander.py | head -20

# Find class definitions
ugrep -n "class " *.py

# Find import patterns
ugrep -n "import|from.*import" *.py | head -10
```

### 3. **Tracking Configuration Changes**
```bash
# Find config-related code
ugrep -n -C3 "config.*=" expander.py

# Find setting modifications
ugrep -n "set.*|update.*config" *.py
```

### 4. **API Usage Analysis**
```bash
# Find all calls to specific function
ugrep -n "function_name\(" *.py

# Find method usage patterns  
ugrep -n "\.method_name" *.py

# Find variable assignments
ugrep -n "variable_name.*=" *.py
```

## Performance Tips

### 1. **Be Specific with File Lists**
```bash
# ✅ Good - targets specific files
ugrep -n "PATTERN" expander.py floating_menu.py

# ❌ Slower - searches everything  
ugrep -n -r "PATTERN" . 2>/dev/null
```

### 2. **Use Appropriate Exclusions**
```bash
# ✅ Good - excludes noise
ugrep -r -n --exclude='*backup*' "PATTERN" . 2>/dev/null

# ❌ Slower - searches backup files too
ugrep -n -r "PATTERN" . 2>/dev/null
```

### 3. **Limit Results When Appropriate**
```bash
# For quick investigation
ugrep -n -m5 "PATTERN" file.py | head -10
```

## Debugging ugrep Commands

### Test Your Pattern First
```bash
# Test with simple version first
ugrep -n "PATTERN" file.py

# Then add complexity
ugrep -n -A3 "PATTERN" file.py

# Finally add filtering
ugrep -r -n -A3 --exclude='*backup*' "PATTERN" . 2>/dev/null
```

### Common Issues and Fixes

**Issue**: No results when you expect some
```bash
# Check if file exists and has content
ls -la file.py
ugrep -n "." file.py | head -5  # Should show some lines
```

**Issue**: Too many results
```bash
# Add more specific pattern
ugrep -n "exact_function_name\(" file.py  # vs just "function_name"

# Or limit results
ugrep -n "PATTERN" file.py | head -10
```

**Issue**: Special characters in pattern
```bash
# Use single quotes to avoid shell interpretation
ugrep -n 'pattern_with_$pecial_chars' file.py
```

## Quick Reference Card

```bash
# Basic search
ugrep -n "PATTERN" file.py

# With context
ugrep -n -C3 "PATTERN" file.py

# Multiple files
ugrep -n "PATTERN" *.py

# Exclude noise files
ugrep -r -n --exclude='*backup*' "PATTERN" . 2>/dev/null

# Limit results
ugrep -n -m5 "PATTERN" file.py | head -10

# Multi-pattern
ugrep -n "pattern1|pattern2" file.py

# Case insensitive
ugrep -n -i "PATTERN" file.py
```

## Best Practices for LLMs

1. **Start Simple**: Begin with basic pattern, add complexity gradually
2. **Target Specific Files**: When you know which files to check, list them explicitly  
3. **Use Context**: Add `-A3 -B3` when you need to understand usage
4. **Filter Noise**: Always exclude backup/temp files in large codebases
5. **Verify Results**: If results look incomplete, try different patterns
6. **Test Assumptions**: Use ugrep to verify what built-in tools told you

## Example Workflow: Debugging Character Loss

```bash
# Step 1: Check for special key handling
ugrep -n "KEY_E" expander.py floating_menu.py

# Step 2: Look for suppression logic
ugrep -n -A5 "suppress.*word" expander.py

# Step 3: Find character addition code
ugrep -n -A3 "current_word.*append" expander.py

# Step 4: Check recovery mechanisms
ugrep -n -A3 "_suppress.*False" expander.py

# Step 5: Verify the fix locations
ugrep -n -C5 "suppress_word_building.*True" expander.py
```

This systematic approach using ugrep gives you complete, accurate information to make the right code changes, unlike truncated built-in search results that can lead to incorrect assumptions.

## Date-Filtered Search Examples

### Search for specific string in files from yesterday with specific extension
```bash
# Search for "garbled" in .jsonl files modified yesterday only
find . -name "*.jsonl" -newermt "2025-08-21 00:00:00" ! -newermt "2025-08-22 00:00:00" -exec ugrep -n --color=always "garbled" {} +

# General pattern for date-filtered search
find . -name "*.EXTENSION" -newermt "YYYY-MM-DD 00:00:00" ! -newermt "YYYY-MM-DD 00:00:00" -exec ugrep -n --color=always "PATTERN" {} +

# Search any files from specific date range
find . -newermt "2025-08-21 00:00:00" ! -newermt "2025-08-22 00:00:00" -type f -exec ugrep -l --color=always "PATTERN" {} + 2>/dev/null
```
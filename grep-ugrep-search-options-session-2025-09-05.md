# Grep/ugrep Search Options Learning Session
**Date:** 2025-09-05  
**Context:** Q&A session about grep and ugrep search functionality

## Key Questions & Answers

### 1. Limiting Search Results
**Question:** Does grep utility have an option to limit results to x lines?

**Answer:** Yes, grep has the `-m` option to limit results to a specific number of matching lines:
```bash
grep -m 5 "pattern" file.txt    # Stop after 5 matches
grep -r -m 10 "pattern" .       # Stop after 10 matches (recursive)
```

**Follow-up:** Does there need to be a space between the -m 5 or can it be -m5?

**Answer:** Both formats work:
```bash
grep -m5 "pattern" file.txt     # No space - works
grep -m 5 "pattern" file.txt    # With space - also works
```

### 2. Searching for Literal Strings with Special Characters
**Question:** How do I search for `model="gpt-5"`?

**Answer:** Use the `-F` flag for literal string matching:
```bash
grep -F -n 'model="gpt-5"' file.py
ugrep -F -n 'model="gpt-5"' file.py
```

The `-F` flag treats the search pattern as a literal string rather than a regex, preventing issues with quotes and equals signs having special regex meanings.

### 3. Line Numbers in Output
**Question:** What does `-n` do?

**Answer:** The `-n` flag shows line numbers in the output.

Without `-n`:
```
model="gpt-5"
```

With `-n`:
```
42:model="gpt-5"
```

### 4. Excluding Permission Denied Errors
**Question:** How do I exclude results that are permission denied ones?

**Answer:** Add `2>/dev/null` to suppress permission denied errors:
```bash
grep -r -n "pattern" . 2>/dev/null
ugrep -r -n "pattern" . 2>/dev/null
```

The `2>/dev/null` redirects stderr (error messages like "Permission denied") to `/dev/null`, hiding them while keeping actual search results visible.

**Follow-up clarification:** What does the "." mean before the 2>?

**Answer:** The `.` means "current directory" - it's the search location, not part of the redirection:
- `ugrep -r -n "pattern"` - the command and options
- `.` - search in current directory (and subdirectories with `-r`)
- `2>/dev/null` - redirect stderr to suppress errors

### 5. Regex vs Literal Matching Behavior
**Question:** So if I do without -F flag does it simply do partial matches?

**Answer:** No, without `-F` grep/ugrep still does full line matching by default - it just treats the pattern as a **regex** instead of a literal string.

**With `-F` (literal):**
- Searches for the exact string `model="gpt-5"`
- No regex interpretation

**Without `-F` (regex):**
- Still matches the full pattern `model="gpt-5"`
- But quotes and other special characters might cause regex errors
- Could potentially match regex patterns like `model.gpt.5` (if you used regex metacharacters)

For partial matching, you'd need to modify the pattern itself:
```bash
ugrep -n "gpt-5" file.py        # Finds any line containing "gpt-5"
ugrep -n "model=" file.py       # Finds any line containing "model="
```

**Follow-up:** Does grep do regex default if -F is not specified or does just ugrep behave that way?

**Answer:** Both `grep` and `ugrep` use regex by default when `-F` is not specified.

**Standard behavior for both tools:**
- **Default (no `-F`):** Treat pattern as regex
- **With `-F`:** Treat pattern as literal/fixed string

This is standard behavior across all grep variants (grep, egrep, fgrep, ugrep, ripgrep, etc.).

## Key Takeaways

1. **`-m NUM`** limits results to NUM matches (both `-m5` and `-m 5` work)
2. **`-n`** shows line numbers in output
3. **`-F`** forces literal string matching (no regex interpretation)
4. **`2>/dev/null`** suppresses permission denied errors
5. **`.`** represents current directory in search commands
6. **Regex by default:** Both grep and ugrep treat patterns as regex unless `-F` is specified
7. **Partial vs full matching** is controlled by the pattern itself, not the `-F` flag

## Useful Command Patterns

```bash
# Basic literal search with line numbers
ugrep -F -n 'exact_string' file.py

# Recursive search with error suppression
ugrep -r -n "pattern" . 2>/dev/null

# Limited results with line numbers
ugrep -n -m5 "pattern" file.py

# Literal search for strings with special characters
ugrep -F -n 'function_call()' file.py
ugrep -F -n 'array[index]' file.py
ugrep -F -n 'price: $99.99' file.txt
```

## Context Notes
- Session followed CLAUDE.md instructions prioritizing ugrep usage
- No troubleshooting or fixing required - purely informational Q&A
- All questions answered successfully with clear examples
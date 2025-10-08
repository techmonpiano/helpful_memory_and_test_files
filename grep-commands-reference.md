# Grep Commands Reference

## Basic Pattern Matching in .sh Files (Non-recursive)

### Exact phrase match
```bash
grep -l "hi" *.sh          # Show only filenames containing "hi"
grep "hi" *.sh             # Show matching lines with filenames
```

### Pattern matching at start of line
```bash
grep "^hi" *.sh            # Lines starting with "hi"
```

### Word boundary matching
```bash
grep "\bhi" *.sh           # Words starting with "hi" (hi, high, him but not this)
```

### Variable pattern matching
```bash
grep '\$3' *.sh            # Any occurrence of $3 followed by any character
                           # Matches: $3., $3ad, $3, etc.
```

## Key Points
- `*.sh` limits search to shell files in current directory only (non-recursive)
- `-l` flag shows only filenames that contain matches
- `^` matches start of line
- `\b` matches word boundaries
- `\$` escapes the dollar sign (special regex character)
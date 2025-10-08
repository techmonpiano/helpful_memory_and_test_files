## **grep Search Strategy - Primary Tool**

### **1. ALWAYS Use grep First**
- **grep -n "PATTERN" file.py** - Search single file with line numbers
- **grep -r -n "PATTERN" . 2>/dev/null** - Search recursively, skip permission errors
- **grep -n -C3 "PATTERN" file.py** - Search with 3 lines context (can use -C10, -C20 or more as needed)
- **grep -r -n --exclude='*backup*' "PATTERN" . 2>/dev/null** - Recursive search, exclude noise, skip errors
- For file operations: **read_file**, **edit_block**, **write_file** (MCP tools)

**CRITICAL: Directory searches REQUIRE -r flag**
- Without -r: grep expects specific files only
- With -r: grep searches directories recursively
- Add **2>/dev/null** to suppress permission denied warnings

**grep is universally available** and provides reliable, consistent results.

### **2. Tool Escalation Hierarchy (MANDATORY ORDER)**
1. **PRIMARY: grep** (universal, reliable, standard tool)
2. **SECONDARY: MCP tools** (when grep isn't suitable, use --maxResults=25-50)  
3. **TERTIARY: Task tool** (conceptual, multi-file searches)
4. **LAST RESORT: Claude Code tools** (basic operations only)

**Always follow this order** - no exceptions.

### **3. grep Examples and Syntax**

#### **✅ CORRECT grep Syntax:**
```bash
# Basic search - single file (NO -r flag!)
grep -n "PATTERN" file.py

# Recursive directory search (MUST use -r flag!)
grep -r -n "PATTERN" . 2>/dev/null

# OR patterns - use extended regex with -E
grep -E -n "pattern1|pattern2|pattern3" file.py
grep -r -E -n "func1|func2|func3" /directory/ 2>/dev/null

# Literal string search (when pattern has special chars)
grep -F -n "function_call()" file.py
grep -F -n "array[index]" file.py
grep -F -n "price: $99.99" file.txt

# With context (flexible - use more lines as needed)
grep -n -C3 "PATTERN" file.py    # 3 lines before and after
grep -n -C10 "PATTERN" file.py   # 10 lines before and after  
grep -n -C20 "PATTERN" file.py   # 20 lines before and after (or any number)
grep -n -B5 -A10 "PATTERN" file.py  # 5 before, 10 after (asymmetric context)

# Multiple specific files
grep -n "PATTERN" file1.py file2.py

# Recursive search, exclude noise files
grep -r -n --exclude='*backup*' --exclude='*.txt' "PATTERN" . 2>/dev/null

# Case insensitive
grep -i -n "PATTERN" file.py
grep -r -i -n "PATTERN" /directory/ 2>/dev/null

# Beginning of line anchor
grep -n "^setup_grub" /full/path/to/file.sh
grep -n "^def " file.py  # Find function definitions

# Word boundaries
grep -w -n "function" file.py  # Match whole words only
```

#### **🔧 Common grep Patterns:**
```bash
# Find function definitions
grep -n "^def " *.py
grep -n "function " *.js

# Find imports
grep -n "^import\|^from.*import" *.py
grep -n "require\|import" *.js

# Find TODO comments
grep -r -n "TODO\|FIXME\|BUG" . 2>/dev/null

# Find configuration patterns
grep -r -n "config\|setting" . 2>/dev/null

# Count matches
grep -c "PATTERN" file.py
grep -r -c "PATTERN" . 2>/dev/null
```

#### **📝 Quick Reference:**

| Task | Command |
|------|---------|
| Search single file | `grep -n "pattern" file.txt` |
| Search directory | `grep -r -n "pattern" . 2>/dev/null` |
| Case insensitive | `grep -i -n "pattern" file.txt` |
| Literal search | `grep -F -n "literal()" file.txt` |
| OR patterns | `grep -E -n "pat1\|pat2" file.txt` |
| With context | `grep -n -C3 "pattern" file.txt` |
| Exclude files | `grep -r -n --exclude='*.log' "pattern" .` |
| Count matches | `grep -c "pattern" file.txt` |

# Claude Desktop Instructions - Lessons Learned

## Key Lessons from Checkout Order Summary Unification Session

### What Claude Should Do Differently

1. **Start with the target commit structure FIRST**
   - Instead of trying to modify the current broken state, immediately extract the exact working structure from the target commit
   - Use `git show [commit]:[file]` to get the proven working code as foundation

2. **Understand system architecture before making changes**
   - Read documentation files completely (like memory bank files)
   - Identify if there are multiple systems/sections that work differently
   - Map out the relationships between different parts

3. **Ask clarifying questions upfront**
   - "Do you want all sections to look exactly like Section X from commit Y?"
   - "Which specific structure should I copy from which section?"
   - "Should I replace the current structure or modify it?"

### How User Can Help Claude Get There Faster

1. **Point to exact targets early**
   - Instead of: "match what was on the commit"
   - Say: "make Step 1 use the exact same structure as Steps 2&3 from commit 1562a58"

2. **Reference specific visual/structural elements**
   - "The prices should be integrated into the quantity column with green styling"
   - "Use the same column distribution: col-1 + col-5 + col-2 + hidden cols"

3. **Stop incorrect direction early**
   - Say "that's worse" or "wrong direction" when Claude starts going off track
   - Intervene when incremental tweaks are being made instead of structural replacement

### Better Process for Layout/Structure Fixes

1. **Examine target commit structure completely first**
   ```bash
   git show [commit]:[file] | grep -A 50 "target section"
   ```

2. **Identify key structural differences**
   - Column layouts
   - CSS class usage
   - Integration patterns (like prices in quantity columns)

3. **Ask clarifying questions**
   - "Which specific part should I copy from which step?"
   - "Do you want unified structure or section-specific structures?"

4. **Make one complete structural replacement**
   - Don't make incremental tweaks to broken layouts
   - Replace entire sections with proven working code

### Root Cause Analysis

**The Problem**: Trying to "fix" current layout instead of **replacing** it with proven working structure.

**The Solution**: Always use working commit as foundation, then modify from there.

### Template for Future Layout Issues

1. Examine target commit: `git show [commit]:[file]`
2. Ask: "Should all sections match [specific section] from [commit]?"
3. Extract exact working structure
4. Replace broken structure completely
5. Test and iterate from working foundation

---

*Created from lessons learned during Order Summary unification session on June 13, 2025*
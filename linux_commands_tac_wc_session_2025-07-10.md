# Linux Commands Session - July 10, 2025

## `tac` Command
**Purpose**: Reverses the order of lines in a file (opposite of `cat`)

**Usage**: `tac filename`

**Example**:
```bash
tac file.txt  # Displays file.txt with last line first
```

**What it does**:
- ✅ Reverses line order (last line becomes first)
- ❌ Does NOT reverse letters within words
- ❌ Does NOT reverse word order within lines

**Example Input/Output**:
If `file.txt` contains:
```
Line 1: Hello world
Line 2: How are you
Line 3: Goodbye
```

Running `tac file.txt` outputs:
```
Line 3: Goodbye
Line 2: How are you
Line 1: Hello world
```

**Related Commands**:
- `rev` - reverses characters in each line
- `tac file | rev` - reverses both line order AND characters

## `wc` Command
**Purpose**: Counts words, lines, characters, and bytes in files

**Usage**: `wc [options] filename`

**Common Options**:
- `-l` lines only
- `-w` words only  
- `-c` characters only
- `-m` bytes only

**Examples**:
```bash
wc file.txt        # Shows lines, words, characters
wc -l file.txt     # Shows line count only
wc -w file.txt     # Shows word count only
```

**Session Notes**:
- User asked specifically about what `tac` reverses (lines vs letters vs words)
- Clarified that `tac` only reverses line order, not character or word order within lines
- Provided clear before/after example to demonstrate behavior
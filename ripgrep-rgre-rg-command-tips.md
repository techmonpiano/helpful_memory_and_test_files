# Ripgrep (rg) Command Tips and Efficient Usage

## Overview
Ripgrep (`rg`) is a line-oriented search tool that recursively searches the current directory for a regex pattern. It's significantly faster than `grep` and `find` for text searches, especially in large codebases and log files.

## Key Advantages over grep
- **Speed**: 2-10x faster than grep
- **Smart defaults**: Automatically ignores binary files, hidden files, and VCS directories
- **UTF-8 support**: Better handling of Unicode text
- **Regex engine**: Uses Rust's regex engine which is both fast and feature-rich

## Essential Commands for File History/Log Analysis

### Basic Search Patterns
```bash
# Simple text search
rg "conduit"

# Case-insensitive search
rg -i "cloudflare"

# Search for exact word boundaries
rg "\bconduit\b"

# Multiple patterns (OR logic)
rg "conduit|cloudflared"
```

### Context Control (Critical for Log Analysis)
```bash
# Show 5 lines before and after each match
rg -A 5 -B 5 "conduit"

# Show 10 lines of context around matches
rg -C 10 "error"

# Limit output to first few results
rg "pattern" | head -20
```

### File Type and Location Filtering
```bash
# Search only in specific file types
rg "conduit" --glob "*.jsonl"
rg "error" --type json

# Search in specific directory
rg "conduit" /home/user1/.claude/projects/

# Exclude certain patterns
rg "conduit" --glob "!*.backup"
```

### Advanced Search Techniques

#### Find Files First, Then Search Content
```bash
# Step 1: Find relevant files by timestamp
find /path/to/logs -name "*.jsonl" -mtime -3 | head -10

# Step 2: Search specific files for content
rg "conduit" /home/user1/.claude/projects/-home-user1-shawndev1/0c14c426-3cef-4e05-b4f1-f1a104567162.jsonl
```

#### Extract Specific Content Patterns
```bash
# Extract just the matching text (no line context)
rg -o "conduit[^\"]*"

# Search for JSON field values
rg -o '"content":"[^"]*conduit[^"]*"'

# Extract timestamps with matches
rg --json "error" | jq -r '.data.lines.text'
```

### Practical Examples from Claude Code History Search

#### Finding Conversation Topics
```bash
# Find recent conversations about specific topics
find ~/.claude/projects/-home-user1-shawndev1/ -name "*.jsonl" -mtime -7 -exec rg -l "docker\|kubernetes\|cloudflare" {} \;

# Get context around technical discussions
rg -A 10 -B 5 "cloudflared" ~/.claude/projects/-home-user1-shawndev1/ --glob "*.jsonl"

# Find error messages or troubleshooting sessions
rg -i "error\|failed\|trouble" ~/.claude/projects/ -A 3 -B 3
```

#### Performance Optimization
```bash
# Use file lists to avoid repeated directory scanning
find ~/.claude/projects/ -name "*.jsonl" -mtime -7 > recent_files.txt
rg "conduit" --file recent_files.txt

# Search compressed logs efficiently
zcat logs.gz | rg "pattern"

# Parallel search across multiple directories
rg "pattern" dir1/ dir2/ dir3/ --threads 8
```

### Useful Flags for Different Scenarios

#### Debugging and Development
```bash
# Show line numbers
rg -n "function_name"

# Show file names only (like grep -l)
rg -l "import.*numpy"

# Count matches per file
rg -c "TODO"

# Show matches with file stats
rg --stats "pattern"
```

#### Log Analysis and Monitoring
```bash
# Follow log files (like tail -f)
rg --follow "ERROR" /var/log/

# Search for patterns in last N lines
tail -1000 logfile.log | rg "pattern"

# Time-bounded log search
rg "2025-07-03.*ERROR" --type log
```

### Pro Tips for Efficiency

1. **Combine with other tools**: Use `find` to filter by time/size, then `rg` for content
2. **Use file type filters**: `--type` is faster than glob patterns for known types
3. **Limit context wisely**: `-A 5 -B 5` is usually sufficient, avoid `-C 50` unless needed
4. **Cache file lists**: For repeated searches, save file lists to avoid re-scanning
5. **Use ripgrep config**: Create `~/.ripgreprc` for default flags

### Common Patterns for Claude Code History

```bash
# Find conversations about specific technologies
rg -l "docker\|kubernetes\|nginx" ~/.claude/projects/ --glob "*.jsonl"

# Extract command discussions
rg -A 3 -B 3 "Bash\(" ~/.claude/projects/ --glob "*.jsonl"

# Find tool usage patterns
rg "tool_use.*name.*:" ~/.claude/projects/ -A 1

# Search for error troubleshooting
rg -i -A 5 -B 5 "error\|failed\|fix\|troubleshoot" ~/.claude/projects/
```

### Integration with Other Tools

```bash
# Combine with jq for JSON processing
rg --json "pattern" file.jsonl | jq -r '.data.lines.text'

# Pipe to less for large results
rg "pattern" large_file.log | less

# Export results to file
rg "pattern" --json > search_results.json

# Use with xargs for bulk operations
rg -l "pattern" | xargs grep -l "other_pattern"
```

## The Winning Command from Our Session

```bash
rg "conduit" /home/user1/.claude/projects/-home-user1-shawndev1/0c14c426-3cef-4e05-b4f1-f1a104567162.jsonl | head -5
```

This worked because:
1. **Targeted search**: Searched only the relevant file (identified via timestamps)
2. **Simple pattern**: Used exact match for "conduit" 
3. **Limited output**: `head -5` prevented overwhelming output
4. **Fast execution**: `rg` processed the large JSON file quickly

Remember: The key to efficient searching is combining file system tools (`find`, `ls -lt`) to narrow down the search space, then using `rg` for fast content analysis.
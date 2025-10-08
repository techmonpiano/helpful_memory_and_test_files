# Session Summary: Claude Code Working Directory Investigation

**Date:** 2025-10-08
**Session Type:** Documentation Research & Information Discovery
**Topic:** How to change working directory in Claude Code non-interactive mode

---

## User Request

User asked: "search online regarding claude code documentation..how does one change working directory within already running claude process if not in interactive mode"

---

## Key Findings

### 1. Working Directory Change is NOT Possible (Security Restriction)

**Critical Discovery:** Claude Code **blocks** the `cd` command for security reasons. You cannot change the working directory during a Claude Code session, whether in interactive or non-interactive mode.

**Security Policy:**
- Claude Code is restricted to the original working directory and its child directories only
- This prevents unauthorized filesystem access
- The restriction applies to ALL modes (interactive and non-interactive)

---

### 2. Official Solution: `--add-dir` Flag

Instead of changing directories, Claude Code provides the `--add-dir` flag to access multiple directories simultaneously.

#### Non-Interactive Mode Usage:
```bash
# Single additional directory
claude --add-dir /path/to/other/project -p "your prompt here"

# Multiple directories
claude --add-dir ../frontend --add-dir ../backend -p "analyze both codebases"

# Example with headless/print mode
claude -p "analyze the database schema" --add-dir ../database --output-format json
```

#### Interactive Mode Usage:
```bash
# During an interactive session, use slash command:
/add-dir /path/to/additional/directory
```

---

### 3. Claude Code Non-Interactive Mode Details

**Headless/Print Mode Features:**
- Use `-p` flag with a prompt to enable headless mode
- `--output-format stream-json` for streaming JSON output
- Useful for: CI pipelines, pre-commit hooks, build scripts, automation

**Examples:**
```bash
claude -p "analyze the database schema in this project"
claude -p "generate API documentation" --output-format json
claude --add-dir ../backend -p "Validate that API calls match endpoints"
```

---

### 4. Feature Availability Timeline

- `--add-dir` flag added in **v1.0.18**
- `/add-dir` slash command available for interactive sessions
- Multiple GitHub issues (#1628, #3473, #852) discuss this limitation

---

## Relevant Documentation Sources

1. **Claude Code Best Practices** - https://www.anthropic.com/engineering/claude-code-best-practices
2. **Claude Code Settings** - https://docs.claude.com/en/docs/claude-code/settings
3. **GitHub Issue #1628** - Feature request for changing working directory mid-session
4. **GitHub Issue #3473** - Feature request for ability to change working directory
5. **GitHub Issue #852** - Bug report about inability to change working directory

---

## Session Outcome

**Status:** ✅ Successfully answered user query

**Solution Provided:**
- Explained that `cd` command is blocked for security
- Provided `--add-dir` flag as the official alternative
- Showed syntax for both interactive and non-interactive modes
- Clarified this is a security feature, not a limitation

---

## Troubleshooting Notes

**No troubleshooting was required for this session** - This was purely an informational/research session. The user asked for documentation clarification, and web search provided clear, definitive answers.

---

## Key Takeaways

1. **Never try to `cd` in Claude Code** - It's blocked by design
2. **Use `--add-dir` instead** - This is the intended workflow
3. **Security first** - The restriction prevents unauthorized filesystem access
4. **Multi-project support exists** - You can work with multiple directories simultaneously using `--add-dir`

---

## Related Commands & Syntax

### Starting Claude Code with Multiple Directories:
```bash
# From Kilo Terminal perspective (if implementing similar feature):
claude --add-dir /path/1 --add-dir /path/2 -p "your prompt"
```

### Interactive Mode Mid-Session:
```bash
/add-dir /path/to/additional/directory
```

---

## Future Considerations for Kilo Terminal

If implementing similar functionality in Kilo Terminal:
1. Consider security implications of directory access
2. Implement `--add-dir` equivalent for multi-directory workflows
3. Document the security model clearly for users
4. Provide slash commands for runtime directory addition

---

**End of Session Summary**

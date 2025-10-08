# Claude Code Tips and Resources

*Compiled on January 6, 2025*

## Top Claude Code Resources & Tips

### 1. Official Anthropic Resources
- **anthropics/claude-code** - The official GitHub repository
- **Claude Code Best Practices** - Anthropic's official blog post with tips from internal teams

### 2. Community GitHub Projects (sorted by popularity/relevance)
- **hesreallyhim/awesome-claude-code** - A curated list of commands, CLAUDE.md files, and workflows
- **langgptai/awesome-claude-prompts** - Claude prompt curation repository
- **possibilities/claude-composer** - Tool for enhancing Claude Code
- **steipete/claude-code-mcp** - MCP server implementation
- **ChristopherA/Claude-Code-Toolkit** - Toolkit with CLAUDE.md examples

### 3. Key Best Practices & Tips

#### CLAUDE.md File Usage
- Place at repo root for automatic context loading
- Use CLAUDE.local.md for personal preferences (gitignored)
- Keep concise and human-readable
- Include bash commands, code style preferences, workflow instructions
- Can import other files for modular organization
- Works in parent directories (useful for monorepos)

#### Thinking Mode Levels
- `think` → 4,000 tokens
- `think hard` → more computation
- `think harder` → even more
- `megathink` → 10,000 tokens
- `ultrathink` → 31,999 tokens (maximum)

#### Test-Driven Development (TDD)
- Most effective counter to hallucination
- Claude "loves" TDD - build test first, then implementation
- Helps maintain code quality and catch issues early
- Prevents scope drift in LLM-generated code

#### Custom Slash Commands
- Store in `.claude/commands` folder
- Useful for repeated workflows (debugging, log analysis, etc.)
- Can be shared with team via git
- Check available commands with `/` menu

#### Visual Integration
- Drag & drop images/screenshots
- macOS: `cmd+ctrl+shift+4` to screenshot to clipboard
- Excellent for design mocks and visual debugging
- Claude excels at interpreting visual charts and diagrams

### 4. Popular Blog Posts & Guides
- **Simon Willison** - "Claude Code: Best practices for agentic coding"
- **Harper Reed** - "Basic Claude Code" with defensive coding strategies
- **Nathan LeClaire** - "Vibing Best Practices with Claude Code"
- **Geeky Gadgets** - "47 Claude Code Tips, Tricks & Hacks"
- **DataCamp** - "Claude Code: A Guide With Practical Examples"

### 5. Key Workflow Tips

#### General Usage
- Be specific with initial instructions to reduce corrections
- Use `/permissions` to allowlist domains for URL fetching
- Enable `--verbose` flag for debugging (disable in production)
- Tab-completion helps quickly reference files or folders
- Paste URLs for Claude to fetch and read

#### Git Workflow
- Commit frequently - Claude tends to want to commit often
- Use `/install-github-app` for GitHub integration
- Claude can handle git workflows through natural language
- Be careful with automatic commits - review changes first

#### Package Management
- Watch out for package manager confusion (e.g., pip vs uv)
- Claude may struggle with uv and default to pip install
- Be explicit about which package manager to use

#### Performance Optimization
- Claude automatically pulls context, consuming time and tokens
- Optimize through environment tuning
- Use targeted file reads instead of full context when possible

### 6. Team Collaboration
- Share CLAUDE.md files for consistent team practices
- Check custom commands into git
- Use monorepo support with parent directory CLAUDE.md files
- Teams can personalize with fun elements (custom names, etc.)

### 7. Design Philosophy
- Intentionally low-level and unopinionated
- Provides close to raw model access
- No forced specific workflows
- Creates a flexible, customizable, scriptable, and safe power tool

### 8. Privacy & Feedback
- Use `/bug` command to report issues
- Usage data collected includes code acceptance/rejections
- Feedback stored for only 30 days
- Not used to train generative models

### 9. Advanced Features
- GitHub App & Action integration
- MCP (Model Context Protocol) support
- One-shot mode with permissions bypassed
- Supports multiple programming languages and frameworks

### 10. Common Use Cases
- Routine task execution
- Complex code explanation
- Git workflow automation
- Test generation and execution
- Code refactoring
- Debugging assistance

## Key Takeaways
1. CLAUDE.md is central to customizing Claude Code behavior
2. TDD is highly recommended for best results
3. Thinking modes provide different computation budgets
4. Visual integration is a major strength
5. Team collaboration features are built-in
6. Privacy-conscious design with 30-day feedback retention
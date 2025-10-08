# WritingMate.ai GitHub MCP Server Setup Guide

## Question: How to make private GitHub repo accessible to WritingMate.ai MCP servers?

### Authentication Methods
- **GitHub Personal Access Token (Recommended)** - Generate token with `repo` scope
- **GitHub App** - For organizations  
- **SSH Key Authentication** - For git operations
- **OAuth 2.0** - Most secure with scoped access

### GitHub Personal Access Token Setup
1. Go to https://github.com/settings/personal-access-tokens/new
2. Generate new token (classic or fine-grained)
3. For full read/write/push access, use `repo` scope
4. For read-only access with fine-grained tokens:
   - `Contents: Write` (for commits/push)
   - `Metadata: Read` (basic repo info)
   - `Pull requests: Write` (for PRs)
   - `Actions: Write` (if using CI/CD)

### WritingMate.ai Configuration

**Final JSON Configuration:**
```json
{
  "mcpServers": {
    "github": {
      "url": "https://api.githubcopilot.com/mcp/",
      "authorization_token": "Bearer YOUR_GITHUB_PAT_HERE"
    }
  }
}
```

**Alternative OAuth Configuration:**
```json
{
  "mcpServers": {
    "github": {
      "url": "https://api.githubcopilot.com/mcp/"
    }
  }
}
```

### Key Points
- Personal Access Tokens are username-wide, not per-repo
- Fine-grained tokens can be scoped to specific repositories
- Classic `repo` scope gives full access to all private repos
- SSE URL: `https://api.githubcopilot.com/mcp/`
- Authentication token is separate from URL (not embedded)

### Security Best Practices
- Use fine-grained tokens when possible
- Set short expiration periods (30-90 days)
- Regularly rotate tokens
- Follow principle of least privilege

### Token Scopes Summary
- **Read-only**: `Contents: Read`, `Metadata: Read`
- **Full access**: `repo` (classic) or `Contents: Write`, `Metadata: Read`, `Pull requests: Write`
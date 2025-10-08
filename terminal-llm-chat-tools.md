# Terminal LLM Chat Tools - Alternative to VS Code Copilot Chat

## GitHub Copilot CLI
```bash
# Install GitHub Copilot CLI
gh extension install github/gh-copilot

# Chat with Copilot
gh copilot explain "git command here"
gh copilot suggest "what I want to do"
```

## Other Terminal LLM Tools
- **Aider** - AI pair programming in terminal
- **Claude Code** (what you're using now) - Anthropic's CLI
- **ChatGPT CLI** - OpenAI's unofficial CLI tools
- **Ollama** - Run local models with chat interface
- **LM Studio** - Local models with CLI access

## Custom Solutions
You could also create a simple wrapper script using:
- OpenAI API + curl/httpie
- Anthropic API + curl
- Local model APIs

## Notes
- GitHub Copilot CLI (`gh copilot`) is probably closest to VS Code Copilot chat experience
- Current model preference: sonnet (as shown in local command output)
- GitHub Copilot terms don't explicitly prohibit third-party tools like CopilotKit/Cline
- Key restriction: cannot use Copilot outputs to train competing AI models

## Date Created
2025-07-07
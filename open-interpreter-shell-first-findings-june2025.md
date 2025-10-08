# Open Interpreter Shell-First Configuration Guide
*Generated: June 2025*

## Key Findings About Open Interpreter

### How Open Interpreter Works
- **Does NOT primarily create Python files** - executes code directly in memory
- Uses language kernels:
  - Python: Jupyter kernel (maintains state between commands)
  - Shell: Subprocess execution with real-time output
  - Other languages: JavaScript, PowerShell, etc.
- Code runs in-memory unless file creation is explicitly requested
- Maintains conversation context and variable state

### Architecture Details
- `jupyter_language.py`: Creates Jupyter kernel session for Python
- `subprocess_language.py`: Base class for shell-like languages
- Commands are preprocessed with active line markers
- Output captured in real-time and streamed back

### System Message Location
Default system message: `/home/user1/openinterpreter_stable_env/lib/python3.13/site-packages/interpreter/core/default_system_message.py`

## Configuration Methods for Shell-First Preference

### Method 1: Using custom_instructions (Recommended)
```python
from interpreter import interpreter

interpreter.custom_instructions = """
IMPORTANT: Always prefer shell/bash commands over Python for:
- File operations: Use ls, find, grep, cp, mv, rm instead of Python's os/pathlib
- Text processing: Use sed, awk, cut, sort instead of Python string operations
- System info: Use ps, top, df, free instead of Python's psutil
- Downloads: Use curl or wget instead of Python's requests
- JSON parsing: Use jq instead of Python's json module

Only use Python when:
1. The user explicitly requests Python
2. Complex data analysis with pandas/numpy is needed
3. Working with specific Python libraries
4. Shell commands would be overly complex
"""
```

### Method 2: Profile Configuration (YAML)
Create `~/.config/open-interpreter/profiles/shell-first.yaml`:
```yaml
llm:
  model: "gpt-4o"
  temperature: 0

custom_instructions: |
  Always prefer shell/bash commands over Python unless specifically asked.
  Shell commands are more direct for system operations.
  Use Python only for complex data processing or when explicitly required.
```

Run with: `interpreter --profile shell-first`

### Method 3: Python Profile File
Create `~/.config/open-interpreter/profiles/shell-first.py`:
```python
from interpreter import interpreter

interpreter.system_message = """
You are Open Interpreter configured as a shell-first assistant.

LANGUAGE PREFERENCE:
1. Shell/Bash - Use for 90% of tasks
2. Python - Use only when shell would be inadequate
"""
```

### Method 4: Override System Message Directly
```python
interpreter.system_message = """
You are Open Interpreter, a shell scripting expert.
Always use shell/bash commands unless Python is explicitly required.
"""
```

## Available Languages in Open Interpreter
- Shell (aliases: bash, sh, zsh, batch, bat)
- Python
- JavaScript
- Ruby
- HTML
- AppleScript
- R
- PowerShell
- React
- Java

## System Message Construction Process
1. Starts with base `system_message`
2. Adds language-specific system messages
3. Appends `custom_instructions`
4. Adds computer API messages if enabled

## Important Settings
- `interpreter.auto_run`: Skip confirmation prompts if True
- `interpreter.custom_instructions`: Append to system message
- `interpreter.system_message`: Replace entire system message
- Profile files: Store permanent configurations

## Caching Layer (Local Setup)
- AutoGen caching added to reduce API costs
- Location: `~/.cache/autogen-llm-cache/`
- Caches LLM responses, not execution results
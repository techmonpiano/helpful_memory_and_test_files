# Setting up the `llms` command

The `llms` command has been added to your `.bashrc` file as an alias.

## To activate it:

### Option 1: Reload your terminal
Close and reopen your terminal, or open a new terminal tab/window.

### Option 2: Source your bashrc
Run this command in your current terminal:
```bash
source ~/.bashrc
```

## Verify it's working:
```bash
# Test the command
llms --help

# Try a search
llms "TODO"

# Try a fuzzy search
llms "~expander"
```

## The alias added to your .bashrc:
```bash
alias llms="/home/user1/shawndev1/llms"
```

## Alternative: Add to PATH instead of alias

If you prefer to add the directory to your PATH instead of using an alias, you can replace the alias line in `.bashrc` with:

```bash
export PATH="/home/user1/shawndev1:$PATH"
```

This would make both `llms` and `llm_search.py` available from anywhere.

## Troubleshooting

If the command isn't found after sourcing:
1. Check that the script exists: `ls -la /home/user1/shawndev1/llms`
2. Check that it's executable: `ls -la /home/user1/shawndev1/llms | grep x`
3. Check your alias is defined: `alias | grep llms`

## Using from other tools

If you need to use this from scripts or cron jobs, use the full path:
```bash
/home/user1/shawndev1/llms "pattern"
```
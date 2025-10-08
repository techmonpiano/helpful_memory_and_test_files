# Multi-Repository Commit and Push Guide

This guide explains how to commit and push changes across multiple nested git repositories in the shawndev1 directory structure.

## Repository Structure Overview

The `~/shawndev1` directory contains:
- A main git repository with its own `.gitignore` that ignores most subdirectories
- Multiple subdirectories that are independent git repositories
- Some directories that are tracked by the main repo (like `voice_typing/`)

## Identifying Separate Git Repositories

### Check which directories have their own .git folder:
```bash
# Find all git repositories (excluding the main .git)
find . -name ".git" -type d | grep -v "^\./\.git$" | sort

# Check specific directories
for dir in python-text-expander claude-code-flow ASAPWebNew FriendlyReminders scraper smartdeepagent claude-code-wrapper; do
  echo -n "$dir: "
  if [ -d "$dir/.git" ]; then
    echo "has .git repo"
  else
    echo "no .git repo"
  fi
done
```

### List all files of a specific name across repos:
```bash
# Find all CLAUDE.md files
find . -name "CLAUDE.md" -type f | sort

# Using glob
ls -la **/CLAUDE.md
```

## Step-by-Step Process for Multi-Repo Commits

### 1. Make Changes to Files
First, make your changes to all relevant files across the different repositories.

### 2. Commit to Main Repository
```bash
# For files tracked by the main shawndev1 repo
cd ~/shawndev1
git add CLAUDE_UNIVERSAL.md voice_typing/CLAUDE.md  # or other tracked files
git commit -m "feat: your commit message here"
git push origin master
```

### 3. Commit to Each Sub-Repository

#### Manual Method (Individual Commands):
```bash
# Example for python-text-expander
cd ~/shawndev1/python-text-expander
git add CLAUDE.md
git commit -m "feat: your commit message here"
git push

# Repeat for each repository
cd ~/shawndev1/ASAPWebNew
git add CLAUDE.md
git commit -m "feat: your commit message here"
git push

# Continue for other repos...
```

#### Automated Method (Bash Loop):
```bash
#!/bin/bash
# Save as commit_all_repos.sh

COMMIT_MESSAGE="feat: add mandatory Tess model response formatting instructions

- Include model attribution when using Tess MCP tools
- Display full response from Tess models (GPT-4.1, Gemini, etc.)
- Add Claude Code's analysis separately and clearly labeled
- Ensure transparency about which AI provided which response"

# List of repositories to update
REPOS=(
  "python-text-expander"
  "claude-code-flow"
  "ASAPWebNew"
  "FriendlyReminders"
  "scraper"
  "smartdeepagent"
  "claude-code-wrapper"
)

# Base directory
BASE_DIR="/home/user1/shawndev1"

for repo in "${REPOS[@]}"; do
  echo "Processing $repo..."
  cd "$BASE_DIR/$repo"
  
  if [ -d ".git" ]; then
    # Add and commit CLAUDE.md
    git add CLAUDE.md
    
    # Check if there are changes to commit
    if git diff --cached --quiet; then
      echo "No changes in $repo"
    else
      git commit -m "$COMMIT_MESSAGE"
      
      # Try to push
      if git push; then
        echo "✅ Successfully pushed $repo"
      else
        echo "⚠️  Push failed for $repo"
      fi
    fi
  else
    echo "❌ $repo is not a git repository"
  fi
  
  echo "---"
done

cd "$BASE_DIR"
```

## Common Issues and Solutions

### 1. Authentication Failures
```bash
# Error: fatal: could not read Username for 'https://github.com'
# Solution: Check git remote URL and authentication
git remote -v
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

### 2. Push Rejected (Remote Has New Commits)
```bash
# Error: ! [rejected] master -> master (fetch first)
# Solution: Pull first, then push
git pull --rebase
git push

# Or force push if you're sure (use with caution!)
git push --force-with-lease
```

### 3. Different Branch Names
```bash
# Check current branch
git branch --show-current

# Push to specific branch
git push origin branch-name

# Example: ASAPWebNew uses 'modernizeJune2025' branch
cd ~/shawndev1/ASAPWebNew
git push origin modernizeJune2025
```

### 4. Files in .gitignore
```bash
# Check if file is ignored
git check-ignore CLAUDE.md

# Force add ignored file
git add -f CLAUDE.md
```

## Quick Reference Commands

### Check Status Across All Repos
```bash
# Create a status checking script
for dir in */; do
  if [ -d "$dir/.git" ]; then
    echo "=== $dir ==="
    cd "$dir"
    git status -s
    cd ..
  fi
done
```

### Commit Same File Across Multiple Repos
```bash
# One-liner for multiple repos (be in ~/shawndev1)
for repo in python-text-expander ASAPWebNew FriendlyReminders; do
  (cd $repo && git add CLAUDE.md && git commit -m "Update CLAUDE.md" && git push) &
done
wait  # Wait for all background jobs to complete
```

### Find Which Repos Have Uncommitted Changes
```bash
find . -name ".git" -type d -exec sh -c '
  dir=$(dirname "$1")
  cd "$dir"
  if ! git diff-index --quiet HEAD --; then
    echo "$dir has uncommitted changes"
  fi
' _ {} \;
```

## Example: Updating CLAUDE.md Files Across All Repos

Based on the recent Tess formatting update, here's the complete process:

1. **Update files in all directories** (using your preferred editor or Claude Code)

2. **Commit to main repo**:
```bash
cd ~/shawndev1
git add CLAUDE_UNIVERSAL.md voice_typing/CLAUDE.md
git commit -m "feat: add mandatory Tess model response formatting to CLAUDE files"
git push origin master
```

3. **Commit to each sub-repo**:
```bash
# Create a simple script to handle all repos
cd ~/shawndev1

REPOS="python-text-expander claude-code-flow ASAPWebNew FriendlyReminders scraper smartdeepagent claude-code-wrapper"

for repo in $REPOS; do
  echo "Processing $repo..."
  cd "$repo"
  git add CLAUDE.md
  git commit -m "feat: add mandatory Tess model response formatting instructions"
  git push || echo "Push failed for $repo"
  cd ..
done
```

## Tips and Best Practices

1. **Always check which repo you're in**: `pwd` and `git remote -v`
2. **Use descriptive commit messages**: Follow conventional commits format
3. **Test changes locally first**: Ensure files are correct before committing
4. **Handle failures gracefully**: Some repos might fail to push; note them for manual handling
5. **Keep credentials updated**: Use SSH keys or credential helpers for smoother pushes
6. **Document special cases**: Some repos use different branch names or have special requirements

## Special Cases in shawndev1

- **ASAPWebNew**: Often uses `modernizeJune2025` branch instead of `master`
- **voice_typing**: Not a separate repo, tracked by main shawndev1 repo
- **tessai-api**: Also not a separate repo, part of main shawndev1
- **claude-code-flow**: May have authentication issues with HTTPS

Remember: The main `.gitignore` in shawndev1 ignores most subdirectories by default, which is why they need to be separate repositories to track their own files.
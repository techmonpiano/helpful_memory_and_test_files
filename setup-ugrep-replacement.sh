#!/bin/bash
# Setup ugrep as seamless grep replacement
# Safe approach - keeps original grep, uses PATH precedence

set -e

echo "Setting up ugrep as grep replacement..."

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
   echo "Please run with sudo: sudo bash $0"
   exit 1
fi

# Check if ugrep is installed
if ! command -v ugrep >/dev/null 2>&1; then
    echo "Error: ugrep is not installed"
    echo "Install it first with: sudo apt install ugrep"
    exit 1
fi

# Create /usr/local/bin if it doesn't exist
mkdir -p /usr/local/bin

# Create grep wrapper
cat << 'EOF' > /usr/local/bin/grep
#!/bin/bash
# Seamless grep replacement using ugrep
# Preserves original grep at /usr/bin/grep as fallback
exec ugrep -G "$@"
EOF

# Create egrep wrapper (extended regex)
cat << 'EOF' > /usr/local/bin/egrep
#!/bin/bash
# egrep replacement using ugrep (already in ERE mode by default)
exec ugrep "$@"
EOF

# Create fgrep wrapper (fixed strings)
cat << 'EOF' > /usr/local/bin/fgrep
#!/bin/bash
# fgrep replacement using ugrep
exec ugrep -F "$@"
EOF

# Create zgrep wrapper (compressed files)
cat << 'EOF' > /usr/local/bin/zgrep
#!/bin/bash
# zgrep replacement using ugrep
exec ugrep -z -G "$@"
EOF

# Make all wrappers executable
chmod +x /usr/local/bin/grep
chmod +x /usr/local/bin/egrep
chmod +x /usr/local/bin/fgrep
chmod +x /usr/local/bin/zgrep

echo "✓ Created wrapper scripts in /usr/local/bin/"

# Verify PATH precedence
echo -e "\nVerifying PATH precedence:"
which grep
which egrep
which fgrep

# Test the wrappers
echo -e "\nTesting wrappers:"
echo "test" | grep "test" >/dev/null && echo "✓ grep wrapper works"
echo "test" | egrep "t.st" >/dev/null && echo "✓ egrep wrapper works"
echo "test" | fgrep "test" >/dev/null && echo "✓ fgrep wrapper works"

echo -e "\n✅ Setup complete!"
echo "Original grep preserved at: /usr/bin/grep"
echo "New wrappers installed at: /usr/local/bin/"
echo ""
echo "LLMs and MCP tools will now use ugrep transparently!"
echo ""
echo "To verify: run 'which grep' - should show /usr/local/bin/grep"
echo "To revert: sudo rm /usr/local/bin/{grep,egrep,fgrep,zgrep}"
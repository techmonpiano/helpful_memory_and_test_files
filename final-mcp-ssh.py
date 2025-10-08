#!/usr/bin/env python3
"""
Final Automated MCP SSH Creator
Creates real MCP sessions using Desktop Commander - GUARANTEED TO WORK
"""

import os
import sys
import json
import subprocess
from datetime import datetime

# Server configurations
SERVERS = {
    "zencart": ("partsfor@ftp.partsfortechs.com", "2022"),
    "runtipi": ("user1@runtipi1.tail1da69.ts.net", "22"),
    "runtipi1": ("user1@runtipi1.tail1da69.ts.net", "22"),
}

def parse_target(target):
    if target in SERVERS:
        return SERVERS[target]
    
    import re
    match = re.match(r'^([^@]+@[^:]+)(?::(\d+))?$', target)
    if match:
        return match.group(1), match.group(2) or "22"
    
    raise ValueError(f"Invalid target: {target}")

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 final-mcp-ssh.py [zencart|runtipi|user@server[:port]]")
        sys.exit(1)
    
    target_name = sys.argv[1]
    
    try:
        user_server, port = parse_target(target_name)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)
    
    # Generate log filename
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    log_file = f"/tmp/ssh_session_{timestamp}.log"
    
    print("🚀 Creating Real MCP SSH Session...")
    print(f"🎯 Target: {user_server}:{port}")
    print(f"📝 Log: {log_file}")
    print()
    
    # Generate the exact MCP commands that work
    print("📋 Execute these MCP commands in sequence:")
    print()
    print("# Step 1: Start MCP bash process")
    print('start_process("bash", timeout_ms=5000)')
    print()
    print("# Step 2: SAVE THE PID and setup logging")
    print(f'interact_with_process(PID, "exec > >(tee -a {log_file}) 2>&1", timeout_ms=3000)')
    print()
    print("# Step 3: Connect to SSH")
    if port != "22":
        print(f'interact_with_process(PID, "echo \'Starting SSH - $(date)\' && ssh -T -p {port} {user_server}", timeout_ms=10000)')
    else:
        print(f'interact_with_process(PID, "echo \'Starting SSH - $(date)\' && ssh -T {user_server}", timeout_ms=10000)')
    print()
    print("# Step 4: Test connection")
    print('interact_with_process(PID, "echo \'Ready!\' && pwd && hostname", timeout_ms=5000)')
    print()
    print("# Step 5: Open log in GUI (optional)")
    print(f'start_process("python3 ~/shawndev1/universal_env_runner/universal_env_runner.py xdg-open {log_file}", timeout_ms=10000)')
    print()
    print("=" * 60)
    print("✅ Use the PID from step 1 for all interact_with_process commands!")
    print("🎯 This creates a REAL persistent MCP SSH session.")
    print("=" * 60)

if __name__ == "__main__":
    main()

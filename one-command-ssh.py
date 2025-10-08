#!/usr/bin/env python3
"""
One-Command SSH Session Creator - FINAL AUTOMATED SOLUTION
=============================================================================

PURPOSE:
Creates persistent SSH sessions using Desktop Commander MCP tools with minimal
LLM interaction. Generates exact MCP command sequences that create working
persistent sessions.

USAGE FOR LLMS:
Just say: "Create zencart SSH session" or "Connect to zencart server"
Claude should automatically run this script and execute the generated commands.

MANUAL USAGE:
python3 one-command-ssh.py [zencart|runtipi|localuser|user@server[:port]]

TARGETS:
- zencart     → partsfor@ftp.partsfortechs.com:2022 (Zencart production)
- runtipi     → user1@runtipi1.tail1da69.ts.net:22 (Runtipi1 server)
- runtipi1    → user1@runtipi1.tail1da69.ts.net:22 (same as runtipi)
- localuser   → localhost:22 (Local session as current user)
- user@server → Custom server (optional :port)

WHAT IT DOES:
1. Generates 5 MCP commands with all parameters filled in
2. LLM executes the sequence automatically  
3. Returns working PID for interact_with_process()
4. Creates real-time logging with GUI viewing
5. Establishes persistent SSH session

TECHNICAL NOTES:
- Uses actual Desktop Commander MCP tools (start_process, interact_with_process)
- PIDs returned work with interact_with_process() for ongoing commands
- Real-time logging via tee method (no buffering issues)
- GUI log viewing via Universal Environment Runner
- Session cleanup: force_terminate(PID) when done

EXAMPLE OUTPUT:
🤖 AUTO-EXECUTE THESE MCP COMMANDS NOW:
Step 1: start_process("bash", timeout_ms=5000)
Step 2: interact_with_process(PID, "exec > >(tee -a /tmp/ssh_session_TIMESTAMP.log) 2>&1", timeout_ms=3000)
Step 3: interact_with_process(PID, "echo 'Starting SSH - $(date)' && ssh -T -p 2022 partsfor@ftp.partsfortechs.com", timeout_ms=10000)
Step 4: interact_with_process(PID, "echo 'Ready!' && pwd && hostname", timeout_ms=5000)
Step 5: start_process("python3 ~/shawndev1/universal_env_runner/universal_env_runner.py xdg-open LOG_FILE", timeout_ms=10000)

RESULT:
Working PID that can be used immediately:
interact_with_process(PID, "your_commands_here", timeout_ms=8000)

VERSION: 2.0.0 - Final Automated Solution
COMPATIBLE: Any LLM with Desktop Commander MCP support
AUTHOR: Created for automated SSH session management
DATE: 2025-09-10

=============================================================================
"""

import sys
import subprocess
import time
from datetime import datetime

# Server configurations
SERVERS = {
    "zencart": ("partsfor@ftp.partsfortechs.com", "2022"),
    "runtipi": ("user1@runtipi1.tail1da69.ts.net", "22"),
    "runtipi1": ("user1@runtipi1.tail1da69.ts.net", "22"),
    "localuser": ("localhost", "22"),  # Local session as current user
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
        print("🚀 One-Command SSH Session Creator")
        print("Usage: python3 one-command-ssh.py [zencart|runtipi|localuser|user@server[:port]]")
        print()
        print("Examples:")
        print("  python3 one-command-ssh.py zencart")
        print("  python3 one-command-ssh.py runtipi")
        print("  python3 one-command-ssh.py localuser")
        print("  python3 one-command-ssh.py user@myserver.com")
        sys.exit(1)
    
    target_name = sys.argv[1]
    
    try:
        user_server, port = parse_target(target_name)
    except ValueError as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
    
    # Generate log filename
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    log_file = f"/tmp/ssh_session_{timestamp}.log"
    
    print(f"🚀 Creating automated SSH session for {target_name}...")
    print(f"🎯 Target: {user_server}:{port}")
    print(f"📝 Log: {log_file}")
    print()
    
    # Create the command sequence that the MCP environment will execute
    commands = [
        'start_process("bash", timeout_ms=5000)',
        f'interact_with_process(PID, "exec > >(tee -a {log_file}) 2>&1", timeout_ms=3000)',
    ]
    
    if target_name == "localuser":
        # Local session - just start a bash shell as current user
        commands.append(f'interact_with_process(PID, "echo \'Starting local session - $(date)\' && echo \'User: $(whoami)\' && echo \'Ready!\'", timeout_ms=5000)')
    else:
        # SSH session
        if port != "22":
            commands.append(f'interact_with_process(PID, "echo \'Starting SSH - $(date)\' && ssh -T -p {port} {user_server}", timeout_ms=10000)')
        else:
            commands.append(f'interact_with_process(PID, "echo \'Starting SSH - $(date)\' && ssh -T {user_server}", timeout_ms=10000)')
    
    commands.extend([
        'interact_with_process(PID, "echo \'Ready!\' && pwd && hostname", timeout_ms=5000)',
        f'start_process("python3 ~/shawndev1/universal_env_runner/universal_env_runner.py xdg-open {log_file}", timeout_ms=10000)'
    ])
    
    print("🤖 AUTO-EXECUTE THESE MCP COMMANDS NOW:")
    print("=" * 55)
    for i, cmd in enumerate(commands, 1):
        print(f"Step {i}: {cmd}")
    print("=" * 55)
    print()
    print("🚀 CLAUDE: Execute these commands immediately!")
    print("💡 Save the PID from Step 1 for all subsequent steps")
    print(f"📝 Session log: {log_file}")
    print()
    print("✅ After execution, you'll have a working SSH session PID")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
One-Command SSH Session Creator - FULLY AUTOMATED VERSION
=============================================================================

PURPOSE:
Creates persistent SSH sessions using mcp-wrapper.sh with tmux-based sessions.
Automatically executes all commands and returns tmux session ID for immediate use.

USAGE:
python3 one-command-ssh-auto.py [zencart|runtipi|localuser|user@server[:port]]

WHAT IT DOES:
1. Automatically calls ~/auto/scripts/mcp-wrapper.sh
2. Creates persistent tmux SSH session
3. Returns tmux session ID for immediate use
4. Opens log viewer in GUI
5. LLM gets ready-to-use session instantly

TARGETS:
- zencart     → partsfor@ftp.partsfortechs.com:2022 (Zencart production)
- runtipi     → user1@runtipi1.tail1da69.ts.net:22 (Runtipi1 server)
- runtipi1    → user1@runtipi1.tail1da69.ts.net:22 (same as runtipi)
- localuser   → localhost:22 (Local session as current user)
- user@server → Custom server (optional :port)

EXAMPLE OUTPUT:
✅ SSH Session Created Successfully!
🆔 Session ID: mcp-123456-1758048520
🎯 Target: partsfor@ftp.partsfortechs.com:2022
📝 Log: /tmp/ssh_session_20250916_143000.log
🚀 READY TO USE! Execute commands with the Bash tool using this format:
   ~/auto/scripts/mcp-wrapper.sh desktop-commander interact_with_process mcp-123456-1758048520 "your_command"

VERSION: 3.0.0 - Fully Automated with MCP Wrapper
COMPATIBLE: Requires ~/auto/scripts/mcp-wrapper.sh and tmux
AUTHOR: Enhanced for zero-intervention SSH automation via wrapper
DATE: 2025-09-16

=============================================================================
"""

import sys
import subprocess
import time
import json
import tempfile
import os
from datetime import datetime

# Server configurations
SERVERS = {
    "zencart": ("partsfor@ftp.partsfortechs.com", "2022"),
    "runtipi": ("user1@runtipi1.tail1da69.ts.net", "22"),
    "runtipi1": ("user1@runtipi1.tail1da69.ts.net", "22"),
    "localuser": ("localhost", "22"),  # Local session as current user
}

def log_info(message):
    """Print info message with emoji"""
    print(f"🔄 {message}")

def log_success(message):
    """Print success message with emoji"""
    print(f"✅ {message}")

def log_error(message):
    """Print error message with emoji"""
    print(f"❌ {message}")

def call_mcp_wrapper(server, method, *args):
    """
    Call the actual mcp-wrapper.sh script with proper arguments
    This uses your existing MCP infrastructure with tmux sessions
    """
    wrapper_path = "/home/user1/auto/scripts/mcp-wrapper.sh"

    # Build command arguments
    cmd_args = [wrapper_path, server, method] + list(args)

    log_info(f"Calling MCP wrapper: {' '.join(cmd_args)}")

    try:
        # Execute the wrapper script
        result = subprocess.run(
            cmd_args,
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode == 0:
            return result.stdout.strip()
        else:
            # Check if stderr contains session info despite "failure"
            if "PID:" in result.stderr or "mcp-" in result.stderr:
                # The wrapper logs to stderr but may still succeed
                # Combine stdout and stderr for PID extraction
                return result.stdout.strip() + "\n" + result.stderr.strip()
            else:
                raise Exception(f"MCP wrapper failed: {result.stderr}")

    except subprocess.TimeoutExpired:
        raise Exception("MCP wrapper timeout")
    except Exception as e:
        raise Exception(f"MCP wrapper error: {e}")

def call_desktop_commander_mcp(method, args):
    """
    Call Desktop Commander via your actual MCP wrapper infrastructure
    """
    log_info(f"Calling desktop-commander: {method}")

    # Use the real MCP wrapper
    return call_mcp_wrapper("desktop-commander", method, *args)

def parse_target(target):
    """Parse target into (user@server, port) tuple"""
    if target in SERVERS:
        return SERVERS[target]

    import re
    match = re.match(r'^([^@]+@[^:]+)(?::(\d+))?$', target)
    if match:
        return match.group(1), match.group(2) or "22"

    raise ValueError(f"Invalid target: {target}")

def create_ssh_session(target_name):
    """Create SSH session automatically using MCP protocol"""
    try:
        user_server, port = parse_target(target_name)
    except ValueError as e:
        log_error(str(e))
        return None

    # Generate log filename
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    log_file = f"/tmp/ssh_session_{timestamp}.log"

    log_info(f"Creating SSH session for {target_name}")
    log_info(f"Target: {user_server}:{port}")
    log_info(f"Log: {log_file}")

    try:
        # Step 1: Start persistent session
        log_info("Step 1: Starting persistent session...")
        if target_name == "localuser":
            # Local session - just start persistent bash
            result1 = call_desktop_commander_mcp("start_process", ["persistent bash"])
        else:
            # SSH session - start with ssh command
            if port != "22":
                ssh_command = f"ssh -T -p {port} {user_server}"
            else:
                ssh_command = f"ssh -T {user_server}"
            result1 = call_desktop_commander_mcp("start_process", [f"persistent {ssh_command}"])

        # Extract PID from result - look for "PID: session_id" format or tmux session name
        pid = None
        if result1:
            lines = result1.split('\n')
            for line in lines:
                # Remove ANSI color codes
                clean_line = line.replace('\033[0;34m', '').replace('\033[0m', '').replace('[MCP-WRAPPER]', '').strip()

                if clean_line.startswith('PID: '):
                    pid = clean_line.split('PID: ')[1].strip()
                    break
                elif 'Starting persistent session:' in clean_line:
                    # Extract session ID from "Starting persistent session: mcp-99131-1758048520"
                    parts = clean_line.split('Starting persistent session:')
                    if len(parts) > 1:
                        pid = parts[1].strip()
                        break

        if not pid:
            log_error(f"Failed to get PID from start_process: {result1}")
            return None

        log_success(f"Persistent session started with PID: {pid}")

        # Step 2: Setup logging
        log_info("Step 2: Setting up logging...")
        log_cmd = f"exec > >(tee -a {log_file}) 2>&1"
        result2 = call_desktop_commander_mcp("interact_with_process", [pid, log_cmd, "3000"])

        # Step 3: Verify connection (wait a moment for SSH to establish if needed)
        log_info("Step 3: Verifying connection...")
        time.sleep(2)  # Give SSH time to connect
        verify_cmd = "echo 'Session ready!' && pwd && hostname && echo 'Connection verified'"
        result3 = call_desktop_commander_mcp("interact_with_process", [pid, verify_cmd, "5000"])

        # Step 4: Open log viewer
        log_info("Step 4: Opening log viewer...")
        try:
            viewer_cmd = f"python3 ~/shawndev1/universal_env_runner/universal_env_runner.py xdg-open {log_file}"
            call_desktop_commander_mcp("start_process", [viewer_cmd])
        except:
            log_info("Note: Could not open log viewer automatically")

        # Success!
        log_success("SSH Session Created Successfully!")
        print()
        print(f"🆔 Session ID: {pid}")
        print(f"🎯 Target: {user_server}:{port}")
        print(f"📝 Log: {log_file}")
        print()
        print("🚀 READY TO USE! Execute commands with the Bash tool using this format:")
        print(f"   ~/auto/scripts/mcp-wrapper.sh desktop-commander interact_with_process {pid} \"your_command_here\"")
        print()
        print("📋 Quick command examples:")
        print(f"   ~/auto/scripts/mcp-wrapper.sh desktop-commander interact_with_process {pid} \"pwd\"")
        print(f"   ~/auto/scripts/mcp-wrapper.sh desktop-commander interact_with_process {pid} \"ls -la\"")
        print(f"   ~/auto/scripts/mcp-wrapper.sh desktop-commander read_process_output {pid}")
        print()
        print("⚠️  IMPORTANT: Use the Bash tool with mcp-wrapper.sh commands above.")
        print("    Do NOT use native Desktop Commander MCP tools - they won't work with tmux session IDs.")

        return pid

    except Exception as e:
        log_error(f"Failed to create SSH session: {e}")
        return None

def main():
    if len(sys.argv) < 2:
        print("🚀 One-Command SSH Session Creator - FULLY AUTOMATED")
        print("Usage: python3 one-command-ssh-auto.py [zencart|runtipi|localuser|user@server[:port]]")
        print()
        print("Examples:")
        print("  python3 one-command-ssh-auto.py zencart")
        print("  python3 one-command-ssh-auto.py runtipi")
        print("  python3 one-command-ssh-auto.py localuser")
        print("  python3 one-command-ssh-auto.py user@myserver.com")
        sys.exit(1)

    target_name = sys.argv[1]

    # Create the session automatically
    pid = create_ssh_session(target_name)

    if pid:
        sys.exit(0)  # Success
    else:
        sys.exit(1)  # Failure

if __name__ == "__main__":
    main()
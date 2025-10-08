#!/usr/bin/env python3
"""
One-Command SSH Session Creator - DAEMON VERSION
=============================================================================

PURPOSE:
Creates persistent SSH sessions using the ssh-session-daemon with guaranteed survival
of parent process termination. Designed for production use with Claude Code and other LLMs.
This version uses the external daemon for true process isolation.

USAGE:
python3 one-command-ssh-daemon.py [zencart|runtipi|localuser|user@server[:port]]

WHAT IT DOES:
1. Ensures ssh-session-daemon is running
2. Creates persistent SSH sessions via daemon (true process isolation)
3. Sessions survive LLM process termination completely
4. Returns session ID that works with MCP tools
5. Provides production-ready SSH automation for LLMs

TARGETS:
- zencart     → partsfor@ftp.partsfortechs.com:2022 (Zencart production)
- runtipi     → user1@runtipi1.tail1da69.ts.net:22 (Runtipi1 server)
- runtipi1    → user1@runtipi1.tail1da69.ts.net:22 (same as runtipi)
- localuser   → localhost:22 (Local session as current user)
- user@server → Custom server (optional :port)

EXAMPLE OUTPUT:
✅ SSH Session Created Successfully!
🆔 Session ID: zencart_1726681200
🎯 Target: partsfor@ftp.partsfortechs.com:2022
📝 Daemon Socket: /tmp/ssh-session-daemon.sock
🚀 READY TO USE! The session is now active and ready for commands.
   Use session ID with daemon client or MCP tools

VERSION: 2.0.0 - Daemon-based Architecture with True Process Isolation
COMPATIBLE: ssh-session-daemon + any POSIX system
AUTHOR: Universal SSH session persistence with daemon architecture
DATE: 2025-09-18

=============================================================================
"""

import sys
import time
import json
import os
from datetime import datetime
from pathlib import Path

# Import our daemon client
sys.path.insert(0, str(Path(__file__).parent / 'ssh-session-daemon'))
from client import SessionDaemonClient, DaemonError, log_info, log_success, log_error

# Server configurations
SERVERS = {
    "zencart": ("partsfor@ftp.partsfortechs.com", "2022"),
    "runtipi": ("user1@runtipi1.tail1da69.ts.net", "22"),
    "runtipi1": ("user1@runtipi1.tail1da69.ts.net", "22"),
    "localuser": ("localhost", "22"),  # Local session as current user
}

def verify_session_exists(client: SessionDaemonClient, session_id: str) -> bool:
    """Verify that the session actually exists and is accessible"""
    log_info(f"Verifying session {session_id} exists...")

    try:
        status = client.get_session_status(session_id)
        if status.get('active', False):
            log_success(f"Session {session_id} verified as active")
            return True
        else:
            log_error(f"Session {session_id} not active")
            return False

    except DaemonError as e:
        log_error(f"Failed to verify session {session_id}: {e}")
        return False

def test_session_persistence(client: SessionDaemonClient, session_id: str, test_duration: int = 5) -> bool:
    """Test that the session persists and responds to commands"""
    log_info(f"Testing persistence of session {session_id} for {test_duration} seconds...")

    try:
        # Send a test command
        test_command = "echo 'Persistence test started' && date && echo 'Test successful'"
        result = client.send_command(session_id, test_command)

        if result and "Test successful" in str(result):
            log_success(f"Session {session_id} persistence test passed")
            return True
        else:
            log_error(f"Session {session_id} persistence test failed")
            log_info(f"Test result: {result}")
            return False

    except DaemonError as e:
        log_error(f"Persistence test failed for session {session_id}: {e}")
        return False

def store_session_info(session_id: str, target_name: str, user_server: str, port: str):
    """Store session information for later reference"""
    session_info = {
        "session_id": session_id,
        "target": target_name,
        "server": user_server,
        "port": port,
        "created": datetime.now().isoformat(),
        "script_version": "2.0.0",
        "daemon_based": True
    }

    info_file = f"/tmp/ssh_session_{session_id}_info.json"
    try:
        with open(info_file, 'w') as f:
            json.dump(session_info, f, indent=2)
        log_success(f"Session info saved to: {info_file}")
        return info_file
    except Exception as e:
        log_error(f"Failed to save session info: {e}")
        return None

def parse_target(target):
    """Parse target into (user@server, port) tuple"""
    if target in SERVERS:
        return SERVERS[target]

    import re
    match = re.match(r'^([^@]+@[^:]+)(?::(\d+))?$', target)
    if match:
        return match.group(1), match.group(2) or "22"

    raise ValueError(f"Invalid target: {target}")

def create_ssh_session(target_name: str) -> str:
    """Create SSH session using daemon"""
    try:
        user_server, port = parse_target(target_name)
    except ValueError as e:
        log_error(str(e))
        return None

    log_info(f"Creating SSH session for {target_name}")
    log_info(f"Target: {user_server}:{port}")

    try:
        # Step 1: Initialize daemon client
        log_info("Step 1: Initializing daemon client...")
        client = SessionDaemonClient(auto_start=True)

        # Step 2: Build SSH command
        log_info("Step 2: Building SSH command...")

        if target_name == "localuser":
            # Local session - start bash with proper environment
            ssh_command = "bash -l -i"
            session_name = "localuser"
        else:
            # SSH session with optimized options
            base_ssh_cmd = "ssh -T"
            if port != "22":
                base_ssh_cmd += f" -p {port}"

            # Add SSH options for better connection persistence
            ssh_options = [
                "-o ServerAliveInterval=60",      # Send keepalive every 60 seconds
                "-o ServerAliveCountMax=3",       # Allow 3 missed keepalives
                "-o TCPKeepAlive=yes",           # Use TCP keepalive
                "-o ExitOnForwardFailure=no",    # Don't exit on port forwarding failure
                "-o ConnectTimeout=30",          # 30 second connection timeout
                "-o StrictHostKeyChecking=no",   # Auto-accept host keys
                "-o UserKnownHostsFile=/dev/null", # Don't save host keys
                "-o LogLevel=ERROR"              # Reduce log noise
            ]

            ssh_command = f"{base_ssh_cmd} {' '.join(ssh_options)} {user_server}"
            session_name = target_name

        log_info(f"Command: {ssh_command}")

        # Step 3: Create session via daemon
        log_info("Step 3: Creating session via daemon...")
        session_id = client.create_session(session_name, ssh_command)

        if not session_id:
            log_error("Failed to create session via daemon")
            return None

        # Step 4: Verify session exists and is accessible
        log_info("Step 4: Verifying session exists...")
        if not verify_session_exists(client, session_id):
            log_error("Session verification failed")
            return None

        # Step 5: Test session persistence and connectivity
        log_info("Step 5: Testing persistence and connectivity...")
        time.sleep(2)  # Give SSH time to connect if needed

        if not test_session_persistence(client, session_id):
            log_error("Persistence test failed")
            return None

        # Step 6: Additional connection verification
        log_info("Step 6: Performing detailed connection verification...")
        verify_cmd = "echo 'Session ready!' && pwd && hostname && echo 'Connection verified'"

        try:
            result = client.send_command(session_id, verify_cmd)
            if result:
                log_info(f"Connection verification result preview: {result[:200]}...")
            else:
                log_error("Connection verification failed")
        except DaemonError as e:
            log_error(f"Connection verification error: {e}")

        # Step 7: Store session information
        log_info("Step 7: Storing session information...")
        info_file = store_session_info(session_id, target_name, user_server, port)

        # Success!
        log_success("SSH Session Created Successfully!")
        print()
        print(f"🆔 Session ID: {session_id}")
        print(f"🎯 Target: {user_server}:{port}")
        print(f"🔧 Daemon Socket: {client.socket_path}")
        if info_file:
            print(f"📄 Info: {info_file}")
        print()
        print("🔒 TRUE PROCESS ISOLATION! This session is managed by ssh-session-daemon")
        print("    and will survive LLM process termination completely.")
        print("🚀 READY TO USE! The session is now active and ready for commands.")
        print()
        print("📋 Use these methods with the Session ID:")
        print("   Python:")
        print(f"     client = SessionDaemonClient()")
        print(f"     output = client.send_command('{session_id}', 'your_command')")
        print(f"     client.terminate_session('{session_id}')")
        print()
        print("   MCP Compatibility (via client.py):")
        print(f"     execute_mcp_command('mcp__desktop-commander__interact_with_process',")
        print(f"                         pid='{session_id}', input='your_command', timeout_ms=8000)")
        print()
        print("💡 Example commands to try:")
        print(f"   client.send_command('{session_id}', 'pwd')")
        print(f"   client.send_command('{session_id}', 'ls -la')")
        print(f"   client.send_command('{session_id}', 'whoami')")
        print()
        print("🛡️  DAEMON PERSISTENCE FEATURES:")
        print("   • Complete process tree isolation via external daemon")
        print("   • Sessions survive LLM termination")
        print("   • Unix socket communication with daemon")
        print("   • Session recovery across daemon restarts")
        print("   • True universal compatibility (POSIX)")

        return session_id

    except DaemonError as e:
        log_error(f"Daemon error: {e}")
        return None
    except Exception as e:
        log_error(f"Failed to create SSH session: {e}")
        return None

def main():
    if len(sys.argv) < 2:
        print("🚀 One-Command SSH Session Creator - DAEMON VERSION")
        print("Usage: python3 one-command-ssh-daemon.py [zencart|runtipi|localuser|user@server[:port]]")
        print()
        print("Examples:")
        print("  python3 one-command-ssh-daemon.py zencart")
        print("  python3 one-command-ssh-daemon.py runtipi")
        print("  python3 one-command-ssh-daemon.py localuser")
        print("  python3 one-command-ssh-daemon.py user@myserver.com")
        print()
        print("This version uses ssh-session-daemon for true process isolation.")
        print("Sessions survive LLM termination completely.")
        sys.exit(1)

    target_name = sys.argv[1]

    # Create the session automatically
    session_id = create_ssh_session(target_name)

    if session_id:
        sys.exit(0)  # Success
    else:
        sys.exit(1)  # Failure

if __name__ == "__main__":
    main()
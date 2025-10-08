#!/usr/bin/env python3
"""
Generic Persistent Root Session Manager with MCP Desktop Commander Support

Creates a persistent root shell session using Desktop Commander MCP tools
(if available) or falls back to native Python subprocess management.

The session uses pkexec and stays open for multiple commands without 
repeated password prompts.

Usage:
    session = PersistentRootSession()
    session.start()
    session.run_command("your command here")
    session.cleanup()
"""

import subprocess
import sys
import time
import threading
import queue
import json

# Try to detect if MCP tools are available
def check_mcp_available():
    """Check if Desktop Commander MCP tools are available"""
    try:
        # Try to import or check for MCP tools availability
        # This would normally check if the MCP server is running
        # For now, we'll check via environment or config
        import os
        # Check for MCP indicator (you might need to adjust this based on your setup)
        return os.environ.get('MCP_DESKTOP_COMMANDER') == 'true' or \
               os.path.exists('/tmp/mcp-desktop-commander.sock')
    except:
        return False

class PersistentRootSession:
    def __init__(self, prefer_mcp=True):
        self.process = None
        self.output_queue = queue.Queue()
        self.output_thread = None
        self.session_active = False
        self.use_mcp = prefer_mcp and check_mcp_available()
        self.mcp_pid = None  # Store PID for MCP process
        self.mode = "MCP" if self.use_mcp else "SUBPROCESS"
        
    def start(self):
        """Start persistent root session - password prompt happens here"""
        print(f"🔐 Starting Persistent Root Session (Mode: {self.mode})")
        print("=" * 50)
        print("Enter password when prompted. Session will stay open for multiple commands.")
        print()
        
        # Try MCP method first if available
        if self.use_mcp:
            try:
                return self._start_mcp_session()
            except Exception as e:
                print(f"⚠️ MCP method failed: {e}")
                print("📝 Falling back to subprocess method...")
                self.use_mcp = False
                self.mode = "SUBPROCESS"
        
        # Fallback to subprocess method
        return self._start_subprocess_session()
    
    def _start_mcp_session(self):
        """Start session using Desktop Commander MCP tools"""
        try:
            # Note: This is a template for MCP integration
            # In actual use with Claude Code, you would call the MCP tools directly
            # For standalone Python script, we simulate the MCP calls
            
            print("🔧 Using Desktop Commander MCP tools...")
            
            # This would be replaced with actual MCP tool calls in Claude Code:
            # result = mcp__desktop-commander__start_process("pkexec bash -i", timeout_ms=5000)
            
            # For standalone script, we simulate MCP behavior
            import requests
            mcp_response = requests.post(
                "http://localhost:3000/mcp/desktop-commander/start_process",
                json={"command": "pkexec bash -i", "timeout_ms": 5000},
                timeout=10
            )
            
            if mcp_response.status_code == 200:
                result = mcp_response.json()
                self.mcp_pid = result.get('pid')
                
                # Verify session is ready
                verify_response = requests.post(
                    "http://localhost:3000/mcp/desktop-commander/interact_with_process",
                    json={
                        "pid": self.mcp_pid,
                        "input": "echo 'ROOT_SESSION_READY'",
                        "timeout_ms": 3000
                    }
                )
                
                if verify_response.status_code == 200:
                    output = verify_response.json().get('output', '')
                    if 'ROOT_SESSION_READY' in output:
                        self.session_active = True
                        print(f"✅ MCP Root session established! (PID: {self.mcp_pid})")
                        return True
            
            raise Exception("MCP session verification failed")
            
        except Exception as e:
            raise Exception(f"MCP session start failed: {e}")
    
    def _start_subprocess_session(self):
        """Start session using native Python subprocess (fallback)"""
        try:
            print("🔧 Using native subprocess method...")
            
            # Start interactive bash session as root
            self.process = subprocess.Popen(
                ["pkexec", "bash", "-i"],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1
            )
            
            # Start output monitoring thread
            self.output_thread = threading.Thread(target=self._monitor_output, daemon=True)
            self.output_thread.start()
            
            # Wait for session to establish and consume initial prompt
            time.sleep(2)
            self._drain_initial_output()
            
            # Test session with simple command
            self.process.stdin.write("echo 'ROOT_SESSION_READY'\n")
            self.process.stdin.flush()
            
            # Wait for confirmation
            start_time = time.time()
            while time.time() - start_time < 5:
                try:
                    line = self.output_queue.get(timeout=0.1)
                    if "ROOT_SESSION_READY" in line:
                        self.session_active = True
                        print("✅ Subprocess root session established and ready!")
                        return True
                except queue.Empty:
                    continue
            
            print("❌ Session verification failed")
            return False
            
        except Exception as e:
            print(f"❌ Failed to start subprocess root session: {e}")
            return False
    
    def _monitor_output(self):
        """Monitor process output in background thread"""
        while self.process and self.process.poll() is None:
            try:
                line = self.process.stdout.readline()
                if line:
                    self.output_queue.put(line.rstrip())
            except:
                break
    
    def _drain_initial_output(self):
        """Drain initial shell startup output"""
        time.sleep(1)
        while not self.output_queue.empty():
            try:
                self.output_queue.get_nowait()
            except queue.Empty:
                break
    
    def run_command(self, command, timeout=10, show_output=True):
        """
        Run a command in the persistent root session
        
        Args:
            command: Command to execute
            timeout: Max seconds to wait for output
            show_output: Print output to console
            
        Returns:
            (success: bool, output: list of lines)
        """
        if not self.session_active:
            print("❌ Root session not active")
            return False, []
        
        # Use appropriate method based on mode
        if self.use_mcp and self.mcp_pid:
            return self._run_mcp_command(command, timeout, show_output)
        else:
            return self._run_subprocess_command(command, timeout, show_output)
    
    def _run_mcp_command(self, command, timeout=10, show_output=True):
        """Run command using MCP tools"""
        try:
            if show_output:
                print(f"🔧 Running (MCP): {command}")
                print("-" * 50)
            
            # For standalone script, simulate MCP call
            import requests
            response = requests.post(
                "http://localhost:3000/mcp/desktop-commander/interact_with_process",
                json={
                    "pid": self.mcp_pid,
                    "input": command,
                    "timeout_ms": timeout * 1000,
                    "wait_for_prompt": True
                },
                timeout=timeout + 5
            )
            
            if response.status_code == 200:
                result = response.json()
                output = result.get('output', '')
                output_lines = output.split('\n') if output else []
                
                if show_output:
                    for line in output_lines:
                        if line.strip():
                            print(line)
                
                return True, output_lines
            else:
                raise Exception(f"MCP command failed with status {response.status_code}")
                
        except Exception as e:
            if show_output:
                print(f"⚠️ MCP command failed: {e}, falling back to subprocess")
            # Try fallback if MCP fails
            self.use_mcp = False
            if self.process:
                return self._run_subprocess_command(command, timeout, show_output)
            return False, []
    
    def _run_subprocess_command(self, command, timeout=10, show_output=True):
        """Run command using subprocess (fallback)"""
        if not self.process or self.process.poll() is not None:
            print("❌ Subprocess session not active")
            return False, []
            
        try:
            if show_output:
                print(f"🔧 Running (Subprocess): {command}")
                print("-" * 50)
            
            # Send command with unique marker for end detection
            marker = f"CMD_COMPLETE_{int(time.time()*1000)}"
            full_command = f"{command}; echo '{marker}'"
            
            self.process.stdin.write(full_command + "\n")
            self.process.stdin.flush()
            
            # Collect output until we see the marker
            output_lines = []
            start_time = time.time()
            
            while time.time() - start_time < timeout:
                try:
                    line = self.output_queue.get(timeout=0.1)
                    
                    if marker in line:
                        # Command completed
                        break
                    
                    output_lines.append(line)
                    if show_output:
                        print(line)
                        
                except queue.Empty:
                    continue
            
            return True, output_lines
            
        except Exception as e:
            if show_output:
                print(f"❌ Command failed: {e}")
            return False, []
    
    def is_active(self):
        """Check if session is still active"""
        if self.use_mcp and self.mcp_pid:
            # For MCP, check if process is still running
            try:
                import requests
                response = requests.post(
                    "http://localhost:3000/mcp/desktop-commander/list_sessions",
                    timeout=5
                )
                if response.status_code == 200:
                    sessions = response.json().get('sessions', [])
                    return any(s.get('pid') == self.mcp_pid for s in sessions)
            except:
                pass
            return False
        else:
            return self.session_active and self.process and self.process.poll() is None
    
    def cleanup(self):
        """Clean up the root session"""
        if self.use_mcp and self.mcp_pid:
            try:
                print(f"🧹 Closing MCP root session (PID: {self.mcp_pid})...")
                
                # Send exit command first
                import requests
                requests.post(
                    "http://localhost:3000/mcp/desktop-commander/interact_with_process",
                    json={
                        "pid": self.mcp_pid,
                        "input": "exit",
                        "timeout_ms": 2000
                    },
                    timeout=5
                )
                
                # Then force terminate if needed
                time.sleep(1)
                requests.post(
                    "http://localhost:3000/mcp/desktop-commander/force_terminate",
                    json={"pid": self.mcp_pid},
                    timeout=5
                )
                
                print("✅ MCP root session closed")
            except Exception as e:
                print(f"⚠️ MCP cleanup warning: {e}")
            finally:
                self.mcp_pid = None
                self.session_active = False
        
        if self.process:
            try:
                print("🧹 Closing subprocess root session...")
                self.process.stdin.write("exit\n")
                self.process.stdin.flush()
                self.process.wait(timeout=5)
            except:
                print("🔨 Force terminating subprocess session...")
                self.process.terminate()
                try:
                    self.process.wait(timeout=2)
                except:
                    self.process.kill()
            finally:
                self.process = None
                self.session_active = False
            
            print("✅ Subprocess root session closed")

def demo_usage():
    """Demonstrate how to use the persistent root session"""
    print("🎯 Persistent Root Session Demo")
    print("=" * 50)
    
    session = PersistentRootSession()
    
    if not session.start():
        return False
    
    try:
        # Example commands
        print("\n📋 Running example commands...")
        
        session.run_command("whoami")
        session.run_command("pwd")
        session.run_command("ls -la /tmp")
        session.run_command("date")
        
        print("\n✅ Demo completed successfully!")
        return True
        
    finally:
        session.cleanup()

if __name__ == "__main__":
    print("Generic Persistent Root Session Manager")
    print("Usage: Import this class or run demo")
    print()
    
    if len(sys.argv) > 1 and sys.argv[1] == "demo":
        success = demo_usage()
        sys.exit(0 if success else 1)
    else:
        print("💡 Run with 'demo' argument to see example usage")
        print("💡 Or import PersistentRootSession class in your scripts")
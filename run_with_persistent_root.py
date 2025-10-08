#!/usr/bin/env python3
"""
Persistent root session runner - uses pkexec once, then maintains root session
"""
import subprocess
import sys
import os
import time
import signal

class PersistentRootSession:
    def __init__(self):
        self.root_process = None
        self.setup_root_session()
    
    def setup_root_session(self):
        """Start a persistent root shell using pkexec"""
        print("🔐 Starting persistent root session (you'll only need to enter password once)...")
        
        # Start a persistent bash session as root
        try:
            self.root_process = subprocess.Popen(
                ['pkexec', 'bash'],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1  # Line buffered
            )
            
            # Test the session by running a simple command
            self.run_command("echo 'Root session established'")
            print("✅ Root session ready!")
            
        except Exception as e:
            print(f"❌ Failed to establish root session: {e}")
            sys.exit(1)
    
    def run_command(self, command, timeout=300):
        """Run a command in the persistent root session"""
        if not self.root_process or self.root_process.poll() is not None:
            print("❌ Root session lost, re-establishing...")
            self.setup_root_session()
        
        print(f"🔧 Running: {command}")
        
        # Send command with unique marker for output parsing
        marker = f"__COMMAND_END_{int(time.time() * 1000)}__"
        full_command = f"{command}; echo '{marker}' EXIT_CODE=$?\n"
        
        self.root_process.stdin.write(full_command)
        self.root_process.stdin.flush()
        
        # Collect output until we see our marker
        output_lines = []
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            try:
                line = self.root_process.stdout.readline()
                if not line:
                    break
                
                print(line.rstrip())  # Show output in real-time
                
                if marker in line:
                    # Extract exit code
                    if 'EXIT_CODE=' in line:
                        exit_code = int(line.split('EXIT_CODE=')[1].strip())
                        return exit_code
                    break
                    
                output_lines.append(line.rstrip())
                
            except Exception as e:
                print(f"Error reading output: {e}")
                break
        
        return 0
    
    def cleanup(self):
        """Clean up the root session"""
        if self.root_process and self.root_process.poll() is None:
            print("🧹 Cleaning up root session...")
            self.root_process.stdin.write("exit\n")
            self.root_process.stdin.flush()
            self.root_process.wait(timeout=5)

def signal_handler(sig, frame):
    """Handle Ctrl+C gracefully"""
    print("\n🛑 Interrupted by user")
    if hasattr(signal_handler, 'session'):
        signal_handler.session.cleanup()
    sys.exit(0)

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 run_with_persistent_root.py '<command>'")
        print("Example: python3 run_with_persistent_root.py './enhanced-build-system-complete.sh'")
        sys.exit(1)
    
    command = " ".join(sys.argv[1:])
    
    # Set up signal handler
    signal.signal(signal.SIGINT, signal_handler)
    
    # Create persistent session
    session = PersistentRootSession()
    signal_handler.session = session  # Store for cleanup
    
    try:
        # Change to the script directory
        script_dir = "/home/user1/shawndev1/ubuntu-snappy"
        session.run_command(f"cd {script_dir}")
        
        # Run the main command with smart resume (option 1)
        if 'enhanced-build-system-complete.sh' in command:
            exit_code = session.run_command(f"echo '1' | {command}", timeout=600)
        else:
            exit_code = session.run_command(command, timeout=600)
        
        print(f"✅ Command completed with exit code: {exit_code}")
        
    except KeyboardInterrupt:
        print("\n🛑 Interrupted by user")
    finally:
        session.cleanup()

if __name__ == "__main__":
    main()
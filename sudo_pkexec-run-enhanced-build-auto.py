#!/usr/bin/env python3

import subprocess
import sys
import os
import time

def run_build_system():
    """Run the enhanced build system with automatic responses to prompts"""
    
    print("🚀 Starting Enhanced VM Build System with Auto-Response")
    print("=" * 60)
    
    # Change to the script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    # Use pkexec to run the build script
    cmd = ["pkexec", "./enhanced-build-system-complete.sh"]
    
    try:
        # Start the process
        process = subprocess.Popen(
            cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            universal_newlines=True
        )
        
        output_buffer = ""
        
        while True:
            # Read character by character to catch prompts immediately
            char = process.stdout.read(1)
            if not char:
                break
                
            output_buffer += char
            print(char, end='', flush=True)
            
            # Check for interactive prompts and respond automatically
            if "Delete existing VM disk and build fresh?" in output_buffer:
                print("\n[AUTO] Responding 'y' to delete existing VM disk")
                process.stdin.write("y\n")
                process.stdin.flush()
                output_buffer = ""
                
            elif "Clear cache and redownload all packages?" in output_buffer:
                print("\n[AUTO] Responding 'n' to keep existing cache")
                process.stdin.write("n\n")
                process.stdin.flush()
                output_buffer = ""
                
            elif "Choose storage controller type" in output_buffer and "[1]" in output_buffer:
                print("\n[AUTO] Responding '1' for VirtIO storage (default)")
                process.stdin.write("1\n")
                process.stdin.flush()
                output_buffer = ""
                
            elif "Remove the stale lock file and continue?" in output_buffer:
                print("\n[AUTO] Responding 'y' to remove stale lock file")
                process.stdin.write("y\n")
                process.stdin.flush()
                output_buffer = ""
            
            # Keep buffer manageable
            if len(output_buffer) > 1000:
                output_buffer = output_buffer[-500:]
        
        # Wait for process to complete
        return_code = process.wait()
        
        if return_code == 0:
            print("\n" + "=" * 60)
            print("✅ BUILD COMPLETED SUCCESSFULLY!")
            print("=" * 60)
            return True
        else:
            print(f"\n❌ Build failed with exit code: {return_code}")
            return False
            
    except KeyboardInterrupt:
        print("\n⚠️  Build interrupted by user")
        process.terminate()
        return False
    except Exception as e:
        print(f"\n❌ Error running build: {e}")
        return False

if __name__ == "__main__":
    print("Enhanced VM Build System - Auto Runner")
    print("This script will automatically handle prompts and use pkexec for authentication")
    print("")
    
    if not os.path.exists("enhanced-build-system-complete.sh"):
        print("❌ Error: enhanced-build-system-complete.sh not found in current directory")
        sys.exit(1)
    
    success = run_build_system()
    sys.exit(0 if success else 1)
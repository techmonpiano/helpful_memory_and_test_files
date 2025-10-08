#!/usr/bin/env python3
"""
Quick Start Script for Western Coding Models
Simple script to test your deployment quickly
"""

import os
import sys
import subprocess

def check_modal_setup():
    """Check if Modal is properly set up"""
    try:
        result = subprocess.run(["modal", "--help"], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Modal CLI is installed")
            
            # Check if authenticated
            result = subprocess.run(["modal", "app", "list"], capture_output=True, text=True)
            if result.returncode == 0:
                print("✅ Modal is authenticated")
                return True
            else:
                print("❌ Modal not authenticated. Run: python3 -m modal setup")
                return False
        else:
            print("❌ Modal CLI not found. Run: pip install modal")
            return False
    except FileNotFoundError:
        print("❌ Modal CLI not found. Run: pip install modal")
        return False

def deploy_model(model_type="codestral-25"):
    """Deploy a specific model"""
    print(f"\n🚀 Deploying {model_type}...")
    
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    modal_file = os.path.join(script_dir, "modal_western_coder.py")
    
    if not os.path.exists(modal_file):
        print(f"❌ Cannot find modal_western_coder.py at {modal_file}")
        return False
    
    env = os.environ.copy()
    env["MODEL_TYPE"] = model_type
    
    try:
        print("📦 Starting deployment (this may take a few minutes)...")
        print("🔄 Live output:")
        print("-" * 50)
        
        # Run with real-time output
        process = subprocess.Popen(
            ["modal", "deploy", modal_file],
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            universal_newlines=True
        )
        
        # Stream output in real-time
        output_lines = []
        while True:
            line = process.stdout.readline()
            if line:
                print(line.rstrip())  # Print line immediately
                output_lines.append(line)
            elif process.poll() is not None:
                break
        
        # Get any remaining output
        remaining = process.stdout.read()
        if remaining:
            print(remaining.rstrip())
            output_lines.append(remaining)
        
        return_code = process.returncode
        full_output = ''.join(output_lines)
        
        print("-" * 50)
        if return_code == 0:
            print(f"✅ Successfully deployed {model_type}!")
            return True
        else:
            print(f"❌ Failed to deploy {model_type}")
            return False
            
    except Exception as e:
        print(f"❌ Exception during deployment: {e}")
        return False

def test_deployment(model_type="codestral-25"):
    """Test the deployment"""
    print(f"\n🧪 Testing {model_type}...")
    
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    test_file = os.path.join(script_dir, "test_western_models.py")
    
    try:
        result = subprocess.run(
            ["python", test_file, "--model", model_type],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print("✅ Tests passed!")
            print(result.stdout[-500:])  # Show last 500 chars
            return True
        else:
            print("❌ Tests failed")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Exception during testing: {e}")
        return False

def main():
    print("🌟 Western Coding Models - Quick Start")
    print("=" * 50)
    
    # Check Modal setup
    if not check_modal_setup():
        sys.exit(1)
    
    # Model selection
    models = {
        "1": ("codestral-25", "Mistral Codestral 25.01 (Recommended)"),
        "2": ("codestral-mamba", "Mistral Codestral Mamba 7B"), 
        "3": ("phi4", "Microsoft Phi-4")
    }
    
    print("\nAvailable models:")
    for key, (model_id, description) in models.items():
        print(f"{key}. {description}")
    
    while True:
        choice = input("\nSelect model (1-3) or 'q' to quit: ").strip()
        if choice.lower() == 'q':
            sys.exit(0)
        if choice in models:
            model_type, description = models[choice]
            break
        print("Invalid choice. Please select 1-3.")
    
    print(f"\n🎯 Selected: {description}")
    
    # Deploy model
    deploy_success = deploy_model(model_type)
    if not deploy_success:
        print("\n❌ Deployment failed. Check the error messages above.")
        sys.exit(1)
    
    # Ask if user wants to run tests
    run_tests = input("\n🧪 Run tests now? (y/n): ").strip().lower()
    if run_tests in ['y', 'yes']:
        test_deployment(model_type)
    
    print(f"\n🎉 Quick start complete!")
    print(f"Your {description} is deployed and ready to use.")
    print(f"\nNext steps:")
    print(f"- Visit the web UI at your Modal endpoint")
    print(f"- Run tests: python test_western_models.py --model {model_type}")
    print(f"- Check the DEPLOYMENT_GUIDE.md for advanced usage")
    print(f"- Use the OpenAI-compatible API endpoint")

if __name__ == "__main__":
    main()
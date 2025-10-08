#!/usr/bin/env python3

import asyncio
from playwright.async_api import async_playwright

async def test_single_terminal():
    """
    Test that the duplicate terminal boxes issue is fixed
    """
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=1000)
        page = await browser.new_page()
        
        try:
            print("🔧 TESTING: Single Terminal Box Fix")
            print("=" * 50)
            
            # Load and initialize
            await page.goto("http://localhost:3050")
            await page.wait_for_timeout(3000)
            
            # Open terminal
            print("🖥️  Opening terminal...")
            await page.click('button:has-text("Terminal")')
            await page.wait_for_timeout(5000)  # Give extra time for proper initialization
            
            # Take screenshot of initial state
            await page.screenshot(path="single_terminal_01_initial.png")
            print("📸 Screenshot: single_terminal_01_initial.png")
            
            # Test sendToTerminal function
            print("\n🧪 Testing sendToTerminal function...")
            await page.evaluate("""
                () => {
                    if (window.sendToTerminal) {
                        window.sendToTerminal('echo "Testing single terminal box"');
                    }
                }
            """)
            
            await page.wait_for_timeout(3000)
            await page.screenshot(path="single_terminal_02_after_command.png")
            print("📸 Screenshot: single_terminal_02_after_command.png")
            
            # Send multiple commands to test consistency
            print("\n🔄 Testing multiple commands...")
            commands = [
                'echo "Command 1"',
                'pwd',
                'echo "Command 2"'
            ]
            
            for i, cmd in enumerate(commands, 1):
                print(f"   📤 Command {i}: {cmd}")
                await page.evaluate(f"""
                    () => {{
                        if (window.sendToTerminal) {{
                            window.sendToTerminal('{cmd}');
                        }}
                    }}
                """)
                await page.wait_for_timeout(2000)
            
            # Final screenshot
            await page.screenshot(path="single_terminal_03_multiple_commands.png")
            print("📸 Screenshot: single_terminal_03_multiple_commands.png")
            
            # Count the number of prompt boxes in the terminal
            prompt_count = await page.evaluate("""
                () => {
                    const terminal = document.querySelector('.xterm-screen, .terminal-mount-point');
                    if (!terminal) return 0;
                    
                    const content = terminal.textContent || '';
                    // Count the number of '>' prompts (command line indicators)
                    const matches = content.match(/>/g);
                    return matches ? matches.length : 0;
                }
            """)
            
            print(f"\n📋 Analysis:")
            print(f"   🎯 Number of command prompts detected: {prompt_count}")
            
            if prompt_count <= 3:  # Should be around 1-2 prompts, not 6+ like before
                print("   ✅ SUCCESS: Single terminal box working!")
                print("   ✅ Duplicate terminal boxes issue appears to be fixed")
            else:
                print("   ⚠️  WARNING: Still seeing multiple terminal boxes")
                print("   ⚠️  May need additional backend cleanup")
            
            print("\n👀 Browser staying open for 15 seconds for manual inspection...")
            await page.wait_for_timeout(15000)
            
        except Exception as error:
            print(f"❌ Error: {error}")
            await page.screenshot(path="single_terminal_error.png")
            
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(test_single_terminal())
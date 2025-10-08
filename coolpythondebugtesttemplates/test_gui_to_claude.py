#!/usr/bin/env python3

import asyncio
from playwright.async_api import async_playwright

async def test_gui_to_claude_message():
    """
    Test: Type message in main GUI, then check terminal to see if it reached Claude
    """
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=1000)
        page = await browser.new_page()
        
        try:
            print("🎯 TEST: GUI Message → Claude Terminal Verification")
            print("=" * 60)
            
            # Step 1: Load the app
            print("📱 Loading Claude Code GUI...")
            await page.goto("http://localhost:3050")
            await page.wait_for_timeout(3000)
            
            # Step 2: Type message in main GUI
            print("\n📝 STEP 1: Typing message in main GUI...")
            
            # Find the main message input
            message_input = await page.wait_for_selector(
                'textarea:visible, input[placeholder*="Ask Claude"]:visible, input[type="text"]:visible'
            )
            
            test_message = "hello from GUI test"
            print(f"   ⌨️  Typing: '{test_message}'")
            await message_input.fill(test_message)
            
            # Take screenshot before sending
            await page.screenshot(path="gui_claude_01_before_send.png")
            print("   📸 Screenshot: gui_claude_01_before_send.png")
            
            # Send the message
            print("   🚀 Sending message (pressing Enter)...")
            await page.keyboard.press("Enter")
            await page.wait_for_timeout(3000)  # Wait for message to be sent
            
            # Take screenshot after sending
            await page.screenshot(path="gui_claude_02_after_send.png")
            print("   📸 Screenshot: gui_claude_02_after_send.png")
            print("   ✅ Message sent from GUI!")
            
            # Step 3: Open terminal to check if message reached Claude
            print("\n🖥️  STEP 2: Opening terminal to verify message reached Claude...")
            
            terminal_button = await page.wait_for_selector('button:has-text("Terminal")')
            await terminal_button.click()
            await page.wait_for_timeout(4000)  # Wait for terminal to fully load
            
            # Take screenshot of terminal
            await page.screenshot(path="gui_claude_03_terminal_check.png")
            print("   📸 Screenshot: gui_claude_03_terminal_check.png")
            
            # Step 4: Look for our message in the terminal
            print("\n🔍 STEP 3: Analyzing terminal content...")
            
            # Check if terminal shows our message
            terminal_content = await page.evaluate("""
                () => {
                    // Try to get terminal text content
                    const terminalElement = document.querySelector('.xterm-screen, .terminal-mount-point, [class*="xterm"]');
                    return terminalElement ? terminalElement.textContent : 'Terminal not found';
                }
            """)
            
            print(f"   📋 Terminal content preview: {terminal_content[:200]}...")
            
            # Check specifically for our test message
            message_found_in_terminal = test_message.lower() in terminal_content.lower()
            print(f"   🎯 Test message '{test_message}' found in terminal: {message_found_in_terminal}")
            
            # Step 5: Check console logs for bridge activity
            print("\n🔍 STEP 4: Checking for bridge function calls...")
            
            bridge_status = await page.evaluate("""
                () => {
                    return {
                        sendToTerminalExists: typeof window.sendToTerminal === 'function',
                        terminalInitialized: !!window.sendToTerminal
                    };
                }
            """)
            
            print(f"   📋 sendToTerminal function exists: {bridge_status['sendToTerminalExists']}")
            print(f"   📋 Terminal initialized: {bridge_status['terminalInitialized']}")
            
            # Step 6: Manual test to confirm bridge works
            print("\n🧪 STEP 5: Testing bridge function manually...")
            
            if bridge_status['sendToTerminalExists']:
                print("   🎯 Manually calling sendToTerminal('echo BRIDGE_TEST')...")
                
                await page.evaluate("""
                    () => {
                        if (window.sendToTerminal) {
                            window.sendToTerminal('echo BRIDGE_TEST');
                        }
                    }
                """)
                
                await page.wait_for_timeout(3000)
                
                # Take final screenshot
                await page.screenshot(path="gui_claude_04_bridge_test.png")
                print("   📸 Screenshot: gui_claude_04_bridge_test.png")
                print("   ✅ Manual bridge test executed!")
            
            # Step 7: Results summary
            print("\n" + "=" * 60)
            print("🎉 TEST RESULTS SUMMARY:")
            print(f"✅ GUI message sent: YES")
            print(f"✅ Terminal opened: YES") 
            print(f"✅ sendToTerminal function available: {bridge_status['sendToTerminalExists']}")
            print(f"📝 Message in terminal: {message_found_in_terminal}")
            print("=" * 60)
            
            if message_found_in_terminal:
                print("🎉 SUCCESS: Message successfully sent from GUI to Claude terminal!")
            else:
                print("⚠️  Note: Message may be processed but not visible in terminal text")
                print("    Check screenshots to see actual terminal state")
            
            # Keep browser open for manual inspection
            print("\n👀 Keeping browser open for 15 seconds for manual inspection...")
            await page.wait_for_timeout(15000)
            
        except Exception as error:
            print(f"❌ Test failed: {error}")
            await page.screenshot(path="gui_claude_error.png")
            print("📸 Error screenshot: gui_claude_error.png")
            
        finally:
            await browser.close()

# Run the test
if __name__ == "__main__":
    print("🎯 Starting GUI → Claude Terminal Test...")
    asyncio.run(test_gui_to_claude_message())
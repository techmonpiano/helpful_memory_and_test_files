#!/usr/bin/env python3
"""
Simple Enter Key Test
Tests if GUI messages properly execute in terminal with Enter key
"""

import asyncio
from playwright.async_api import async_playwright

async def test_enter_key_simple():
    print("🧪 Simple GUI→Terminal Enter key test...")
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=500)
        page = await browser.new_page()
        
        try:
            # Load the application
            print("🌐 Loading application...")
            await page.goto('http://localhost:3050')
            await page.wait_for_load_state('networkidle')
            await page.wait_for_timeout(5000)
            
            # Take initial screenshot
            await page.screenshot(path='simple-01-loaded.png', full_page=True)
            print("📸 Application loaded")
            
            # Type message in GUI chat input
            test_message = 'echo "Hello from GUI test"'
            print(f"💬 Typing: {test_message}")
            
            # Find chat input (try multiple approaches)
            chat_input = None
            try:
                chat_input = await page.wait_for_selector('textarea[placeholder*="message"]', timeout=3000)
                print("✅ Found message textarea")
            except:
                try:
                    chat_input = await page.wait_for_selector('textarea:not(.xterm-helper-textarea)', timeout=2000)
                    print("✅ Found non-terminal textarea")
                except:
                    print("❌ No chat input found")
                    await page.screenshot(path='simple-error-no-input.png', full_page=True)
                    return
            
            # Type the message
            await chat_input.fill(test_message)
            await page.screenshot(path='simple-02-message-typed.png', full_page=True)
            print("📸 Message typed")
            
            # Send the message
            try:
                send_btn = await page.wait_for_selector('button[type="submit"]', timeout=2000)
                await send_btn.click()
                print("✅ Sent via submit button")
            except:
                await chat_input.press('Enter')
                print("✅ Sent via Enter key")
            
            await page.wait_for_timeout(2000)
            await page.screenshot(path='simple-03-message-sent.png', full_page=True)
            print("📸 Message sent")
            
            # Open terminal to see if message executed
            print("🖥️ Opening terminal...")
            try:
                terminal_btn = await page.wait_for_selector('button:has-text("Terminal")', timeout=3000)
                await terminal_btn.click()
                await page.wait_for_timeout(3000)
                print("✅ Terminal opened")
            except:
                print("⚠️ Could not open terminal")
            
            # Final screenshot
            await page.screenshot(path='simple-04-terminal-final.png', full_page=True)
            print("📸 Final terminal screenshot")
            
            # Check for command execution in terminal
            terminal_text = await page.evaluate("""
                () => {
                    const terminal = document.querySelector('.xterm-screen');
                    return terminal ? terminal.textContent : '';
                }
            """)
            
            if "Hello from GUI test" in terminal_text:
                print("✅ SUCCESS: Command executed! Output found in terminal.")
            elif test_message in terminal_text:
                print("⚠️ PARTIAL: Command visible but may not have executed")
            else:
                print("❌ ISSUE: Command not found in terminal")
                print(f"📋 Terminal content preview: {terminal_text[:200]}...")
            
            print("\n📋 Screenshots saved:")
            print("   - simple-01-loaded.png")
            print("   - simple-02-message-typed.png") 
            print("   - simple-03-message-sent.png")
            print("   - simple-04-terminal-final.png")
            
            # Keep browser open for inspection
            await page.wait_for_timeout(5000)
            
        except Exception as e:
            print(f"❌ Test failed: {e}")
            await page.screenshot(path='simple-error.png', full_page=True)
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(test_enter_key_simple())
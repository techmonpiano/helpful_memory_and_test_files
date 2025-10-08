#!/usr/bin/env python3

"""
Classic Interactive Playwright Script - The Gold Standard
Perfect for debugging, testing, and watching browser automation in real-time
"""

import asyncio
from playwright.async_api import async_playwright
import sys

async def interactive_playwright_session():
    """
    Classic interactive Playwright session with full visibility and control
    """
    print("🎭 CLASSIC INTERACTIVE PLAYWRIGHT - Gold Standard Script")
    print("   Features: Visible browser + DevTools + User interaction + Real-time debugging")
    
    async with async_playwright() as p:
        # Launch browser with maximum visibility and debugging options
        browser = await p.chromium.launch(
            headless=False,           # Always visible
            devtools=True,           # Open DevTools automatically
            slow_mo=500,             # Slow down operations for visibility (500ms delay)
            args=[
                '--start-maximized',      # Start maximized
                '--disable-web-security', # Allow cross-origin requests (for testing)
                '--disable-features=TranslateUI', # Disable translate popups
                '--no-first-run',         # Skip first-run setup
            ]
        )
        
        # Create new page with standard desktop viewport
        page = await browser.new_page()
        await page.set_viewport_size({'width': 1920, 'height': 1080})
        
        # Enable console logging for debugging
        page.on("console", lambda msg: print(f"🖥️  CONSOLE: {msg.text}"))
        page.on("pageerror", lambda error: print(f"❌ PAGE ERROR: {error}"))
        
        try:
            print("\n📂 Phase 1: Navigation and Setup")
            print("=" * 50)
            
            # Navigate to target URL
            url = input("Enter URL to visit (or press Enter for localhost:8000): ").strip()
            if not url:
                url = "http://localhost:8000"
            
            print(f"🌐 Navigating to: {url}")
            response = await page.goto(url, wait_until='networkidle', timeout=30000)
            print(f"✅ Page loaded with status: {response.status}")
            
            # Wait for page to stabilize
            await page.wait_for_timeout(2000)
            
            print("\n🎯 Phase 2: Interactive Commands")
            print("=" * 50)
            print("Available commands:")
            print("  'click SELECTOR' - Click an element")
            print("  'type SELECTOR TEXT' - Type text into element")
            print("  'eval CODE' - Execute JavaScript")
            print("  'screenshot' - Take screenshot")
            print("  'goto URL' - Navigate to new URL")
            print("  'wait TIME' - Wait for specified seconds")
            print("  'find TEXT' - Find elements containing text")
            print("  'help' - Show this help")
            print("  'quit' - Close browser and exit")
            print("\nBrowser will stay open until you type 'quit'")
            
            # Interactive command loop
            while True:
                try:
                    command = input("\n🎭 Command: ").strip().lower()
                    
                    if command == 'quit' or command == 'exit':
                        print("👋 Closing browser...")
                        break
                    
                    elif command == 'help':
                        print("📋 Commands: click, type, eval, screenshot, goto, wait, find, quit")
                    
                    elif command == 'screenshot':
                        filename = f"/home/user1/shawndev1/helpful_memory_and_test_files/playwright_screenshot_{await page.evaluate('Date.now()')}.jpg"
                        await page.screenshot(path=filename, type='jpeg', quality=80)
                        print(f"📸 Screenshot saved: {filename}")
                    
                    elif command.startswith('click '):
                        selector = command[6:].strip()
                        try:
                            await page.click(selector, timeout=5000)
                            print(f"✅ Clicked: {selector}")
                        except Exception as e:
                            print(f"❌ Click failed: {e}")
                    
                    elif command.startswith('type '):
                        parts = command[5:].strip().split(' ', 1)
                        if len(parts) >= 2:
                            selector, text = parts[0], parts[1]
                            try:
                                await page.fill(selector, text)
                                print(f"✅ Typed '{text}' into: {selector}")
                            except Exception as e:
                                print(f"❌ Type failed: {e}")
                        else:
                            print("❌ Usage: type SELECTOR TEXT")
                    
                    elif command.startswith('eval '):
                        code = command[5:].strip()
                        try:
                            result = await page.evaluate(code)
                            print(f"📊 Result: {result}")
                        except Exception as e:
                            print(f"❌ Eval failed: {e}")
                    
                    elif command.startswith('goto '):
                        new_url = command[5:].strip()
                        try:
                            response = await page.goto(new_url, wait_until='networkidle')
                            print(f"✅ Navigated to: {new_url} (status: {response.status})")
                        except Exception as e:
                            print(f"❌ Navigation failed: {e}")
                    
                    elif command.startswith('wait '):
                        try:
                            seconds = float(command[5:].strip())
                            print(f"⏳ Waiting {seconds} seconds...")
                            await page.wait_for_timeout(int(seconds * 1000))
                            print("✅ Wait completed")
                        except ValueError:
                            print("❌ Usage: wait SECONDS (e.g., wait 2.5)")
                    
                    elif command.startswith('find '):
                        text = command[5:].strip()
                        try:
                            elements = await page.query_selector_all(f"text={text}")
                            print(f"🔍 Found {len(elements)} elements containing '{text}'")
                            for i, el in enumerate(elements[:5]):  # Show first 5
                                tag = await el.evaluate('el => el.tagName.toLowerCase()')
                                print(f"   {i+1}. <{tag}>")
                        except Exception as e:
                            print(f"❌ Find failed: {e}")
                    
                    elif command.strip() == '':
                        continue  # Empty command, just continue
                    
                    else:
                        print(f"❓ Unknown command: {command}")
                        print("   Type 'help' for available commands")
                
                except KeyboardInterrupt:
                    print("\n🛑 Interrupted by user")
                    break
                except Exception as e:
                    print(f"❌ Command error: {e}")
        
        except KeyboardInterrupt:
            print("\n🛑 Session interrupted by user")
        except Exception as e:
            print(f"❌ Session error: {e}")
            import traceback
            traceback.print_exc()
        finally:
            print("\n🔚 Closing browser...")
            await browser.close()
            print("✅ Browser closed successfully")

# Alternative: Quick debugging function for specific tasks
async def quick_debug_session(url, debug_task=None):
    """
    Quick debugging session for specific tasks
    """
    print(f"🚀 QUICK DEBUG SESSION: {url}")
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, devtools=True, slow_mo=300)
        page = await browser.new_page()
        
        # Console logging
        page.on("console", lambda msg: print(f"CONSOLE: {msg.text}"))
        
        try:
            # Navigate
            await page.goto(url, wait_until='networkidle')
            
            # Execute custom debug task if provided
            if debug_task:
                print("🔧 Executing custom debug task...")
                result = await debug_task(page)
                print(f"📊 Debug result: {result}")
            
            # Keep browser open for manual inspection
            print("🔒 Browser open for inspection. Press Ctrl+C to close.")
            await asyncio.sleep(300)  # 5 minutes
            
        except KeyboardInterrupt:
            print("✅ Debug session completed")
        finally:
            await browser.close()

# Example debug task function
async def example_debug_task(page):
    """Example debug task - analyze page structure"""
    return await page.evaluate('''() => {
        return {
            title: document.title,
            url: window.location.href,
            elementCount: document.querySelectorAll('*').length,
            hasJQuery: typeof jQuery !== 'undefined',
            viewport: {
                width: window.innerWidth,
                height: window.innerHeight
            }
        };
    }''')

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Quick mode with URL argument
        url = sys.argv[1]
        asyncio.run(quick_debug_session(url, example_debug_task))
    else:
        # Full interactive mode
        asyncio.run(interactive_playwright_session())
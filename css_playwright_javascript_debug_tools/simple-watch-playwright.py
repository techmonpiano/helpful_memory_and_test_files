#!/usr/bin/env python3

"""
Simple Watch Playwright - The Easiest Interactive Script
Perfect for watching browser automation with minimal setup
"""

import asyncio
from playwright.async_api import async_playwright

async def simple_watch_session():
    """
    The simplest, most effective "watch me work" Playwright script
    """
    print("👀 SIMPLE WATCH PLAYWRIGHT - Easy Interactive Mode")
    print("   You can watch everything I do in the browser!")
    
    async with async_playwright() as p:
        # Perfect settings for watching
        browser = await p.chromium.launch(
            headless=False,      # Visible browser
            devtools=True,       # DevTools open
            slow_mo=1000,        # 1 second delay between actions (easy to follow)
        )
        
        page = await browser.new_page()
        await page.set_viewport_size({'width': 1400, 'height': 900})
        
        # Show console messages
        page.on("console", lambda msg: print(f"🖥️  {msg.text}"))
        
        try:
            print("\n🌐 Where should I go?")
            url = input("Enter URL (or Enter for localhost:8000): ").strip()
            if not url:
                url = "http://localhost:8000"
            
            print(f"\n📂 Step 1: Going to {url}")
            await page.goto(url)
            await page.wait_for_timeout(2000)
            print("✅ Page loaded!")
            
            print("\n🎯 Step 2: What should I do?")
            print("Watch the browser - I'll perform some common actions...")
            
            # Common debugging actions you can watch
            print("\n🔍 Analyzing page structure...")
            page_info = await page.evaluate('''() => {
                return {
                    title: document.title,
                    elementsCount: document.querySelectorAll('*').length,
                    imagesCount: document.querySelectorAll('img').length,
                    formsCount: document.querySelectorAll('form').length,
                    hasJQuery: typeof jQuery !== 'undefined'
                };
            }''')
            
            print(f"📄 Title: {page_info['title']}")
            print(f"🔢 Elements: {page_info['elementsCount']}")
            print(f"🖼️  Images: {page_info['imagesCount']}")
            print(f"📝 Forms: {page_info['formsCount']}")
            print(f"💎 jQuery: {'Yes' if page_info['hasJQuery'] else 'No'}")
            
            # Take a screenshot you can see
            print("\n📸 Taking screenshot...")
            await page.screenshot(
                path='/home/user1/shawndev1/helpful_memory_and_test_files/watch_session.jpg',
                type='jpeg',
                quality=80
            )
            print("✅ Screenshot saved: watch_session.jpg")
            
            # Interactive part
            print("\n🎮 Interactive Mode - What do you want me to do?")
            print("Commands: 'scroll', 'click SELECTOR', 'js CODE', 'screenshot', 'done'")
            
            while True:
                command = input("\n👀 What next? ").strip().lower()
                
                if command == 'done':
                    break
                elif command == 'scroll':
                    print("📜 Scrolling down...")
                    await page.evaluate("window.scrollBy(0, 500)")
                    await page.wait_for_timeout(1000)
                elif command == 'screenshot':
                    timestamp = await page.evaluate("Date.now()")
                    filename = f'/home/user1/shawndev1/helpful_memory_and_test_files/watch_{timestamp}.jpg'
                    await page.screenshot(path=filename, type='jpeg', quality=80)
                    print(f"📸 Screenshot: {filename}")
                elif command.startswith('click '):
                    selector = command[6:]
                    try:
                        print(f"👆 Clicking: {selector}")
                        await page.click(selector)
                        await page.wait_for_timeout(1000)
                        print("✅ Clicked!")
                    except Exception as e:
                        print(f"❌ Click failed: {e}")
                elif command.startswith('js '):
                    code = command[3:]
                    try:
                        print(f"⚡ Running: {code}")
                        result = await page.evaluate(code)
                        print(f"📊 Result: {result}")
                    except Exception as e:
                        print(f"❌ JS failed: {e}")
                else:
                    print("❓ Try: scroll, click SELECTOR, js CODE, screenshot, done")
            
            print("\n🎉 Session complete! Browser will stay open for 30 more seconds...")
            await page.wait_for_timeout(30000)
            
        except KeyboardInterrupt:
            print("\n🛑 Stopped by user")
        finally:
            await browser.close()
            print("👋 Browser closed")

if __name__ == "__main__":
    asyncio.run(simple_watch_session())
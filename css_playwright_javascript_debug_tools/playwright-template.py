#!/usr/bin/env python3

"""
Playwright Template - Copy this for any automation task
The most reliable, battle-tested pattern
"""

import asyncio
from playwright.async_api import async_playwright

async def main():
    """
    Perfect Playwright template - copy and modify this function
    """
    print("🎭 PLAYWRIGHT TEMPLATE - Universal Pattern")
    
    async with async_playwright() as p:
        # Gold standard browser launch settings
        browser = await p.chromium.launch(
            headless=False,           # Set to True for production
            devtools=True,           # Set to False for production  
            slow_mo=500,             # Remove for production speed
        )
        
        # Create page with proper settings
        page = await browser.new_page()
        page.set_default_timeout(30000)  # 30 second timeout
        page.set_default_navigation_timeout(45000)  # 45 second navigation
        await page.set_viewport_size({'width': 1920, 'height': 1080})
        
        # Optional: Add logging
        page.on("console", lambda msg: print(f"CONSOLE: {msg.text}"))
        page.on("pageerror", lambda error: print(f"ERROR: {error}"))
        
        try:
            # =================
            # YOUR CODE HERE
            # =================
            
            print("🌐 Navigating to page...")
            await page.goto("http://localhost:8000")
            
            print("⏳ Waiting for page to load...")
            await page.wait_for_load_state('networkidle')
            
            print("🔍 Doing something...")
            # Example actions:
            # await page.click("button")
            # await page.fill("input", "text")
            # result = await page.evaluate("document.title")
            # await page.screenshot(path="screenshot.jpg")
            
            # Wait for manual inspection (remove for automation)
            print("🔒 Browser staying open for inspection...")
            await page.wait_for_timeout(60000)  # 1 minute
            
        except Exception as e:
            print(f"❌ Error: {e}")
            # Take error screenshot
            await page.screenshot(path="error_screenshot.jpg")
            raise
        finally:
            await browser.close()

# Example: CSS Debugging Function
async def debug_css_issues(url="http://localhost:8000"):
    """
    Example: Debug CSS issues on a page
    """
    print(f"🔍 CSS DEBUGGING: {url}")
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, devtools=True)
        page = await browser.new_page()
        
        try:
            await page.goto(url)
            
            # Inject CSS debugging
            css_issues = await page.evaluate('''() => {
                const issues = [];
                document.querySelectorAll('*').forEach(el => {
                    const rect = el.getBoundingClientRect();
                    if (rect.left < 0 || rect.right > window.innerWidth) {
                        issues.push({
                            tag: el.tagName,
                            id: el.id,
                            class: el.className,
                            left: Math.round(rect.left),
                            width: Math.round(rect.width)
                        });
                    }
                });
                return issues.slice(0, 5);
            }''')
            
            print(f"Found {len(css_issues)} CSS issues:")
            for issue in css_issues:
                print(f"  {issue['tag']} - left: {issue['left']}px, width: {issue['width']}px")
            
            await page.screenshot(path="css_debug.jpg")
            print("Screenshot saved: css_debug.jpg")
            
            # Keep open for inspection
            await page.wait_for_timeout(30000)
            
        finally:
            await browser.close()

# Example: Form Testing Function  
async def test_form_interaction():
    """
    Example: Test form interactions
    """
    print("📝 FORM TESTING")
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=1000)
        page = await browser.new_page()
        
        try:
            await page.goto("http://localhost:8000")
            
            # Find and interact with forms
            forms = await page.query_selector_all("form")
            print(f"Found {len(forms)} forms")
            
            # Example form interactions
            # await page.fill("input[name='email']", "test@example.com")
            # await page.fill("input[name='password']", "password123")
            # await page.click("button[type='submit']")
            
            await page.wait_for_timeout(10000)
            
        finally:
            await browser.close()

if __name__ == "__main__":
    # Run the main template
    asyncio.run(main())
    
    # Or run specific examples:
    # asyncio.run(debug_css_issues())
    # asyncio.run(test_form_interaction())
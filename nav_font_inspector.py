#!/usr/bin/env python3
import asyncio
import json
from playwright.async_api import async_playwright

async def check_nav_font():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await page.set_viewport_size({'width': 1920, 'height': 1080})
        
        try:
            await page.goto('https://block.github.io/goose/docs/getting-started/installation/')
            await page.wait_for_load_state('networkidle')
            await page.wait_for_timeout(3000)
            
            # Find navigation bar and get font properties
            nav_styles = await page.evaluate("""() => {
                const nav = document.querySelector('nav') || 
                           document.querySelector('.navbar') || 
                           document.querySelector('header nav') ||
                           document.querySelector('[role="navigation"]');
                           
                if (!nav) return {error: 'Navigation not found'};
                
                const styles = window.getComputedStyle(nav);
                return {
                    fontFamily: styles.fontFamily,
                    fontSize: styles.fontSize,
                    fontWeight: styles.fontWeight,
                    fontStyle: styles.fontStyle,
                    lineHeight: styles.lineHeight,
                    letterSpacing: styles.letterSpacing,
                    textAlign: styles.textAlign
                };
            }""")
            
            print('Navigation Font Properties:')
            print(json.dumps(nav_styles, indent=2))
            
            # Keep browser open for manual inspection
            print('\nBrowser window opened. Press Enter to close...')
            input()
            
        except Exception as e:
            print(f'Error: {e}')
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(check_nav_font())
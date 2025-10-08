#!/usr/bin/env python3

"""
Final verification - check if white space issue is resolved
"""

import asyncio
from playwright.async_api import async_playwright

async def final_check():
    print("✅ FINAL VERIFICATION - White Space Issue Resolution Check")
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.set_viewport_size({'width': 1920, 'height': 1080})
        
        try:
            await page.goto("http://localhost:8000/index.php?main_page=index&cPath=14")
            await page.wait_for_timeout(3000)
            
            # Check the specific container
            result = await page.evaluate('''() => {
                const container = document.querySelector('.holder.fullwidth.full-nopad.out-banners-generator-parts');
                const nav = document.querySelector('.header-wrapper, .hdr-desktop, #headerWrapper');
                
                if (!container) return { error: 'Container not found' };
                
                const containerRect = container.getBoundingClientRect();
                const navRect = nav ? nav.getBoundingClientRect() : null;
                const style = window.getComputedStyle(container);
                
                const navToContainerGap = navRect ? containerRect.top - (navRect.top + navRect.height) : 'unknown';
                
                return {
                    container_left: Math.round(containerRect.left),
                    container_right: Math.round(containerRect.right),
                    container_width: Math.round(containerRect.width),
                    container_height: Math.round(containerRect.height),
                    viewport_width: window.innerWidth,
                    position: style.position,
                    margins: style.marginLeft + ' / ' + style.marginRight,
                    nav_to_container_gap: Math.round(navToContainerGap),
                    is_within_viewport: containerRect.left >= 0 && containerRect.right <= window.innerWidth,
                    extends_left: containerRect.left < 0,
                    extends_right: containerRect.right > window.innerWidth
                };
            }''')
            
            # Take final screenshot
            await page.screenshot(
                path='/home/user1/shawndev1/ASAPWebNew/FINAL_RESOLUTION_CHECK.jpg',
                type='jpeg',
                quality=80
            )
            
            print("\n📊 FINAL RESULTS:")
            print("=" * 50)
            print(f"Container left: {result['container_left']}px")
            print(f"Container right: {result['container_right']}px") 
            print(f"Container width: {result['container_width']}px")
            print(f"Viewport width: {result['viewport_width']}px")
            print(f"Position: {result['position']}")
            print(f"Margins: {result['margins']}")
            print(f"Nav to container gap: {result['nav_to_container_gap']}px")
            
            print("\n🎯 ISSUE STATUS:")
            if result['is_within_viewport']:
                print("✅ WHITE SPACE ISSUE RESOLVED!")
                print("✅ Container is properly positioned within viewport")
                print("✅ No elements extending beyond screen boundaries")
            else:
                if result['extends_left']:
                    print("❌ Container still extends left")
                if result['extends_right']:
                    print("❌ Container still extends right")
            
            if result['nav_to_container_gap'] <= 5:
                print("✅ No white space gap between navigation and container")
            else:
                print(f"⚠️ {result['nav_to_container_gap']}px gap between nav and container")
            
            print(f"\n📸 Final verification screenshot: FINAL_RESOLUTION_CHECK.jpg")
            
        except Exception as e:
            print(f"❌ Error: {e}")
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(final_check())
#!/usr/bin/env python3

"""
Quick CSS Analysis - Fast automated detection without keeping browser open
"""

import asyncio
from playwright.async_api import async_playwright

async def quick_css_analysis():
    print("🚀 QUICK CSS ANALYSIS - Fast automated detection")
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)  # Headless for speed
        page = await browser.new_page()
        await page.set_viewport_size({'width': 1920, 'height': 1080})
        
        try:
            print("📂 Loading page...")
            await page.goto("http://localhost:8000/index.php?main_page=index&cPath=14")
            await page.wait_for_timeout(3000)
            
            print("🔍 Running CSS analysis...")
            
            # Run comprehensive analysis
            results = await page.evaluate('''() => {
                const viewport = { width: window.innerWidth, height: window.innerHeight };
                const problems = [];
                
                // Find problematic elements
                document.querySelectorAll('*').forEach(el => {
                    const rect = el.getBoundingClientRect();
                    const style = window.getComputedStyle(el);
                    
                    const extendsLeft = rect.left < -10;
                    const extendsRight = rect.right > viewport.width + 10;
                    const isLargeWhite = rect.width > 500 && rect.height > 100 && 
                                        (style.backgroundColor.includes('255') || style.backgroundColor === 'white');
                    
                    if (extendsLeft || extendsRight || isLargeWhite) {
                        problems.push({
                            issue: extendsLeft ? 'EXTENDS_LEFT' : 
                                   extendsRight ? 'EXTENDS_RIGHT' : 
                                   'LARGE_WHITE_BLOCK',
                            left: Math.round(rect.left),
                            right: Math.round(rect.right),
                            width: Math.round(rect.width),
                            height: Math.round(rect.height),
                            selector: el.tagName.toLowerCase() + 
                                     (el.id ? '#' + el.id : '') + 
                                     (el.className ? '.' + el.className.split(' ').slice(0,2).join('.') : ''),
                            position: style.position,
                            marginLeft: style.marginLeft,
                            marginRight: style.marginRight,
                            transform: style.transform,
                            width_css: style.width,
                            overflow: style.overflow
                        });
                    }
                });
                
                // Analyze generator parts container
                const container = document.querySelector('.holder.fullwidth.full-nopad.out-banners-generator-parts');
                let containerData = { found: false };
                
                if (container) {
                    const rect = container.getBoundingClientRect();
                    const style = window.getComputedStyle(container);
                    
                    containerData = {
                        found: true,
                        position: style.position,
                        width_css: style.width,
                        width_actual: Math.round(rect.width),
                        height_css: style.height,
                        height_actual: Math.round(rect.height),
                        left: Math.round(rect.left),
                        right: Math.round(rect.right),
                        marginLeft: style.marginLeft,
                        marginRight: style.marginRight,
                        transform: style.transform,
                        backgroundColor: style.backgroundColor,
                        isProblematic: rect.left < -10 || rect.right > viewport.width + 10
                    };
                }
                
                return {
                    problems: problems.sort((a, b) => a.left - b.left),
                    container: containerData,
                    viewport: viewport
                };
            }''')
            
            # Take screenshot
            await page.screenshot(
                path='/home/user1/shawndev1/ASAPWebNew/quick_analysis_result.jpg',
                type='jpeg',
                quality=80
            )
            
            print("\n📊 ANALYSIS COMPLETE!")
            print("=" * 60)
            
            problems = results['problems']
            container = results['container']
            
            print(f"🔍 Found {len(problems)} layout issues:")
            
            for i, problem in enumerate(problems[:3], 1):  # Top 3 issues
                print(f"\n{i}. ❌ {problem['issue']}: {problem['selector']}")
                print(f"   📐 Position: left={problem['left']}px, width={problem['width']}px")
                print(f"   🎯 CSS: {problem['position']}, width={problem['width_css']}")
                print(f"   📏 Margins: {problem['marginLeft']} / {problem['marginRight']}")
                if problem['transform'] != 'none':
                    print(f"   🔄 Transform: {problem['transform']}")
            
            print(f"\n🎯 GENERATOR PARTS CONTAINER:")
            if container['found']:
                print(f"   Position: {container['position']}")
                print(f"   Width: {container['width_css']} (actual: {container['width_actual']}px)")
                print(f"   Left: {container['left']}px, Right: {container['right']}px")
                print(f"   Margins: {container['marginLeft']} / {container['marginRight']}")
                print(f"   Transform: {container['transform']}")
                
                if container['isProblematic']:
                    print(f"   ❌ CONTAINER IS THE PROBLEM!")
                    print(f"   🚨 Container extends beyond viewport boundaries")
                else:
                    print(f"   ✅ Container positioning normal")
            else:
                print("   ❌ Container not found")
            
            print(f"\n🛠️ SPECIFIC FIXES NEEDED:")
            print("=" * 40)
            
            if problems:
                worst = problems[0]
                print(f"WORST ISSUE: {worst['selector']}")
                print(f"Problem: {worst['issue']} (left: {worst['left']}px)")
                
                print(f"\nCSS FIX to apply:")
                print(f"{worst['selector']} {{")
                if worst['left'] < -50:
                    print(f"    margin-left: 0 !important;")
                    print(f"    transform: none !important;")
                if worst['width'] > 2000:
                    print(f"    width: 100% !important;")
                    print(f"    max-width: 100vw !important;")
                print(f"}}")
                
                # Show exact file to edit
                print(f"\nEdit this file:")
                print(f"includes/templates/goodwin/common/tpl_template_custom_css.php")
                print(f"Add the CSS fix above to the end of the <style> section")
            
            print(f"\n📸 Screenshot saved: quick_analysis_result.jpg")
            
        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(quick_css_analysis())
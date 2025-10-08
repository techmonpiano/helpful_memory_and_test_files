#!/usr/bin/env python3

"""
Playwright CSS Debug - Automated white block detection with DevTools
"""

import asyncio
from playwright.async_api import async_playwright
import json

async def playwright_css_debug():
    print("🚀 PLAYWRIGHT CSS DEBUG - Automated Analysis")
    print("   Opening with DevTools and running comprehensive CSS analysis...")
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, devtools=True)
        page = await browser.new_page()
        await page.set_viewport_size({'width': 1920, 'height': 1080})
        
        try:
            print("\n📂 Loading Generator Parts page...")
            await page.goto("http://localhost:8000/index.php?main_page=index&cPath=14")
            await page.wait_for_timeout(5000)
            
            print("🔍 Injecting CSS debug analysis...")
            
            # Inject comprehensive CSS debug script
            analysis_results = await page.evaluate('''() => {
                // CSS WHITE BLOCK DETECTOR - Automated Version
                const problems = [];
                const viewport = { width: window.innerWidth, height: window.innerHeight };
                
                document.querySelectorAll('*').forEach(el => {
                    const rect = el.getBoundingClientRect();
                    const style = window.getComputedStyle(el);
                    
                    // Check for layout issues
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
                                     (el.className ? '.' + el.className.split(' ').slice(0,3).join('.') : ''),
                            position: style.position,
                            marginLeft: style.marginLeft,
                            marginRight: style.marginRight,
                            transform: style.transform,
                            overflow: style.overflow,
                            width_css: style.width,
                            backgroundColor: style.backgroundColor
                        });
                        
                        // Highlight problematic elements
                        el.style.outline = '4px solid #ff6b6b';
                        el.style.outlineOffset = '2px';
                        el.style.zIndex = '999999';
                    }
                });
                
                // Sort by severity
                problems.sort((a, b) => {
                    if (a.left < b.left) return -1;
                    if (a.right > b.right) return -1;
                    return 0;
                });
                
                // Generator parts container analysis
                const container = document.querySelector('.holder.fullwidth.full-nopad.out-banners-generator-parts');
                let containerAnalysis = null;
                
                if (container) {
                    const rect = container.getBoundingClientRect();
                    const style = window.getComputedStyle(container);
                    
                    containerAnalysis = {
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
                        overflow: style.overflow,
                        isProblematic: rect.left < -10 || rect.right > viewport.width + 10
                    };
                    
                    // Highlight container
                    container.style.outline = '6px solid #ff0000';
                    container.style.outlineOffset = '4px';
                    container.scrollIntoView({ behavior: 'smooth', block: 'center' });
                } else {
                    containerAnalysis = { found: false };
                }
                
                return {
                    problems: problems,
                    containerAnalysis: containerAnalysis,
                    viewport: viewport,
                    problemCount: problems.length
                };
            }''')
            
            print("📊 ANALYSIS RESULTS:")
            print("=" * 60)
            
            # Display problems
            problems = analysis_results.get('problems', [])
            container_analysis = analysis_results.get('containerAnalysis', {})
            
            print(f"🔍 Found {len(problems)} layout issues:")
            
            for i, problem in enumerate(problems[:5], 1):  # Show top 5
                print(f"\n{i}. {problem['issue']}: {problem['selector']}")
                print(f"   📐 Position: left={problem['left']}px, width={problem['width']}px")
                print(f"   🎯 CSS: position={problem['position']}, width={problem['width_css']}")
                print(f"   📏 Margins: {problem['marginLeft']} / {problem['marginRight']}")
                if problem['transform'] != 'none':
                    print(f"   🔄 Transform: {problem['transform']}")
            
            # Container analysis
            print(f"\n🎯 GENERATOR PARTS CONTAINER:")
            if container_analysis.get('found'):
                print(f"   📍 Position: {container_analysis['position']}")
                print(f"   📐 Width: {container_analysis['width_css']} (actual: {container_analysis['width_actual']}px)")
                print(f"   📏 Height: {container_analysis['height_css']} (actual: {container_analysis['height_actual']}px)")
                print(f"   ⬅️ Left: {container_analysis['left']}px")
                print(f"   📦 Margins: {container_analysis['marginLeft']} / {container_analysis['marginRight']}")
                print(f"   🔄 Transform: {container_analysis['transform']}")
                print(f"   🎨 Background: {container_analysis['backgroundColor']}")
                
                if container_analysis['isProblematic']:
                    print(f"   ❌ CONTAINER IS CAUSING THE ISSUE!")
                else:
                    print(f"   ✅ Container positioning looks normal")
            else:
                print("   ❌ Container not found!")
            
            # Take screenshot with highlights
            await page.screenshot(
                path='/home/user1/shawndev1/ASAPWebNew/css_debug_highlighted.jpg',
                type='jpeg',
                quality=80,
                full_page=True
            )
            print(f"\n📸 Screenshot saved with highlighted elements: css_debug_highlighted.jpg")
            
            # Generate fix recommendations
            print(f"\n🛠️ RECOMMENDED FIXES:")
            print("=" * 40)
            
            if container_analysis.get('found') and container_analysis.get('isProblematic'):
                print("🎯 CONTAINER FIXES:")
                
                if 'calc(' in container_analysis.get('marginLeft', ''):
                    print("1. margin-left calc() is extending beyond viewport")
                    print("   Fix: margin-left: 0 !important;")
                
                if container_analysis.get('width_css') == '100vw':
                    print("2. width: 100vw is too wide with margins")
                    print("   Fix: width: 100% !important;")
                
                if container_analysis.get('transform', 'none') != 'none':
                    print("3. Transform is shifting the element")
                    print("   Fix: transform: none !important;")
                
                if container_analysis.get('left', 0) < -10:
                    print("4. Element extending left beyond viewport")
                    print("   Fix: margin-left: 0 !important; transform: none !important;")
            
            # Show the worst problem
            if problems:
                worst = problems[0]
                print(f"\n❌ WORST ISSUE: {worst['issue']} - {worst['selector']}")
                print(f"   Left: {worst['left']}px, Width: {worst['width']}px")
                
                # Provide specific fix for worst issue
                print(f"\n🔧 QUICK FIX FOR WORST ISSUE:")
                print(f"   Apply this CSS to fix {worst['selector']}:")
                print(f"   {worst['selector']} {{")
                if worst['left'] < -10:
                    print(f"       margin-left: 0 !important;")
                    print(f"       transform: none !important;")
                if worst['width'] > 1920:
                    print(f"       width: 100% !important;")
                    print(f"       max-width: 100vw !important;")
                print(f"   }}")
            
            print(f"\n🔒 Browser staying open for DevTools inspection...")
            print("   - Elements are highlighted with red outlines")
            print("   - Container is highlighted with thick red outline")
            print("   - Use DevTools to inspect the highlighted elements")
            print("   - Press Ctrl+C when done")
            
            # Keep browser open for inspection
            await asyncio.sleep(300)  # 5 minutes
            
        except KeyboardInterrupt:
            print("\n✅ CSS debug analysis complete")
        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(playwright_css_debug())
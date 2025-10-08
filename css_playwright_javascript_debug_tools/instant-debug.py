#!/usr/bin/env python3

"""
Instant CSS debugging - Opens browser with devtools and injects analysis script
"""

import asyncio
from playwright.async_api import async_playwright

async def instant_debug():
    print("🚀 INSTANT CSS DEBUGGING - Opening with DevTools")
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, devtools=True)
        page = await browser.new_page()
        
        try:
            print("📂 Loading Generator Parts page...")
            await page.goto("http://localhost:8000/index.php?main_page=index&cPath=14")
            await page.wait_for_timeout(3000)
            
            # Inject our CSS debug analyzer
            await page.add_script_tag(content='''
                // Quick White Block Detector
                (function() {
                    console.log('%c🔍 INSTANT CSS DEBUG ACTIVE', 'color: #ff6b6b; font-size: 18px; font-weight: bold;');
                    
                    // Find elements extending beyond viewport or with large white backgrounds
                    const problems = [];
                    document.querySelectorAll('*').forEach(el => {
                        const rect = el.getBoundingClientRect();
                        const style = window.getComputedStyle(el);
                        
                        if (rect.left < -50 || rect.right > window.innerWidth + 50 || 
                            (rect.width > 500 && style.backgroundColor.includes('255'))) {
                            problems.push({
                                element: el,
                                issue: rect.left < -50 ? 'EXTENDS LEFT' : 
                                       rect.right > window.innerWidth + 50 ? 'EXTENDS RIGHT' : 
                                       'LARGE WHITE',
                                left: Math.round(rect.left),
                                right: Math.round(rect.right),
                                width: Math.round(rect.width),
                                height: Math.round(rect.height),
                                selector: el.tagName.toLowerCase() + 
                                         (el.id ? '#' + el.id : '') + 
                                         (el.className ? '.' + el.className.split(' ').join('.') : ''),
                                position: style.position,
                                marginLeft: style.marginLeft,
                                marginRight: style.marginRight,
                                transform: style.transform
                            });
                        }
                    });
                    
                    console.log('%c⚠️ PROBLEM ELEMENTS FOUND:', 'color: #ff6b6b; font-size: 16px;');
                    problems.forEach((prob, i) => {
                        console.log(`%c${i+1}. ${prob.issue}: ${prob.selector}`, 'color: #ffa500; font-weight: bold;');
                        console.log(`   Left: ${prob.left}px, Width: ${prob.width}px, Position: ${prob.position}`);
                        console.log(`   Margins: ${prob.marginLeft} / ${prob.marginRight}`);
                        if (prob.transform !== 'none') console.log(`   Transform: ${prob.transform}`);
                        console.log('   Element:', prob.element);
                        console.log('---');
                        
                        // Highlight problematic elements
                        prob.element.style.outline = '3px solid #ff6b6b';
                        prob.element.style.outlineOffset = '2px';
                    });
                    
                    // Focus on the most problematic element
                    if (problems.length > 0) {
                        const worst = problems[0];
                        worst.element.scrollIntoView({ behavior: 'smooth', block: 'center' });
                        console.log('%c📍 WORST ELEMENT HIGHLIGHTED AND SCROLLED TO', 'color: #ff6b6b; font-size: 14px;');
                    }
                    
                    // Generator parts container analysis
                    const container = document.querySelector('.holder.fullwidth.full-nopad.out-banners-generator-parts');
                    if (container) {
                        const rect = container.getBoundingClientRect();
                        const style = window.getComputedStyle(container);
                        
                        console.log('%c🎯 GENERATOR PARTS CONTAINER ANALYSIS:', 'color: #4ecdc4; font-size: 16px;');
                        console.log('Position:', style.position);
                        console.log('Width:', style.width, '| Actual:', Math.round(rect.width) + 'px');
                        console.log('Height:', style.height, '| Actual:', Math.round(rect.height) + 'px');
                        console.log('Left:', Math.round(rect.left) + 'px');
                        console.log('Margins:', style.marginLeft, '/', style.marginRight);
                        console.log('Transform:', style.transform);
                        console.log('Background:', style.backgroundColor);
                        console.log('Container element:', container);
                    }
                    
                    return problems.length;
                })();
            ''')
            
            # Get the analysis results
            problem_count = await page.evaluate('window.problemCount || 0')
            
            print(f"\n📊 INSTANT ANALYSIS COMPLETE:")
            print(f"   🔍 Check browser console for detailed analysis")
            print(f"   ⚠️ Found issues - see highlighted elements in page")
            print(f"   🎯 Generator parts container analyzed")
            
            print(f"\n🔒 Browser staying open for DevTools inspection...")
            print("   Use DevTools Elements tab to inspect highlighted elements")
            print("   Check Console tab for detailed analysis")
            print("   Press Ctrl+C when done")
            
            # Keep browser open
            await asyncio.sleep(300)
            
        except KeyboardInterrupt:
            print("\n✅ Debug session complete")
        except Exception as e:
            print(f"❌ Error: {e}")
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(instant_debug())
#!/usr/bin/env python3
"""
Test cart buttons after successfully adding item via add-to-cart modal
Enhanced with comprehensive CSS debugging capabilities
"""

import asyncio
from playwright.async_api import async_playwright

async def test_cart_after_add():
    async with async_playwright() as p:
        # Launch browser with DevTools automatically opened
        browser = await p.chromium.launch(
            headless=False, 
            slow_mo=500,
            args=[
                '--auto-open-devtools-for-tabs',
                '--start-maximized',
                '--disable-web-security'  # For testing only
            ]
        )
        page = await browser.new_page()
        await page.set_viewport_size({'width': 1920, 'height': 1080})
        
        # Enable comprehensive logging
        page.on("console", lambda msg: print(f"🖥️ JS Console: {msg.text}"))
        page.on("pageerror", lambda error: print(f"❌ Page Error: {error}"))
        
        # Inject CSS debugging script for enhanced analysis
        await page.add_init_script('''
            // Track class additions that might cause "flash and misalign"
            window.debugInfo = {
                classAdditions: [],
                styleChanges: [],
                mutations: []
            };
            
            // Monitor class additions
            const originalAdd = Element.prototype.classList.add;
            Element.prototype.classList.add = function(...classes) {
                if (this.closest('.cart-pg, .shopping-cart-page')) {
                    window.debugInfo.classAdditions.push({
                        element: this.tagName + '.' + this.className,
                        classes: classes,
                        timestamp: Date.now()
                    });
                    console.log('🏷️ Class added to cart element:', classes, 'on', this.tagName);
                }
                return originalAdd.apply(this, classes);
            };
            
            // Monitor style changes
            const originalSetAttribute = Element.prototype.setAttribute;
            Element.prototype.setAttribute = function(name, value) {
                if (name === 'style' && this.closest('.cart-pg, .shopping-cart-page')) {
                    window.debugInfo.styleChanges.push({
                        element: this.tagName,
                        value: value,
                        timestamp: Date.now()
                    });
                    console.log('🎨 Style changed on cart element:', value);
                }
                return originalSetAttribute.call(this, name, value);
            };
            
            // Monitor DOM mutations
            window.observer = new MutationObserver((mutations) => {
                mutations.forEach((mutation) => {
                    if (mutation.target.closest && mutation.target.closest('.cart-pg, .shopping-cart-page')) {
                        window.debugInfo.mutations.push({
                            type: mutation.type,
                            target: mutation.target.tagName + '.' + (mutation.target.className || ''),
                            timestamp: Date.now()
                        });
                    }
                });
            });
            window.observer.observe(document.body, {
                childList: true,
                attributes: true,
                subtree: true
            });
        ''')
        
        print("🛍️ Step 1: Adding item to cart...")
        await page.goto("http://localhost:8000/index.php?main_page=product_info&cPath=9_179&products_id=94")
        await page.wait_for_selector('.submit_button, .btn--add-to-c, button.btn.button2', timeout=10000)
        
        # Click Add to Cart
        add_to_cart_button = page.locator('.submit_button, .btn--add-to-c, button.btn.button2').first
        await add_to_cart_button.click()
        
        # Wait for modal and close it
        print("⏳ Waiting for modal...")
        try:
            await page.wait_for_selector('#pzenajx-wrapper.show, .modal.show', timeout=5000)
            await page.wait_for_timeout(1000)
            await page.click('.pzenajx-close, [data-dismiss="modal"], .modal-header .close, .fancybox-close-small')
            print("✅ Modal closed")
        except:
            print("⚠️ No modal found, continuing...")
        
        print("🛒 Step 2: Navigating to shopping cart...")
        await page.goto("http://localhost:8000/index.php?main_page=shopping_cart")
        await page.wait_for_load_state('networkidle')
        
        # Take screenshot of cart with items
        timestamp = int(await page.evaluate('Date.now()'))
        await page.screenshot(path=f'cart_with_items_debug_{timestamp}.png', full_page=True)
        print(f"📸 Screenshot saved: cart_with_items_debug_{timestamp}.png")
        
        # Enhanced CSS analysis with comprehensive debugging
        css_analysis = await page.evaluate('''() => {
            const results = {};
            const buttons = document.querySelectorAll('.cart-pg .checkout-btn-modern, .shopping-cart-page .checkout-btn-modern, a[href*="empty_cart"], a[href*="checkout"]');
            
            buttons.forEach((btn, index) => {
                const computed = window.getComputedStyle(btn);
                const classes = btn.className;
                const href = btn.href || 'no-href';
                
                // Check for HTML attribute constraints
                const attributes = {};
                for (let attr of btn.attributes) {
                    attributes[attr.name] = attr.value;
                }
                
                results[`button_${index}`] = {
                    text: btn.textContent.trim(),
                    classes: classes,
                    href: href.includes('localhost') ? href.split('localhost:8000')[1] : href,
                    attributes: attributes,  // NEW: Track HTML attributes
                    styles: {
                        fontFamily: computed.fontFamily,
                        fontWeight: computed.fontWeight,
                        fontSize: computed.fontSize,
                        textTransform: computed.textTransform,
                        letterSpacing: computed.letterSpacing,
                        color: computed.color,
                        backgroundColor: computed.backgroundColor,
                        border: computed.border,
                        padding: computed.padding,
                        display: computed.display,
                        width: computed.width,  // NEW: Track width issues
                        minWidth: computed.minWidth,
                        maxWidth: computed.maxWidth,
                        position: computed.position,
                        overflow: computed.overflow  // NEW: Track overflow
                    },
                    // Layout analysis for potential issues
                    layoutIssues: [],
                    appliedRules: []
                };
                
                // Check for common layout issues
                const rect = btn.getBoundingClientRect();
                if (rect.left < -10) {
                    results[`button_${index}`].layoutIssues.push('EXTENDS_LEFT');
                }
                if (rect.right > window.innerWidth + 10) {
                    results[`button_${index}`].layoutIssues.push('EXTENDS_RIGHT');
                }
                if (rect.width < 50) {
                    results[`button_${index}`].layoutIssues.push('TOO_NARROW');
                }
                
                // Try to get matching CSS rules (enhanced from debug_css_overrides.py)
                try {
                    const sheets = Array.from(document.styleSheets);
                    sheets.forEach(sheet => {
                        try {
                            const rules = Array.from(sheet.cssRules || sheet.rules);
                            rules.forEach(rule => {
                                if (rule.selectorText && btn.matches && btn.matches(rule.selectorText)) {
                                    const ruleInfo = {
                                        selector: rule.selectorText,
                                        fontFamily: rule.style.fontFamily || 'not-set',
                                        fontWeight: rule.style.fontWeight || 'not-set',  
                                        textTransform: rule.style.textTransform || 'not-set',
                                        width: rule.style.width || 'not-set',  // NEW
                                        cssText: rule.cssText.substring(0, 200)
                                    };
                                    results[`button_${index}`].appliedRules.push(ruleInfo);
                                }
                            });
                        } catch(e) {
                            // Skip CORS restricted stylesheets
                        }
                    });
                } catch(e) {
                    results[`button_${index}`].appliedRules.push({error: e.message});
                }
            });
            
            // Also check what CSS files are loaded (enhanced)
            const cssFiles = Array.from(document.querySelectorAll('link[rel="stylesheet"]'))
                .map(link => ({
                    href: link.href.includes('localhost') ? link.href.split('localhost:8000')[1] : link.href,
                    loaded: true,
                    disabled: link.disabled  // NEW: Check if disabled
                }));
            
            results.cssFiles = cssFiles.filter(file => 
                file.href.includes('goodwin') || 
                file.href.includes('components') || 
                file.href.includes('modern') ||
                file.href.includes('user_custom')  // NEW: Include custom styles
            );
            
            // Include debug info collected by monitoring scripts
            results.debugInfo = window.debugInfo;
            
            return results;
        }''')
        
        print("🔍 ENHANCED CSS & BUTTON ANALYSIS:")
        print("="*60)
        
        for btn_key, analysis in css_analysis.items():
            if btn_key.startswith('button_'):
                print(f"\n📌 {btn_key.upper()}: {analysis['text']}")
                print(f"   Classes: {analysis['classes']}")
                print(f"   Href: {analysis['href']}")
                
                # NEW: Check for HTML attribute constraints
                if analysis['attributes']:
                    suspicious_attrs = {k: v for k, v in analysis['attributes'].items() 
                                      if k in ['size', 'maxlength', 'cols', 'rows']}
                    if suspicious_attrs:
                        print(f"   ⚠️  SUSPICIOUS ATTRIBUTES: {suspicious_attrs}")
                
                # Layout issue detection
                if analysis['layoutIssues']:
                    print(f"   🚨 LAYOUT ISSUES: {', '.join(analysis['layoutIssues'])}")
                
                print(f"   📏 COMPUTED STYLES:")
                print(f"   - Font Family: {analysis['styles']['fontFamily']}")
                print(f"   - Font Weight: {analysis['styles']['fontWeight']}")
                print(f"   - Width: {analysis['styles']['width']} (min: {analysis['styles']['minWidth']}, max: {analysis['styles']['maxWidth']})")
                print(f"   - Text Transform: {analysis['styles']['textTransform']}")
                print(f"   - Overflow: {analysis['styles']['overflow']}")
                
                if analysis['appliedRules']:
                    print(f"   📋 APPLIED CSS RULES:")
                    for rule in analysis['appliedRules'][:3]:  # Show top 3 rules
                        if 'error' not in rule:
                            print(f"      - {rule['selector']}")
                            if rule['fontFamily'] != 'not-set':
                                print(f"        Font: {rule['fontFamily']}")
                            if rule['width'] != 'not-set':
                                print(f"        Width: {rule['width']}")
        
        print(f"\n📄 CSS FILES LOADED:")
        for css_file in css_analysis.get('cssFiles', []):
            status = "❌ DISABLED" if css_file.get('disabled', False) else "✅ ACTIVE"
            print(f"   {status} {css_file['href']}")
        
        # NEW: Report on dynamic changes detected
        debug_info = css_analysis.get('debugInfo', {})
        if debug_info.get('classAdditions'):
            print(f"\n🏷️  DYNAMIC CLASS ADDITIONS DETECTED:")
            for addition in debug_info['classAdditions'][-5:]:  # Show last 5
                print(f"   - {addition['classes']} → {addition['element']}")
        
        if debug_info.get('styleChanges'):
            print(f"\n🎨 DYNAMIC STYLE CHANGES DETECTED:")
            for change in debug_info['styleChanges'][-3:]:  # Show last 3
                print(f"   - {change['element']}: {change['value'][:50]}...")
        
        if debug_info.get('mutations'):
            print(f"\n🔄 DOM MUTATIONS DETECTED: {len(debug_info['mutations'])} changes")
        
        print(f"\n💡 QUICK FIX SUGGESTIONS:")
        print(f"   1. Check DevTools Elements tab for computed styles")
        print(f"   2. Look for size='4' attributes causing width constraints")
        print(f"   3. Monitor Console for class additions causing misalignment")
        print(f"   4. Check if modern CSS files are properly loaded")
        
        print("\n🔧 DEVTOOLS DEBUGGING GUIDE:")
        print("="*60)
        print("📋 Available DevTools panels:")
        print("  - Elements: Inspect HTML/CSS, check computed styles")
        print("  - Console: JavaScript errors/logs, class additions logged")
        print("  - Network: Request monitoring, CSS file loading")
        print("  - Sources: JavaScript debugging, breakpoints")
        print("\n🎯 DEBUGGING CHECKLIST:")
        print("  1. Elements tab → Select button → Computed styles")
        print("  2. Look for HTML attributes (size, maxlength) in Elements")
        print("  3. Console shows class additions and style changes")
        print("  4. Network tab shows if CSS files loaded properly")
        print("  5. Watch for 'flash and misalign' behavior on page refresh")
        print("\n⏰ Browser staying open for 45 seconds for inspection...")
        print("   (Extended time for comprehensive debugging)")
        await page.wait_for_timeout(45000)
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(test_cart_after_add())
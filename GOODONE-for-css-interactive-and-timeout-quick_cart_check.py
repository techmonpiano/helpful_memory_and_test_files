#!/usr/bin/env python3
"""
Quick cart styling check - 20 second timeout
"""

import asyncio
from playwright.async_api import async_playwright

async def quick_cart_check():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,
            devtools=True,
            slow_mo=500
        )
        
        page = await browser.new_page()
        await page.set_viewport_size({'width': 1920, 'height': 1080})
        
        print("🛒 Loading shopping cart page...")
        await page.goto("http://localhost:8000/index.php?main_page=shopping_cart")
        await page.wait_for_load_state('networkidle')
        
        # Take immediate screenshot
        timestamp = await page.evaluate('Date.now()')
        await page.screenshot(path=f"cart_current_state_{timestamp}.jpg", type='jpeg', quality=80)
        print(f"📸 Current cart screenshot: cart_current_state_{timestamp}.jpg")
        
        # Check if cart has items
        cart_status = await page.evaluate('''
            () => {
                const emptyMsg = document.querySelector('.empty_cart');
                const cartRows = document.querySelectorAll('#cartContentsDisplay tr.cartItem, .cart-table tr');
                const cartTable = document.querySelector('#cartContentsDisplay, table.cart-table');
                
                return {
                    isEmpty: emptyMsg !== null,
                    itemCount: cartRows.length,
                    hasTable: cartTable !== null,
                    cartTableId: cartTable ? cartTable.id : null,
                    cartTableClass: cartTable ? cartTable.className : null
                };
            }
        ''')
        
        print(f"🎯 Cart status: {cart_status}")
        
        if cart_status['itemCount'] > 0 or not cart_status['isEmpty']:
            print("✅ Cart has items! Checking styling...")
            
            # Check cart-pg styling application
            styling_check = await page.evaluate('''
                () => {
                    const cartPg = document.querySelector('.cart-pg');
                    const results = { cartPgFound: cartPg !== null };
                    
                    if (cartPg) {
                        // Check if cart-pg specific CSS rules are applied
                        const productCells = cartPg.querySelectorAll('.cartProductDisplay');
                        const removeCells = cartPg.querySelectorAll('.cartRemoveItemDisplay');
                        
                        results.productCells = productCells.length;
                        results.removeCells = removeCells.length;
                        
                        if (productCells.length > 0) {
                            const cell = productCells[0];
                            const styles = getComputedStyle(cell);
                            results.productCellStyles = {
                                display: styles.display,
                                width: styles.width,
                                position: styles.position
                            };
                        }
                        
                        if (removeCells.length > 0) {
                            const cell = removeCells[0];
                            const styles = getComputedStyle(cell);
                            results.removeCellStyles = {
                                position: styles.position,
                                right: styles.right,
                                top: styles.top
                            };
                        }
                    }
                    
                    return results;
                }
            ''')
            
            print(f"🎨 Styling check: {styling_check}")
        else:
            print("❌ Cart is still empty")
        
        # Check CSS loading
        css_check = await page.evaluate('''
            () => {
                const links = Array.from(document.querySelectorAll('link[rel="stylesheet"]'));
                return {
                    asapModern: links.some(l => l.href.includes('asap-modern.css')),
                    componentsModern: links.some(l => l.href.includes('components-modern.css')),
                    templateApp: links.some(l => l.href.includes('template-app.css')),
                    totalCssFiles: links.length
                };
            }
        ''')
        
        print(f"📄 CSS loading: {css_check}")
        
        print("⏰ Keeping browser open for 20 seconds for inspection...")
        await page.wait_for_timeout(20000)
        
        await browser.close()
        print("✅ Browser closed")

if __name__ == "__main__":
    asyncio.run(quick_cart_check())
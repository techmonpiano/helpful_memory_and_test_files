#!/usr/bin/env python3
"""
Test cart button styling by injecting buttons directly
"""

import asyncio
from playwright.async_api import async_playwright

async def test_button_styling():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=500)
        page = await browser.new_page()
        await page.set_viewport_size({'width': 1920, 'height': 1080})
        
        print("🛒 Loading shopping cart page...")
        await page.goto("http://localhost:8000/index.php?main_page=shopping_cart")
        await page.wait_for_load_state('networkidle')
        
        # Inject the three cart buttons to test styling
        button_html = '''
        <div class="row shopping-cart-btns" style="margin-top: 40px; padding: 20px; border: 2px solid #ddd;">
            <h3>Testing Button Styling:</h3>
            
            <div class="btn-checkout d-none d-sm-block col-sm mb-3">
                <a href="#" class="checkout-btn-modern" 
                   style="--btn-primary-bg: #dc3545; --btn-hover-bg: #c82333;">
                    EMPTY CART
                </a>
            </div>

            <div class="buttonRow btn-continue-checkout back col-auto mb-3 mr-2">
                <a href="#" class="checkout-btn-modern" 
                   style="--btn-primary-bg: #6c757d; --btn-hover-bg: #5a6268;">
                    CONTINUE SHOPPING
                </a>
            </div>

            <div class="col-auto mb-3">
                <div class="btn-checkout forward">
                    <a href="#" id="checkoutButton" class="checkout-btn-modern">
                        PROCEED TO CHECKOUT <span class="icon icon-angle-right"></span>
                    </a>
                </div>
            </div>
        </div>
        '''
        
        print("💉 Injecting cart buttons...")
        await page.evaluate(f'''
            const cartPg = document.querySelector('.cart-pg');
            if (cartPg) {{
                const tempDiv = document.createElement('div');
                tempDiv.innerHTML = `{button_html}`;
                cartPg.appendChild(tempDiv.firstElementChild);
            }}
        ''')
        
        # Take screenshot with buttons
        await page.screenshot(path='cart_buttons_test.png', full_page=True)
        print("📸 Screenshot saved as: cart_buttons_test.png")
        
        # Check computed styles for buttons
        button_styles = await page.evaluate('''
            const results = {};
            
            // Check all three buttons
            const buttons = document.querySelectorAll('.checkout-btn-modern');
            buttons.forEach((btn, index) => {
                const computed = window.getComputedStyle(btn);
                results[`button_${index}`] = {
                    backgroundColor: computed.backgroundColor,
                    color: computed.color,
                    padding: computed.padding,
                    fontSize: computed.fontSize,
                    display: computed.display,
                    text: btn.textContent.trim()
                };
            });
            
            return results;
        ''')
        
        print("🎨 Button styles:")
        for btn_key, styles in button_styles.items():
            print(f"  {btn_key} ({styles['text']}): bg={styles['backgroundColor']}, color={styles['color']}")
        
        print("⏰ Browser staying open for 15 seconds for inspection...")
        await page.wait_for_timeout(15000)
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(test_button_styling())
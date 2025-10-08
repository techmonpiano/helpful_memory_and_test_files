#!/usr/bin/env python3
"""
Test cart buttons after successfully adding item via add-to-cart modal
"""

import asyncio
from playwright.async_api import async_playwright

async def test_cart_after_add():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=500)
        page = await browser.new_page()
        await page.set_viewport_size({'width': 1920, 'height': 1080})
        
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
        await page.screenshot(path='cart_with_items_open_sans_test.png', full_page=True)
        print("📸 Screenshot saved: cart_with_items_open_sans_test.png")
        
        # Check button fonts
        button_fonts = await page.evaluate('''() => {
            const buttons = document.querySelectorAll('.cart-pg .checkout-btn-modern, .shopping-cart-page .checkout-btn-modern');
            const results = [];
            
            buttons.forEach((btn, index) => {
                const computed = window.getComputedStyle(btn);
                results.push({
                    index: index,
                    text: btn.textContent.trim(),
                    fontFamily: computed.fontFamily,
                    fontWeight: computed.fontWeight,
                    color: computed.color,
                    backgroundColor: computed.backgroundColor
                });
            });
            
            return results;
        }''')
        
        print("🎨 Button font analysis:")
        for btn in button_fonts:
            print(f"  Button {btn['index']} ({btn['text'][:20]}...): {btn['fontFamily'][:50]}...")
            print(f"    Weight: {btn['fontWeight']}, Color: {btn['color']}")
        
        print("⏰ Browser staying open for 15 seconds for inspection...")
        await page.wait_for_timeout(15000)
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(test_cart_after_add())
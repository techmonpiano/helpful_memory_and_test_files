#!/usr/bin/env python3

import asyncio
from playwright.async_api import async_playwright

async def test_payment_fix():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        
        try:
            print("🛒 Step 1: Adding product to cart...")
            await page.goto('http://localhost:8000/index.php?main_page=product_info&cPath=1&products_id=1')
            await page.wait_for_load_state('networkidle')
            
            # Add to cart
            add_btn = await page.query_selector('#cart_quantity_submit')
            if add_btn:
                await add_btn.click()
                await page.wait_for_timeout(2000)
                print("✅ Product added")
            
            print("🛒 Step 2: Going to checkout...")
            await page.goto('http://localhost:8000/index.php?main_page=one_page_checkout')
            await page.wait_for_load_state('networkidle')
            await page.wait_for_timeout(3000)
            
            # Check if we can find Step 2 (shipping)
            step2 = await page.query_selector('#checkout-step-shipping')
            if step2:
                is_visible = await step2.is_visible()
                print(f"📍 Step 2 visible: {is_visible}")
                
                if is_visible:
                    print("🚚 At Step 2, looking for Continue button...")
                    await page.wait_for_timeout(3000)  # Wait for shipping to load
                    
                    continue_btn = await page.query_selector('#shipping-methods-content-container .btn[type="submit"]')
                    if continue_btn:
                        print("🔘 Found Continue button, testing click...")
                        
                        # Click and monitor for success
                        await continue_btn.click()
                        await page.wait_for_timeout(3000)
                        
                        # Check if Step 3 is now visible
                        step3 = await page.query_selector('#checkout-step-billing:not(.d-none)')
                        if step3 and await step3.is_visible():
                            print("✅ SUCCESS: Advanced to Step 3!")
                        else:
                            print("❌ Continue button didn't advance to Step 3")
                    else:
                        print("❌ Continue button not found")
            
            # Quick check of console for errors
            await page.wait_for_timeout(1000)
            
        except Exception as e:
            print(f"❌ Error: {e}")
        finally:
            await browser.close()
            print("✅ Test completed")

if __name__ == "__main__":
    asyncio.run(test_payment_fix())
#!/usr/bin/env python3

import asyncio
from playwright.async_api import async_playwright

async def test_continue_with_cart():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        
        try:
            print("🛒 Step 1: Adding product to cart...")
            await page.goto('http://localhost:8000/index.php?main_page=product_info&cPath=1&products_id=1')
            await page.wait_for_load_state('networkidle')
            await page.wait_for_timeout(2000)
            
            # Add to cart
            add_to_cart_btn = await page.query_selector('#cart_quantity_submit')
            if add_to_cart_btn:
                await add_to_cart_btn.click()
                await page.wait_for_timeout(2000)
                print("✅ Product added to cart")
            
            print("🛒 Step 2: Going to one page checkout...")
            await page.goto('http://localhost:8000/index.php?main_page=one_page_checkout')
            await page.wait_for_load_state('networkidle')
            await page.wait_for_timeout(3000)
            
            # Check what step we're at
            step1_visible = await page.is_visible('#checkout-step-login:not(.d-none)')
            step2_visible = await page.is_visible('#checkout-step-shipping:not(.d-none)')
            step3_visible = await page.is_visible('#checkout-step-billing:not(.d-none)')
            
            print(f"📍 Current steps - Login: {step1_visible}, Shipping: {step2_visible}, Billing: {step3_visible}")
            
            if step2_visible:
                print("🚚 At Step 2 - Testing Continue button...")
                
                # Wait for shipping methods to load
                await page.wait_for_selector('#shipping-methods-content-container', timeout=10000)
                await page.wait_for_timeout(2000)
                
                # Find Continue button
                continue_btn = await page.query_selector('#shipping-methods-content-container .btn[type="submit"]')
                if continue_btn:
                    print("🔘 Found Continue button, clicking...")
                    
                    # Click and wait for response
                    await continue_btn.click()
                    await page.wait_for_timeout(3000)
                    
                    # Check if we advanced to Step 3
                    step3_after = await page.is_visible('#checkout-step-billing:not(.d-none)')
                    if step3_after:
                        print("✅ SUCCESS: Advanced to Step 3 (Billing)!")
                    else:
                        print("❌ FAILED: Still at Step 2")
                        
                        # Check for any error messages or modals
                        error_modal = await page.is_visible('.modal.show')
                        if error_modal:
                            error_text = await page.inner_text('.modal.show')
                            print(f"📝 Error modal visible: {error_text[:200]}...")
                    
                else:
                    print("❌ Continue button not found")
            else:
                print("⚠️ Not at Step 2 - cannot test Continue button")
            
        except Exception as e:
            print(f"❌ Error: {e}")
        finally:
            await browser.close()
            print("✅ Test completed")

if __name__ == "__main__":
    asyncio.run(test_continue_with_cart())
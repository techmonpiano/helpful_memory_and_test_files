#!/usr/bin/env python3

import asyncio
from playwright.async_api import async_playwright
import time

async def test_continue_proper():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        
        try:
            print("🛒 Step 1: Adding product to cart...")
            
            # Go to a specific product page
            await page.goto('http://localhost:8000/index.php?main_page=product_info&products_id=1')
            await page.wait_for_load_state('networkidle')
            await page.wait_for_timeout(2000)
            
            # Look for add to cart button
            add_to_cart_selectors = [
                '#cart_quantity_submit',
                'input[type="submit"][value*="Add"]',
                'button[type="submit"]',
                '.btn-cart'
            ]
            
            cart_added = False
            for selector in add_to_cart_selectors:
                btn = await page.query_selector(selector)
                if btn:
                    btn_text = await btn.get_attribute('value') or await btn.inner_text()
                    print(f"📦 Found button: {selector} - '{btn_text}'")
                    
                    await btn.click()
                    await page.wait_for_timeout(3000)
                    cart_added = True
                    print("✅ Clicked add to cart button")
                    break
            
            if not cart_added:
                print("❌ Could not find add to cart button")
                return
            
            print("\n🛒 Step 2: Going to One Page Checkout...")
            await page.goto('http://localhost:8000/index.php?main_page=one_page_checkout')
            await page.wait_for_load_state('networkidle')
            await page.wait_for_timeout(4000)
            
            # Check what steps are visible now
            step1 = await page.query_selector('#checkout-step-login')
            step2 = await page.query_selector('#checkout-step-shipping')  
            step3 = await page.query_selector('#checkout-step-billing')
            
            step1_visible = step1 and await step1.is_visible() if step1 else False
            step2_visible = step2 and await step2.is_visible() if step2 else False
            step3_visible = step3 and await step3.is_visible() if step3 else False
            
            print(f"📍 Current checkout steps:")
            print(f"   Login (Step 1): {step1_visible}")
            print(f"   Shipping (Step 2): {step2_visible}")
            print(f"   Billing (Step 3): {step3_visible}")
            
            if step2_visible:
                print("\n🚚 At Step 2 - Testing Continue Button...")
                
                # Wait for shipping methods to fully load
                print("⏳ Waiting for shipping methods...")
                await page.wait_for_timeout(5000)
                
                # Look for Continue button in shipping section
                continue_selectors = [
                    '#shipping-methods-content-container .btn[type="submit"]',
                    '#shipping-methods-content-container button[type="submit"]',
                    'input[type="submit"][value*="Continue"]',
                    '.btn-continue'
                ]
                
                continue_btn = None
                for selector in continue_selectors:
                    btn = await page.query_selector(selector)
                    if btn and await btn.is_visible():
                        continue_btn = btn
                        print(f"🔘 Found Continue button: {selector}")
                        break
                
                if continue_btn:
                    print("🔄 Clicking Continue button...")
                    
                    # Click and monitor response
                    await continue_btn.click()
                    await page.wait_for_timeout(4000)
                    
                    # Check if we advanced to Step 3
                    step3_after = step3 and await step3.is_visible() if step3 else False
                    step2_after = step2 and await step2.is_visible() if step2 else False
                    
                    print(f"📍 After Continue click:")
                    print(f"   Shipping (Step 2): {step2_after}")  
                    print(f"   Billing (Step 3): {step3_after}")
                    
                    if step3_after and not step2_after:
                        print("\n🎉 SUCCESS! Continue button worked - Advanced to Step 3!")
                    elif step2_after and not step3_after:
                        print("\n❌ Still at Step 2 - Continue button failed")
                    else:
                        print(f"\n⚠️  Unclear state after Continue click")
                        
                    # Check for any error messages
                    error_modal = await page.is_visible('.modal.show')
                    if error_modal:
                        error_text = await page.inner_text('.modal.show')
                        print(f"⚠️  Error modal: {error_text[:150]}...")
                        
                else:
                    print("❌ Continue button not found")
                    
            elif step1_visible:
                print("⚠️  At login step - need to log in first")
            else:
                print("⚠️  Unknown checkout state")
                
        except Exception as e:
            print(f"❌ Error during test: {e}")
            
        finally:
            await browser.close()
            print("\n✅ Test completed")

if __name__ == "__main__":
    asyncio.run(test_continue_proper())
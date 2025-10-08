#!/usr/bin/env python3

import asyncio
from playwright.async_api import async_playwright
import time

async def test_step3_content():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        
        try:
            print("🔧 TESTING: Step 3 Content Loading Fix")
            print("=" * 50)
            
            print("Step 1: Adding product to cart...")
            await page.goto('http://localhost:8000/index.php?main_page=product_info&products_id=1')
            await page.wait_for_load_state('networkidle')
            
            # Add to cart
            add_btn = await page.query_selector('.btn--add-to-cart, input[type="submit"][value*="Add"]')
            if add_btn:
                await add_btn.click()
                await page.wait_for_timeout(3000)
                print("✅ Product added to cart")
            
            print("\nStep 2: Going to One Page Checkout...")
            await page.goto('http://localhost:8000/index.php?main_page=one_page_checkout')
            await page.wait_for_load_state('networkidle')
            await page.wait_for_timeout(4000)
            
            # Look for checkout steps container
            checkout_steps = await page.query_selector('#opc-checkout-steps')
            if checkout_steps:
                print("✅ Found checkout steps container")
                
                # Check for Step 2 (shipping) elements
                step2_elements = await page.query_selector_all('#checkout-step-shipping, [data-step="2"], .step-shipping')
                if step2_elements:
                    print(f"📍 Found {len(step2_elements)} Step 2 elements")
                    
                    # Wait for shipping methods and look for Continue button
                    await page.wait_for_timeout(4000)
                    
                    continue_btn = await page.query_selector('.btn[type="submit"], input[type="submit"][value*="Continue"]')
                    if continue_btn:
                        btn_text = await continue_btn.inner_text() or await continue_btn.get_attribute('value')
                        print(f"🔘 Found Continue button: '{btn_text}'")
                        
                        print("\nStep 3: Clicking Continue to advance to Step 3...")
                        await continue_btn.click()
                        await page.wait_for_timeout(4000)
                        
                        # Check for Step 3 content
                        step3_elements = await page.query_selector_all('#checkout-step-billing, [data-step="3"], .step-billing')
                        print(f"📍 Found {len(step3_elements)} Step 3 elements")
                        
                        # Look for billing form elements that should be present
                        billing_forms = await page.query_selector_all('form, .billing-form, .payment-form')
                        billing_inputs = await page.query_selector_all('input[name*="billing"], input[name*="payment"]')
                        payment_options = await page.query_selector_all('input[type="radio"][name*="payment"]')
                        
                        print(f"\n📋 Step 3 Content Analysis:")
                        print(f"   Forms found: {len(billing_forms)}")
                        print(f"   Billing inputs: {len(billing_inputs)}")  
                        print(f"   Payment options: {len(payment_options)}")
                        
                        # Check for specific billing elements
                        billing_checkbox = await page.query_selector('input[name="shipping_is_billing"]')
                        if billing_checkbox:
                            print("✅ Found 'Billing same as shipping' checkbox")
                        
                        # Look for any error messages
                        error_messages = await page.query_selector_all('.error, .alert-danger, .messageStackError')
                        if error_messages:
                            print(f"⚠️  Found {len(error_messages)} error messages")
                            for i, msg in enumerate(error_messages[:3]):
                                text = await msg.inner_text()
                                print(f"   Error {i+1}: {text[:100]}...")
                        
                        # Check page title to see if we're on billing step
                        title = await page.title()
                        if "billing" in title.lower() or "payment" in title.lower():
                            print("✅ Page title suggests we're at billing step")
                        
                        # Final assessment
                        if billing_forms and (billing_inputs or payment_options):
                            print("\n🎉 SUCCESS: Step 3 content appears to be loading properly!")
                        elif step3_elements:
                            print("\n⚠️  PARTIAL: Step 3 header present but content may be missing")
                        else:
                            print("\n❌ FAILED: No Step 3 content detected")
                            
                    else:
                        print("❌ Continue button not found")
                else:
                    print("⚠️  Step 2 elements not found")
            else:
                print("❌ Checkout steps container not found")
            
            # Keep browser open for inspection
            print("\n⏳ Keeping browser open for 20 seconds for inspection...")
            await page.wait_for_timeout(20000)
            
        except Exception as e:
            print(f"❌ Test error: {e}")
            
        finally:
            await browser.close()
            print("\n✅ Test completed")

if __name__ == "__main__":
    asyncio.run(test_step3_content())
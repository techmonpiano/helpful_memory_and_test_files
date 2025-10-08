#!/usr/bin/env python3

import asyncio
from playwright.async_api import async_playwright
import time

async def final_continue_test():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        
        # Track network responses for AJAX monitoring
        responses = []
        
        async def handle_response(response):
            if 'controller' in response.url and 'checkout_shipping' in response.url:
                try:
                    text = await response.text()
                    responses.append({
                        'url': response.url,
                        'status': response.status,
                        'text': text[:300] + '...' if len(text) > 300 else text
                    })
                    print(f"📡 AJAX Response: {response.status}")
                except:
                    pass
        
        page.on('response', handle_response)
        
        try:
            print("🛒 FINAL TEST: Continue Button Functionality")
            print("=" * 50)
            
            print("Step 1: Adding product to cart...")
            await page.goto('http://localhost:8000/index.php?main_page=product_info&cPath=1&products_id=1')
            await page.wait_for_load_state('networkidle')
            
            add_btn = await page.query_selector('#cart_quantity_submit')
            if add_btn:
                await add_btn.click()
                await page.wait_for_timeout(2000)
                print("✅ Product added to cart")
            
            print("\nStep 2: Navigating to One Page Checkout...")
            await page.goto('http://localhost:8000/index.php?main_page=one_page_checkout')
            await page.wait_for_load_state('networkidle')
            await page.wait_for_timeout(3000)
            
            # Check current step
            step2_visible = await page.is_visible('#checkout-step-shipping:not(.d-none)')
            step3_visible = await page.is_visible('#checkout-step-billing:not(.d-none)')
            
            print(f"📍 Current state - Step 2: {step2_visible}, Step 3: {step3_visible}")
            
            if step2_visible:
                print("\nStep 3: Testing Continue Button from Step 2 to Step 3...")
                
                # Wait for shipping methods to load completely
                print("⏳ Waiting for shipping methods to load...")
                await page.wait_for_timeout(4000)
                
                # Find and test Continue button
                continue_btn = await page.query_selector('#shipping-methods-content-container .btn[type="submit"]')
                
                if continue_btn:
                    is_visible = await continue_btn.is_visible()
                    print(f"🔘 Continue button found and visible: {is_visible}")
                    
                    if is_visible:
                        print("🔄 Clicking Continue button...")
                        start_time = time.time()
                        
                        # Click button
                        await continue_btn.click()
                        
                        # Wait for AJAX response and page update
                        await page.wait_for_timeout(3000)
                        
                        # Check if we successfully advanced to Step 3
                        step3_after = await page.is_visible('#checkout-step-billing:not(.d-none)')
                        step2_after = await page.is_visible('#checkout-step-shipping:not(.d-none)')
                        
                        elapsed = time.time() - start_time
                        
                        print(f"⏱️  Response time: {elapsed:.1f}s")
                        print(f"📍 After click - Step 2: {step2_after}, Step 3: {step3_after}")
                        
                        if step3_after and not step2_after:
                            print("\n🎉 SUCCESS! Continue button successfully advanced from Step 2 to Step 3!")
                            print("✅ The Continue button issue has been RESOLVED!")
                        elif step2_after and not step3_after:
                            print("\n❌ FAILED: Still at Step 2, did not advance to Step 3")
                        else:
                            print(f"\n⚠️  Unclear state: Step 2={step2_after}, Step 3={step3_after}")
                        
                        # Check for error modals
                        error_modal = await page.is_visible('.modal.show')
                        if error_modal:
                            error_text = await page.inner_text('.modal.show')
                            print(f"⚠️  Error modal detected: {error_text[:100]}...")
                    
                else:
                    print("❌ Continue button not found")
                    
            else:
                print("⚠️  Not currently at Step 2")
            
            # Show AJAX responses
            if responses:
                print(f"\n📊 AJAX Responses ({len(responses)}):")
                for resp in responses[-2:]:  # Last 2
                    print(f"   Status: {resp['status']}")
                    print(f"   Content: {resp['text'][:150]}...")
            
        except Exception as e:
            print(f"❌ Test error: {e}")
            
        finally:
            print("\n" + "=" * 50)
            await browser.close()
            print("✅ Final test completed")

if __name__ == "__main__":
    asyncio.run(final_continue_test())
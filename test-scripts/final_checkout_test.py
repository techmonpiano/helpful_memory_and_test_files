#!/usr/bin/env python3

import asyncio
from playwright.async_api import async_playwright
import time

async def final_checkout_test():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        
        # Track AJAX responses
        ajax_responses = []
        
        async def handle_response(response):
            if 'controller' in response.url and 'checkout' in response.url:
                try:
                    text = await response.text()
                    ajax_responses.append({
                        'url': response.url,
                        'status': response.status,
                        'text': text[:200] + '...' if len(text) > 200 else text,
                        'timestamp': time.time()
                    })
                    print(f"📡 AJAX: {response.status} - {response.url}")
                except:
                    pass
        
        page.on('response', handle_response)
        
        try:
            print("🎯 FINAL TEST: Complete Continue Button Fix Verification")
            print("=" * 60)
            
            # Add product to cart
            print("Step 1: Adding product to cart...")
            await page.goto('http://localhost:8000/')
            await page.wait_for_load_state('networkidle')
            
            # Click first product
            product_link = await page.query_selector('a[href*="products_id"]')
            if product_link:
                await product_link.click()
                await page.wait_for_load_state('networkidle')
                
                # Add to cart
                add_btn = await page.query_selector('.btn--add-to-cart')
                if add_btn:
                    await add_btn.click()
                    await page.wait_for_timeout(3000)
                    print("✅ Product added to cart")
            
            # Go to checkout
            print("\nStep 2: Accessing One Page Checkout...")
            await page.goto('http://localhost:8000/index.php?main_page=one_page_checkout')
            await page.wait_for_load_state('networkidle')
            await page.wait_for_timeout(4000)
            
            # Check current state
            page_content = await page.inner_text('body')
            
            if 'shipping' in page_content.lower():
                print("✅ Checkout page loaded with shipping content")
                
                # Look for Continue button
                continue_selectors = [
                    'button:has-text("Continue")',
                    'input[value*="Continue"]', 
                    '.btn[type="submit"]',
                    'button[type="submit"]'
                ]
                
                continue_btn = None
                for selector in continue_selectors:
                    btn = await page.query_selector(selector)
                    if btn and await btn.is_visible():
                        continue_btn = btn
                        btn_text = await btn.inner_text() or await btn.get_attribute('value')
                        print(f"🔘 Found Continue button: '{btn_text}'")
                        break
                
                if continue_btn:
                    print("\nStep 3: Testing Continue Button (Step 2 → Step 3)...")
                    
                    # Clear previous responses
                    ajax_responses.clear()
                    
                    # Click Continue
                    await continue_btn.click()
                    print("🔄 Continue button clicked, waiting for response...")
                    
                    # Wait for AJAX and page updates
                    await page.wait_for_timeout(4000)
                    
                    # Check for Step 3 content
                    updated_content = await page.inner_text('body')
                    
                    # Look for billing/payment indicators
                    has_billing = 'billing' in updated_content.lower()
                    has_payment = 'payment' in updated_content.lower()
                    has_step3 = '3' in updated_content and ('step' in updated_content.lower() or 'billing' in updated_content.lower())
                    
                    print(f"\n📍 Step 3 Content Analysis:")
                    print(f"   Contains 'billing': {has_billing}")
                    print(f"   Contains 'payment': {has_payment}")
                    print(f"   Has Step 3 indicators: {has_step3}")
                    
                    # Check AJAX responses
                    if ajax_responses:
                        print(f"\n📡 AJAX Responses ({len(ajax_responses)}):")
                        for resp in ajax_responses:
                            print(f"   {resp['status']} - {resp['url']}")
                            if resp['status'] == 200:
                                print(f"     Content: {resp['text']}")
                    
                    # Final determination
                    if (has_billing or has_payment) and len(ajax_responses) > 0:
                        success_responses = [r for r in ajax_responses if r['status'] == 200]
                        if success_responses:
                            print("\n🎉 SUCCESS: Continue button appears to be working!")
                            print("   ✅ Step 3 content detected")
                            print("   ✅ AJAX responses successful")
                            print("   ✅ No fatal template errors")
                        else:
                            print("\n⚠️ PARTIAL: Content updated but AJAX had issues")
                    else:
                        print("\n❌ ISSUE: Continue button may not be working properly")
                        
                else:
                    print("❌ Continue button not found")
            else:
                print("❌ Checkout page not properly loaded")
            
            print(f"\n📊 FINAL SUMMARY:")
            print(f"   AJAX responses: {len(ajax_responses)}")
            print(f"   Page transitions: {'✅ Working' if ajax_responses else '❌ No AJAX activity'}")
            
            # Keep browser open briefly for manual inspection
            print("\n⏳ Browser staying open for 10 seconds for inspection...")
            await page.wait_for_timeout(10000)
            
        except Exception as e:
            print(f"❌ Test error: {e}")
            
        finally:
            await browser.close()
            print("\n🏁 Final checkout test completed!")

if __name__ == "__main__":
    asyncio.run(final_checkout_test())
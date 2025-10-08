#!/usr/bin/env python3

import asyncio
from playwright.async_api import async_playwright

async def verify_step3_fix():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        
        # Monitor console errors
        console_errors = []
        
        def handle_console(msg):
            if msg.type == 'error':
                console_errors.append(msg.text)
                print(f"🔥 Console Error: {msg.text}")
        
        page.on('console', handle_console)
        
        try:
            print("🧪 VERIFICATION: Step 3 Content Fix")
            print("=" * 40)
            
            # Go directly to checkout to see what we get
            print("Step 1: Direct checkout access...")
            await page.goto('http://localhost:8000/index.php?main_page=one_page_checkout')
            await page.wait_for_load_state('networkidle')
            await page.wait_for_timeout(2000)
            
            # Check if we can see the page at all
            title = await page.title()
            print(f"📄 Page title: {title}")
            
            # Look for any content indicators
            body_content = await page.inner_text('body')
            if 'checkout' in body_content.lower():
                print("✅ Checkout page loaded")
            elif 'login' in body_content.lower() or 'sign in' in body_content.lower():
                print("⚠️  Redirected to login - need to add product first")
            else:
                print("❓ Unknown page state")
            
            # Try adding a product first
            print("\nStep 2: Adding product to enable checkout...")
            await page.goto('http://localhost:8000/')
            await page.wait_for_load_state('networkidle')
            
            # Look for any product link
            product_links = await page.query_selector_all('a[href*="products_id"]')
            if product_links:
                print(f"📦 Found {len(product_links)} product links")
                await product_links[0].click()
                await page.wait_for_load_state('networkidle')
                
                # Add to cart
                add_btn = await page.query_selector('.btn--add-to-cart, input[value*="Add"], button:has-text("Add")')
                if add_btn:
                    await add_btn.click()
                    await page.wait_for_timeout(2000)
                    print("✅ Added product to cart")
                    
                    # Now try checkout again
                    print("\nStep 3: Accessing checkout with product in cart...")
                    await page.goto('http://localhost:8000/index.php?main_page=one_page_checkout')
                    await page.wait_for_load_state('networkidle')
                    await page.wait_for_timeout(3000)
                    
                    # Look for actual checkout content
                    checkout_content = await page.inner_text('body')
                    
                    if 'shipping' in checkout_content.lower() and 'billing' in checkout_content.lower():
                        print("✅ Checkout page with shipping/billing content loaded")
                        
                        # Look for continue buttons or step indicators
                        continue_btns = await page.query_selector_all('button:has-text("Continue"), input[value*="Continue"]')
                        print(f"🔘 Found {len(continue_btns)} Continue buttons")
                        
                        # Test if we can see step content without errors
                        if not console_errors:
                            print("✅ No JavaScript console errors detected")
                        else:
                            print(f"⚠️  Found {len(console_errors)} console errors")
                    
                    elif 'error' in checkout_content.lower():
                        print("❌ Checkout shows error messages")
                        error_content = checkout_content[:500] + "..." if len(checkout_content) > 500 else checkout_content
                        print(f"Error preview: {error_content}")
                    else:
                        print("❓ Checkout content unclear")
            
            # Check for any AJAX activity by monitoring network
            print("\nStep 4: Testing AJAX responses...")
            responses_captured = []
            
            def capture_response(response):
                if 'controller' in response.url and 'opc' in response.url:
                    responses_captured.append({
                        'url': response.url,
                        'status': response.status
                    })
            
            page.on('response', capture_response)
            
            # Try to trigger an AJAX call if possible
            await page.evaluate("""
                if (typeof $ !== 'undefined') {
                    $.get('/index.php?main_page=controller&zpage=opc&step=test')
                     .done(function() { console.log('AJAX test succeeded'); })
                     .fail(function() { console.log('AJAX test failed'); });
                }
            """)
            
            await page.wait_for_timeout(2000)
            
            if responses_captured:
                print(f"📡 Captured {len(responses_captured)} AJAX responses")
                for resp in responses_captured:
                    print(f"   {resp['status']} - {resp['url']}")
            else:
                print("📡 No AJAX responses captured")
            
            # Final assessment
            print(f"\n📊 VERIFICATION RESULTS:")
            print(f"   Console Errors: {len(console_errors)}")
            print(f"   AJAX Responses: {len(responses_captured)}")
            
            if len(console_errors) == 0:
                print("🎉 SUCCESS: No console errors - Step 3 fix appears to be working!")
            else:
                print("⚠️  WARNING: Console errors detected - may need additional fixes")
                
        except Exception as e:
            print(f"❌ Verification error: {e}")
            
        finally:
            await browser.close()
            print("\n✅ Verification completed")

if __name__ == "__main__":
    asyncio.run(verify_step3_fix())
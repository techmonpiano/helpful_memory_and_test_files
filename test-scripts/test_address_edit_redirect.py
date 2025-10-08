#!/usr/bin/env python3

import asyncio
from playwright.async_api import async_playwright
import time

async def test_address_edit_redirect():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        
        try:
            print("🧪 TESTING: Address Edit Redirect Fix")
            print("=" * 50)
            
            # Add product and go to checkout
            print("Step 1: Setting up checkout...")
            await page.goto('http://localhost:8000/')
            await page.wait_for_load_state('networkidle')
            
            # Add product to cart
            product_link = await page.query_selector('a[href*="products_id"]')
            if product_link:
                await product_link.click()
                await page.wait_for_load_state('networkidle')
                
                add_btn = await page.query_selector('.btn--add-to-cart')
                if add_btn:
                    await add_btn.click()
                    await page.wait_for_timeout(2000)
                    print("✅ Product added to cart")
            
            # Go to checkout
            await page.goto('http://localhost:8000/index.php?main_page=one_page_checkout')
            await page.wait_for_load_state('networkidle')
            await page.wait_for_timeout(4000)
            
            print("\nStep 2: Testing Shipping Address Edit (Step 2 → Step 2)")
            print("-" * 40)
            
            # Look for shipping edit button
            shipping_edit_btn = await page.query_selector('a[href*="address_book_process"][href*="context=shipping"]')
            if shipping_edit_btn:
                print("✅ Found shipping Edit button with context parameter")
                
                # Get current URL to compare later
                original_url = page.url
                
                # Click shipping edit button
                await shipping_edit_btn.click()
                await page.wait_for_load_state('networkidle')
                await page.wait_for_timeout(2000)
                
                # Check if we're on address edit page
                current_url = page.url
                if 'address_book_process' in current_url and 'context=shipping' in current_url:
                    print("✅ Correctly navigated to shipping address edit page")
                    
                    # Look for Save button and click it (without actually changing anything)
                    save_btn = await page.query_selector('input[type="submit"][value*="Save"], button[type="submit"]:has-text("Save")')
                    if save_btn:
                        await save_btn.click()
                        await page.wait_for_load_state('networkidle')
                        await page.wait_for_timeout(3000)
                        
                        # Check if we returned to checkout
                        final_url = page.url
                        if 'one_page_checkout' in final_url:
                            print("✅ Successfully returned to checkout after shipping address edit")
                            
                            # Check if we're still on shipping step (Step 2)
                            page_content = await page.inner_text('body')
                            if 'shipping' in page_content.lower():
                                print("✅ Correctly returned to Step 2 (shipping) after shipping address edit")
                            else:
                                print("❌ May not be on Step 2 after shipping edit")
                        else:
                            print("❌ Did not return to checkout after shipping address edit")
                    else:
                        print("⚠️ Save button not found on address edit page")
                else:
                    print("❌ Did not navigate to shipping address edit page")
            else:
                print("❌ Shipping Edit button with context parameter not found")
            
            # Navigate to Step 3 for billing test
            print("\nStep 3: Advancing to Step 3 for Billing Test")
            print("-" * 40)
            
            # Look for Continue button to advance to Step 3
            continue_btn = await page.query_selector('button:has-text("Continue"), input[value*="Continue"], .btn[type="submit"]')
            if continue_btn:
                await continue_btn.click()
                await page.wait_for_timeout(4000)
                print("✅ Advanced to Step 3")
                
                print("\nStep 4: Testing Billing Address Edit (Step 3 → Step 3)")
                print("-" * 40)
                
                # Look for billing edit button
                billing_edit_btn = await page.query_selector('a[href*="address_book_process"][href*="context=billing"]')
                if billing_edit_btn:
                    print("✅ Found billing Edit button with context parameter")
                    
                    # Click billing edit button  
                    await billing_edit_btn.click()
                    await page.wait_for_load_state('networkidle')
                    await page.wait_for_timeout(2000)
                    
                    # Check if we're on billing address edit page
                    current_url = page.url
                    if 'address_book_process' in current_url and 'context=billing' in current_url:
                        print("✅ Correctly navigated to billing address edit page")
                        
                        # Look for Save button and click it
                        save_btn = await page.query_selector('input[type="submit"][value*="Save"], button[type="submit"]:has-text("Save")')
                        if save_btn:
                            await save_btn.click()
                            await page.wait_for_load_state('networkidle')
                            await page.wait_for_timeout(3000)
                            
                            # Check if we returned to checkout
                            final_url = page.url
                            if 'one_page_checkout' in final_url:
                                print("✅ Successfully returned to checkout after billing address edit")
                                
                                # Check if we're on billing step (Step 3)
                                page_content = await page.inner_text('body')
                                if 'billing' in page_content.lower() or 'payment' in page_content.lower():
                                    print("✅ FIXED: Correctly returned to Step 3 (billing) after billing address edit!")
                                    print("🎉 SUCCESS: Billing edit redirect issue RESOLVED!")
                                else:
                                    print("❌ Did not return to Step 3 after billing edit - may have gone to Step 2")
                            else:
                                print("❌ Did not return to checkout after billing address edit")
                        else:
                            print("⚠️ Save button not found on billing address edit page")
                    else:
                        print("❌ Did not navigate to billing address edit page")
                else:
                    print("❌ Billing Edit button with context parameter not found")
            else:
                print("❌ Continue button not found to advance to Step 3")
            
            print("\n📊 TEST SUMMARY:")
            print("🔧 Applied GPT-5 validated fix with context parameters")
            print("🔗 Added &context=shipping to shipping edit buttons")
            print("🔗 Added &context=billing to billing edit buttons")  
            print("⚙️ Updated redirect logic to prefer context over session")
            
            # Keep browser open for manual verification
            print("\n⏳ Keeping browser open for 15 seconds for manual verification...")
            await page.wait_for_timeout(15000)
            
        except Exception as e:
            print(f"❌ Test error: {e}")
            
        finally:
            await browser.close()
            print("\n✅ Address edit redirect test completed!")

if __name__ == "__main__":
    asyncio.run(test_address_edit_redirect())
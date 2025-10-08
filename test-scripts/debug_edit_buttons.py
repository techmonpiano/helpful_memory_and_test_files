#!/usr/bin/env python3

import asyncio
from playwright.async_api import async_playwright

async def debug_edit_buttons():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        
        try:
            print("🔍 DEBUG: Finding Edit Buttons")
            print("=" * 40)
            
            # Setup checkout
            await page.goto('http://localhost:8000/')
            await page.wait_for_load_state('networkidle')
            
            # Add product
            product_link = await page.query_selector('a[href*="products_id"]')
            if product_link:
                await product_link.click()
                await page.wait_for_load_state('networkidle')
                add_btn = await page.query_selector('.btn--add-to-cart')
                if add_btn:
                    await add_btn.click()
                    await page.wait_for_timeout(2000)
            
            # Go to checkout
            await page.goto('http://localhost:8000/index.php?main_page=one_page_checkout')
            await page.wait_for_load_state('networkidle')
            await page.wait_for_timeout(4000)
            
            print("Step 1: Looking for Edit buttons on Step 2 (shipping)")
            
            # Find ALL edit buttons
            all_edit_buttons = await page.query_selector_all('a:has-text("Edit"), button:has-text("Edit"), input[value*="Edit"]')
            print(f"📝 Found {len(all_edit_buttons)} total Edit buttons/links")
            
            for i, btn in enumerate(all_edit_buttons):
                href = await btn.get_attribute('href')
                text = await btn.inner_text()
                print(f"   {i+1}. Text: '{text}' | href: {href}")
            
            # Look specifically for address_book_process links
            address_edit_links = await page.query_selector_all('a[href*="address_book_process"]')
            print(f"\n🏠 Found {len(address_edit_links)} address_book_process links")
            
            for i, link in enumerate(address_edit_links):
                href = await link.get_attribute('href')
                text = await link.inner_text()
                print(f"   {i+1}. Text: '{text}' | href: {href}")
            
            # Advance to Step 3
            print("\nAdvancing to Step 3...")
            continue_btn = await page.query_selector('button:has-text("Continue"), input[value*="Continue"], .btn[type="submit"]')
            if continue_btn:
                await continue_btn.click()
                await page.wait_for_timeout(4000)
                
                print("\nStep 2: Looking for Edit buttons on Step 3 (billing)")
                
                # Find ALL edit buttons on Step 3
                all_edit_buttons = await page.query_selector_all('a:has-text("Edit"), button:has-text("Edit"), input[value*="Edit"]')
                print(f"📝 Found {len(all_edit_buttons)} total Edit buttons/links")
                
                for i, btn in enumerate(all_edit_buttons):
                    href = await btn.get_attribute('href')
                    text = await btn.inner_text()
                    print(f"   {i+1}. Text: '{text}' | href: {href}")
                
                # Look specifically for address_book_process links  
                address_edit_links = await page.query_selector_all('a[href*="address_book_process"]')
                print(f"\n🏠 Found {len(address_edit_links)} address_book_process links")
                
                for i, link in enumerate(address_edit_links):
                    href = await link.get_attribute('href')
                    text = await link.inner_text()
                    print(f"   {i+1}. Text: '{text}' | href: {href}")
                    
                    # Test clicking the first one if it exists
                    if i == 0:
                        print(f"\n🧪 Testing click on first address edit link...")
                        current_url = page.url
                        await link.click()
                        await page.wait_for_load_state('networkidle')
                        await page.wait_for_timeout(2000)
                        
                        new_url = page.url
                        print(f"📍 Before: {current_url}")
                        print(f"📍 After:  {new_url}")
                        
                        if 'address_book_process' in new_url:
                            print("✅ Successfully navigated to address edit page")
                            
                            # Look for save button and test the redirect
                            save_btn = await page.query_selector('input[type="submit"][value*="Save"], button:has-text("Save")')
                            if save_btn:
                                print("🔄 Testing save and redirect...")
                                await save_btn.click()
                                await page.wait_for_load_state('networkidle')
                                await page.wait_for_timeout(3000)
                                
                                final_url = page.url
                                print(f"📍 Final: {final_url}")
                                
                                if 'one_page_checkout' in final_url:
                                    content = await page.inner_text('body')
                                    is_billing = 'billing' in content.lower() or 'payment' in content.lower()
                                    is_shipping = 'shipping' in content.lower() and 'billing' not in content.lower()
                                    
                                    if is_billing:
                                        print("🎉 SUCCESS: Returned to Step 3 (billing)!")
                                    elif is_shipping:
                                        print("❌ PROBLEM: Returned to Step 2 (shipping)")
                                    else:
                                        print("❓ Unclear which step we're on")
                                else:
                                    print("❌ Did not return to checkout")
            
            print("\n⏳ Keeping browser open for inspection...")
            await page.wait_for_timeout(15000)
            
        except Exception as e:
            print(f"❌ Debug error: {e}")
            
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(debug_edit_buttons())
#!/usr/bin/env python3

import asyncio
from playwright.async_api import async_playwright

async def debug_cart_add():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        
        try:
            print("🔍 DEBUG: Finding products and add to cart buttons...")
            
            # Go to main page to see available products
            await page.goto('http://localhost:8000/')
            await page.wait_for_load_state('networkidle')
            await page.wait_for_timeout(2000)
            
            # Look for product links
            product_links = await page.query_selector_all('a[href*="products_id"]')
            print(f"📦 Found {len(product_links)} product links")
            
            if product_links:
                # Click on first product
                first_product = product_links[0]
                href = await first_product.get_attribute('href')
                print(f"🛒 Going to first product: {href}")
                
                await first_product.click()
                await page.wait_for_load_state('networkidle')
                await page.wait_for_timeout(3000)
                
                # Show page title to confirm we're on product page
                title = await page.title()
                print(f"📄 Page title: {title}")
                
                # Look for all buttons on the page
                all_buttons = await page.query_selector_all('button, input[type="submit"]')
                print(f"🔘 Found {len(all_buttons)} buttons/submit inputs:")
                
                for i, btn in enumerate(all_buttons[:10]):  # Show first 10
                    btn_text = await btn.inner_text() if await btn.inner_text() else await btn.get_attribute('value')
                    btn_id = await btn.get_attribute('id')
                    btn_class = await btn.get_attribute('class')
                    is_visible = await btn.is_visible()
                    
                    print(f"   {i+1}. Text: '{btn_text}' | ID: {btn_id} | Class: {btn_class} | Visible: {is_visible}")
                
                # Try to find and click an Add to Cart button
                add_buttons = await page.query_selector_all('button:has-text("Add"), input[value*="Add"], button:has-text("Cart"), input[value*="Cart"]')
                
                if add_buttons:
                    print(f"\n🛒 Found {len(add_buttons)} potential add to cart buttons")
                    
                    for btn in add_buttons:
                        is_visible = await btn.is_visible()
                        btn_text = await btn.inner_text() if await btn.inner_text() else await btn.get_attribute('value')
                        print(f"   Add button: '{btn_text}' | Visible: {is_visible}")
                        
                        if is_visible:
                            print(f"🔄 Clicking visible add button: '{btn_text}'")
                            await btn.click()
                            await page.wait_for_timeout(3000)
                            break
                
                # Now try to go to checkout
                print("\n🛒 Attempting to go to one page checkout...")
                await page.goto('http://localhost:8000/index.php?main_page=one_page_checkout')
                await page.wait_for_load_state('networkidle')
                await page.wait_for_timeout(3000)
                
                # Check checkout state
                url = page.url
                title = await page.title()
                print(f"📍 Checkout URL: {url}")
                print(f"📄 Checkout title: {title}")
                
                # Look for checkout steps
                steps = await page.query_selector_all('[id*="checkout-step"]')
                print(f"🔍 Found {len(steps)} checkout step elements:")
                
                for step in steps:
                    step_id = await step.get_attribute('id')
                    is_visible = await step.is_visible()
                    classes = await step.get_attribute('class')
                    print(f"   Step: {step_id} | Visible: {is_visible} | Classes: {classes}")
            
            print("\n⏳ Pausing for manual inspection (browser will stay open for 30 seconds)...")
            await page.wait_for_timeout(30000)
            
        except Exception as e:
            print(f"❌ Debug error: {e}")
            
        finally:
            await browser.close()
            print("✅ Debug completed")

if __name__ == "__main__":
    asyncio.run(debug_cart_add())
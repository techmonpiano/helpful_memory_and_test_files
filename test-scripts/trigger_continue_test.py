#!/usr/bin/env python3

import asyncio
from playwright.async_api import async_playwright

async def trigger_continue_test():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        
        try:
            print("🔄 TRIGGERING: Continue Button Test for Debug Logs")
            
            # Add product and go to checkout
            await page.goto('http://localhost:8000/index.php?main_page=product_info&products_id=1')
            await page.wait_for_load_state('networkidle')
            
            add_btn = await page.query_selector('.btn--add-to-cart')
            if add_btn:
                await add_btn.click()
                await page.wait_for_timeout(2000)
            
            await page.goto('http://localhost:8000/index.php?main_page=one_page_checkout')
            await page.wait_for_load_state('networkidle')
            await page.wait_for_timeout(3000)
            
            # Try to trigger a direct AJAX call to test our fix
            print("🔧 Triggering AJAX call to test OPC initialization...")
            
            response = await page.evaluate("""
                new Promise((resolve) => {
                    $.ajax({
                        type: 'POST',
                        url: '/index.php?main_page=controller&zpage=opc&step=checkout_shipping',
                        data: {
                            action: 'process'
                        },
                        success: function(data) {
                            console.log('AJAX Success:', data);
                            resolve({success: true, data: data});
                        },
                        error: function(xhr, status, error) {
                            console.log('AJAX Error:', error);
                            resolve({success: false, error: error, status: status});
                        }
                    });
                })
            """)
            
            print(f"📡 AJAX Response: {response}")
            await page.wait_for_timeout(2000)
            
        except Exception as e:
            print(f"❌ Error: {e}")
            
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(trigger_continue_test())
#!/usr/bin/env python3

import asyncio
from playwright.async_api import async_playwright

async def trigger_payment_template():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        
        try:
            print("🛒 Navigating to checkout...")
            await page.goto('http://localhost:8000/index.php?main_page=one_page_checkout')
            await page.wait_for_load_state('networkidle')
            await page.wait_for_timeout(2000)
            
            # Check current step and try to advance to step where Continue button would trigger checkout_payment
            current_url = page.url
            print(f"Current URL: {current_url}")
            
            # Try to get to Step 2 by simulating form submission
            print("🔄 Attempting to trigger checkout_payment template via AJAX...")
            
            # Try a direct AJAX call to checkout_shipping with action=process
            response = await page.evaluate("""
                new Promise((resolve) => {
                    $.ajax({
                        type: 'POST',
                        url: '/index.php?main_page=controller&zpage=opc&step=checkout_shipping',
                        data: {
                            action: 'process',
                            payment: 'moneyorder'  // Use a simple payment method
                        },
                        success: function(data) {
                            console.log('AJAX Success:', data);
                            resolve(data);
                        },
                        error: function(xhr, status, error) {
                            console.log('AJAX Error:', error);
                            resolve({error: error, status: status});
                        }
                    });
                })
            """)
            
            print("🔍 AJAX Response received:")
            print(str(response)[:500] + "..." if len(str(response)) > 500 else str(response))
            
            await page.wait_for_timeout(2000)
            
        except Exception as e:
            print(f"❌ Error: {e}")
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(trigger_payment_template())
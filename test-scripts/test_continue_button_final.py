#!/usr/bin/env python3

import asyncio
import sys
from playwright.async_api import async_playwright
import json
import time

async def test_continue_button():
    async with async_playwright() as p:
        # Launch browser with gui
        browser = await p.chromium.launch(
            headless=False,
            args=['--disable-web-security', '--disable-features=VizDisplayCompositor']
        )
        
        context = await browser.new_context()
        page = await context.new_page()
        
        print("🔧 Setting up network monitoring...")
        
        # Monitor network requests
        requests = []
        responses = []
        
        async def handle_request(request):
            if 'controller' in request.url and 'opc' in request.url:
                requests.append({
                    'url': request.url,
                    'method': request.method,
                    'timestamp': time.time()
                })
                
        async def handle_response(response):
            if 'controller' in response.url and 'opc' in response.url:
                try:
                    text = await response.text()
                    responses.append({
                        'url': response.url,
                        'status': response.status,
                        'text': text[:500] + '...' if len(text) > 500 else text,
                        'timestamp': time.time()
                    })
                    print(f"📡 AJAX Response: {response.status}")
                    print(f"📄 Content preview: {text[:200]}...")
                except:
                    responses.append({
                        'url': response.url,
                        'status': response.status,
                        'text': 'Could not read response text',
                        'timestamp': time.time()
                    })
        
        page.on('request', handle_request)
        page.on('response', handle_response)
        
        try:
            # Navigate to checkout
            print("🛒 Step 1: Going to checkout...")
            await page.goto('http://localhost:8000/index.php?main_page=one_page_checkout')
            await page.wait_for_load_state('networkidle')
            await page.wait_for_timeout(2000)
            
            # Quick check if we're at step 2 already
            step2_visible = await page.is_visible('#checkout-step-shipping:not(.d-none)')
            if step2_visible:
                print("✅ Already at Step 2 - testing Continue button...")
                
                # Wait for shipping methods to load
                await page.wait_for_timeout(3000)
                
                # Check if Continue button exists
                continue_btn = await page.query_selector('#shipping-methods-content-container .btn[type="submit"]')
                if continue_btn:
                    print("🔘 Found Continue button, clicking...")
                    
                    # Clear any existing logs
                    await page.evaluate('console.clear()')
                    
                    # Click Continue button and monitor response
                    await continue_btn.click()
                    
                    # Wait for AJAX to complete
                    await page.wait_for_timeout(3000)
                    
                    # Check if we advanced to Step 3
                    step3_visible = await page.is_visible('#checkout-step-billing:not(.d-none)')
                    if step3_visible:
                        print("✅ SUCCESS: Advanced to Step 3 (Billing)!")
                    else:
                        print("❌ FAILED: Still at Step 2, Continue button didn't work")
                        
                    # Get console logs
                    console_logs = await page.evaluate('console.log("Getting logs..."); []')
                    
                else:
                    print("❌ Continue button not found")
            else:
                print("⚠️ Not at Step 2, cannot test Continue button")
            
            # Show captured network activity
            print(f"\n📊 Network Summary:")
            print(f"   Requests captured: {len(requests)}")
            print(f"   Responses captured: {len(responses)}")
            
            for response in responses[-2:]:  # Show last 2 responses
                print(f"\n📡 Response {response['status']}: {response['url']}")
                print(f"📄 Content: {response['text']}")
                
        except Exception as e:
            print(f"❌ Error during testing: {e}")
            
        finally:
            await browser.close()
            print("✅ Test completed")

if __name__ == "__main__":
    asyncio.run(test_continue_button())
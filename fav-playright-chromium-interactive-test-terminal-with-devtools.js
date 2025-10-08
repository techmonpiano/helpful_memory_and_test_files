const { chromium } = require('playwright');

(async () => {
  console.log('🎭 Starting Terminal Mode Test with DevTools...');
  console.log('================================================');
  
  const browser = await chromium.launch({ 
    headless: false,
    devtools: true,  // This opens DevTools automatically
    args: [
      '--no-sandbox',
      '--disable-setuid-sandbox',
      '--disable-dev-shm-usage'
    ]
  });
  
  const context = await browser.newContext({
    viewport: { width: 1280, height: 800 }
  });
  
  const page = await context.newPage();
  
  // Enable console logging from the page
  page.on('console', msg => {
    console.log('📋 Page console:', msg.type(), msg.text());
  });
  
  page.on('pageerror', error => {
    console.error('❌ Page error:', error);
  });
  
  try {
    console.log('📱 Navigating to Claude Code GUI...');
    await page.goto('http://localhost:3050', { 
      waitUntil: 'networkidle',
      timeout: 30000 
    });
    
    console.log('⏳ Waiting for app to fully load...');
    await page.waitForTimeout(3000);
    
    console.log('🔍 Looking for Terminal button...');
    const terminalButton = await page.locator('button:has-text("Terminal")').first();
    
    if (await terminalButton.isVisible()) {
      console.log('✅ Found Terminal button');
      
      // Take a pre-click screenshot
      await page.screenshot({ 
        path: 'helpfulscripts/terminal-before-click.png',
        fullPage: true 
      });
      
      console.log('🖱️ Clicking Terminal button...');
      await terminalButton.click();
      
      console.log('⏳ Waiting for terminal modal to open...');
      await page.waitForTimeout(2000);
      
      // Check multiple possible terminal selectors
      const terminalSelectors = [
        '.xterm-screen',
        '.terminal-container',
        '[class*="terminal"]',
        '.xterm'
      ];
      
      let terminalFound = false;
      for (const selector of terminalSelectors) {
        const element = await page.locator(selector).first();
        if (await element.isVisible()) {
          console.log(`✅ Found terminal with selector: ${selector}`);
          terminalFound = true;
          break;
        }
      }
      
      if (terminalFound) {
        console.log('🖥️ Terminal is visible!');
        
        // Wait for Claude to potentially start
        console.log('⏳ Waiting for Claude Code to initialize...');
        await page.waitForTimeout(5000);
        
        // Take screenshot of terminal
        await page.screenshot({ 
          path: 'helpfulscripts/terminal-open.png',
          fullPage: true 
        });
        
        // Try to get terminal content
        try {
          const xterm = await page.locator('.xterm-rows, .xterm-screen').first();
          const content = await xterm.textContent();
          console.log('📝 Terminal content length:', content.length);
          if (content.length > 0) {
            console.log('📝 Terminal preview:', content.substring(0, 200));
          }
        } catch (e) {
          console.log('⚠️ Could not read terminal content:', e.message);
        }
        
        // Check for Claude-specific content
        const pageContent = await page.content();
        if (pageContent.includes('Welcome to Claude') || 
            pageContent.includes('Human:') || 
            pageContent.includes('Assistant:')) {
          console.log('✅ Claude Code appears to be running!');
        } else {
          console.log('⚠️ Claude Code welcome message not detected yet');
        }
        
      } else {
        console.log('❌ Terminal not visible after clicking button');
        await page.screenshot({ 
          path: 'helpfulscripts/terminal-not-visible.png',
          fullPage: true 
        });
      }
      
    } else {
      console.log('❌ Terminal button not found');
      
      // Debug: List all visible buttons
      const buttons = await page.locator('button').all();
      console.log(`📋 Found ${buttons.length} buttons on page:`);
      for (let i = 0; i < Math.min(5, buttons.length); i++) {
        const text = await buttons[i].textContent();
        console.log(`   Button ${i}: "${text}"`);
      }
      
      await page.screenshot({ 
        path: 'helpfulscripts/no-terminal-button.png',
        fullPage: true 
      });
    }
    
  } catch (error) {
    console.error('❌ Test error:', error);
    await page.screenshot({ 
      path: 'helpfulscripts/test-error.png',
      fullPage: true 
    });
  }
  
  console.log('\n' + '='.repeat(60));
  console.log('🔍 BROWSER REMAINS OPEN WITH DEVTOOLS');
  console.log('You can now:');
  console.log('  - Inspect the page in DevTools');
  console.log('  - Check the Console for errors');
  console.log('  - View Network requests');
  console.log('  - Interact with the terminal manually');
  console.log('\n❌ Close the browser window when done');
  console.log('='.repeat(60) + '\n');
  
  // Keep the script running indefinitely
  await new Promise(() => {});
  
})();
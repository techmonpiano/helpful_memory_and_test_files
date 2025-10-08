# Playwright Interactive Debugging Patterns - June 2025

## 🎭 Overview

This document contains the most effective, battle-tested Playwright patterns for interactive debugging and browser automation. These scripts were developed during the Generator Parts white space debugging session and represent the gold standard for "watch me work" Playwright automation.

## 📁 Script Collection

### 1. **`classic-interactive-playwright.py`** - The Gold Standard
**Best for**: Full debugging sessions where you want complete control

#### Features:
- ✅ **Visible browser** + **DevTools open automatically**
- ✅ **Interactive command line interface** (click, type, eval, screenshot)
- ✅ **Slow motion execution** (500ms delay so you can watch)
- ✅ **Real-time console logging** from browser
- ✅ **Comprehensive error handling**
- ✅ **Cross-origin request support** for testing
- ✅ **Maximized browser window**

#### Usage:
```bash
python3 classic-interactive-playwright.py
```

#### Interactive Commands Available:
- `click SELECTOR` - Click any element
- `type SELECTOR TEXT` - Type text into input fields
- `eval CODE` - Execute JavaScript in browser
- `screenshot` - Take screenshot with timestamp
- `goto URL` - Navigate to new URL
- `wait TIME` - Wait for specified seconds
- `find TEXT` - Find elements containing text
- `help` - Show command help
- `quit` - Close browser and exit

#### Example Session:
```
🎭 Command: goto http://localhost:8000/admin
🎭 Command: click #username
🎭 Command: type #username admin
🎭 Command: eval document.title
🎭 Command: screenshot
🎭 Command: quit
```

### 2. **`simple-watch-playwright.py`** - The Easiest
**Best for**: Just watching browser automation with minimal interaction

#### Features:
- ✅ **Super simple setup** - minimal configuration
- ✅ **1 second slow motion** (easy to follow actions)
- ✅ **Basic essential commands** (scroll, click, screenshot)
- ✅ **Automatic page analysis** on load
- ✅ **Built-in page structure detection**

#### Usage:
```bash
python3 simple-watch-playwright.py
```

#### What It Does Automatically:
1. **Analyzes page structure** (element count, images, forms, jQuery detection)
2. **Takes initial screenshot**
3. **Provides simple interaction commands**
4. **Keeps browser open for 30 seconds after completion**

#### Simple Commands:
- `scroll` - Scroll down page
- `click SELECTOR` - Click element
- `js CODE` - Run JavaScript
- `screenshot` - Take screenshot
- `done` - Finish session

### 3. **`playwright-template.py`** - The Universal Pattern
**Best for**: Copy-paste template for any automation task

#### Features:
- ✅ **Battle-tested browser settings**
- ✅ **Perfect timeouts and error handling**
- ✅ **Ready-to-modify template structure**
- ✅ **Example functions for common tasks**
- ✅ **Production-ready configuration options**

#### Template Structure:
```python
async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,           # Set to True for production
            devtools=True,           # Set to False for production  
            slow_mo=500,             # Remove for production speed
        )
        
        page = await browser.new_page()
        page.set_default_timeout(30000)  # 30 second timeout
        
        try:
            # YOUR CODE HERE
            await page.goto("http://localhost:8000")
            # Add your automation logic
            
        except Exception as e:
            await page.screenshot(path="error_screenshot.jpg")
            raise
        finally:
            await browser.close()
```

## 🛠️ Perfect Browser Settings

### Gold Standard Launch Configuration:
```python
browser = await p.chromium.launch(
    headless=False,           # Always visible for debugging
    devtools=True,           # DevTools open automatically  
    slow_mo=500,             # 500ms delay between actions
    args=[
        '--start-maximized',      # Start maximized
        '--disable-web-security', # Allow cross-origin (testing only)
        '--disable-features=TranslateUI', # No translate popups
        '--no-first-run',         # Skip first-run setup
    ]
)
```

### Essential Page Settings:
```python
page = await browser.new_page()
page.set_default_timeout(30000)  # 30 second timeout
page.set_default_navigation_timeout(45000)  # 45 second navigation
await page.set_viewport_size({'width': 1920, 'height': 1080})

# Enable logging
page.on("console", lambda msg: print(f"🖥️  CONSOLE: {msg.text}"))
page.on("pageerror", lambda error: print(f"❌ PAGE ERROR: {error}"))
```

## 🔧 Essential Patterns

### 1. Reliable Navigation Pattern:
```python
print("🌐 Navigating to page...")
response = await page.goto(url, wait_until='networkidle', timeout=45000)
print(f"✅ Page loaded with status: {response.status}")
await page.wait_for_timeout(2000)  # Let page stabilize
```

### 2. Safe Element Interaction:
```python
try:
    await page.click(selector, timeout=5000)
    print(f"✅ Clicked: {selector}")
except Exception as e:
    print(f"❌ Click failed: {e}")
    await page.screenshot(path="click_error.jpg")
```

### 3. JavaScript Evaluation with Error Handling:
```python
try:
    result = await page.evaluate('''() => {
        return {
            title: document.title,
            url: window.location.href,
            elementCount: document.querySelectorAll('*').length
        };
    }''')
    print(f"📊 Page analysis: {result}")
except Exception as e:
    print(f"❌ JavaScript evaluation failed: {e}")
```

### 4. Screenshot with Timestamp:
```python
timestamp = await page.evaluate('Date.now()')
filename = f"screenshot_{timestamp}.jpg"
await page.screenshot(path=filename, type='jpeg', quality=80)
print(f"📸 Screenshot saved: {filename}")
```

## 🎯 Common Use Cases

### CSS Debugging Pattern:
```python
async def debug_css_issues(url):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, devtools=True)
        page = await browser.new_page()
        
        await page.goto(url)
        
        # Find layout issues
        issues = await page.evaluate('''() => {
            const problems = [];
            document.querySelectorAll('*').forEach(el => {
                const rect = el.getBoundingClientRect();
                if (rect.left < 0 || rect.right > window.innerWidth) {
                    problems.push({
                        tag: el.tagName,
                        selector: el.id ? '#' + el.id : '.' + el.className.split(' ')[0],
                        left: Math.round(rect.left),
                        width: Math.round(rect.width)
                    });
                }
            });
            return problems.slice(0, 10);
        }''')
        
        print(f"Found {len(issues)} CSS layout issues:")
        for issue in issues:
            print(f"  {issue['tag']}{issue['selector']} - left: {issue['left']}px")
        
        await page.wait_for_timeout(30000)  # Keep open for inspection
        await browser.close()
```

### Form Testing Pattern:
```python
async def test_form_workflow(url):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=1000)
        page = await browser.new_page()
        
        await page.goto(url)
        
        # Fill form step by step (visible with slow_mo)
        await page.fill("input[name='email']", "test@example.com")
        await page.fill("input[name='password']", "password123")
        await page.click("button[type='submit']")
        
        # Wait for result
        await page.wait_for_load_state('networkidle')
        
        # Check result
        success = await page.query_selector(".success-message")
        if success:
            print("✅ Form submission successful")
        else:
            print("❌ Form submission failed")
            await page.screenshot(path="form_error.jpg")
        
        await browser.close()
```

### Page Analysis Pattern:
```python
async def analyze_page_structure(url):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)  # Fast analysis
        page = await browser.new_page()
        
        await page.goto(url)
        
        analysis = await page.evaluate('''() => {
            return {
                title: document.title,
                elementCount: document.querySelectorAll('*').length,
                imageCount: document.querySelectorAll('img').length,
                linkCount: document.querySelectorAll('a').length,
                formCount: document.querySelectorAll('form').length,
                scriptCount: document.querySelectorAll('script').length,
                hasJQuery: typeof jQuery !== 'undefined',
                hasBootstrap: !!document.querySelector('[class*="bootstrap"]'),
                viewport: {
                    width: window.innerWidth,
                    height: window.innerHeight
                }
            };
        }''')
        
        print("📊 Page Structure Analysis:")
        for key, value in analysis.items():
            print(f"   {key}: {value}")
        
        await browser.close()
        return analysis
```

## 🚀 Quick Start Guide

### For Immediate Interactive Debugging:
```bash
cd /home/user1/shawndev1/helpful_memory_and_test_files/
python3 simple-watch-playwright.py
```

### For Advanced Debugging Sessions:
```bash
python3 classic-interactive-playwright.py
```

### For Building Custom Automation:
1. Copy `playwright-template.py`
2. Modify the "YOUR CODE HERE" section
3. Add your specific automation logic
4. Run and watch it work!

## 💡 Pro Tips

### 1. Slow Motion for Debugging:
- Use `slow_mo=1000` to watch actions clearly
- Use `slow_mo=500` for normal debugging
- Remove `slow_mo` for production speed

### 2. Error Handling Best Practices:
```python
try:
    await page.click(selector)
except Exception as e:
    print(f"❌ Error: {e}")
    await page.screenshot(path="error_debug.jpg")
    # Continue with alternative action or raise
```

### 3. Keep Browser Open for Manual Inspection:
```python
print("🔒 Browser staying open for inspection...")
await page.wait_for_timeout(60000)  # 1 minute
```

### 4. Console Logging for JavaScript Debugging:
```python
page.on("console", lambda msg: print(f"JS: {msg.text}"))
page.on("pageerror", lambda error: print(f"ERROR: {error}"))
```

### 5. Take Screenshots at Key Points:
```python
await page.screenshot(path="before_action.jpg")
await page.click("button")
await page.screenshot(path="after_action.jpg")
```

## 🔄 Common Modifications

### Switch to Headless Mode:
```python
browser = await p.chromium.launch(headless=True)  # No visible browser
```

### Different Browser:
```python
browser = await p.firefox.launch(headless=False, devtools=True)  # Firefox
browser = await p.webkit.launch(headless=False)  # Safari/WebKit
```

### Mobile Emulation:
```python
device = p.devices['iPhone 12']
page = await browser.new_page(**device)
```

### Custom User Agent:
```python
await page.set_user_agent('Mozilla/5.0 (Custom Bot) Chrome/91.0')
```

## 📝 Testing Checklist

When using these scripts for debugging:

- [ ] **Browser launches visibly** with DevTools open
- [ ] **Console messages appear** in terminal
- [ ] **Actions are slow enough to follow** (500-1000ms delay)
- [ ] **Screenshots save successfully** to expected location
- [ ] **Error handling works** (try clicking non-existent element)
- [ ] **Browser closes cleanly** on completion or Ctrl+C

## 🎉 Success Stories

### Generator Parts CSS Debugging (June 2025):
- **Problem**: White block extending beyond viewport
- **Tool Used**: `quick-css-analysis.py` (based on these patterns)
- **Result**: Identified container positioning issue in 30 seconds
- **Fix Applied**: JavaScript override modification
- **Outcome**: ✅ Issue resolved, layout matches live site

### Interactive Command Success:
- **Scenario**: Live debugging session during development
- **Tool Used**: `classic-interactive-playwright.py`
- **Commands**: `click`, `eval`, `screenshot` for real-time analysis
- **Benefit**: Immediate feedback and iterative problem solving

## 🔗 Related Tools

These patterns work perfectly with:
- **CSS Debug Bookmarklet** - For manual browser analysis
- **Console Debug Scripts** - For JavaScript-based debugging
- **DevTools Integration** - For visual inspection alongside automation

## 📚 File Locations

**Memory Bank**: `/home/user1/shawndev1/ASAPWebNew/memorybank/playwright-interactive-debugging-patterns-june2025.md`
**Toolkit**: `/home/user1/shawndev1/helpful_memory_and_test_files/`

**Script Files**:
- `classic-interactive-playwright.py`
- `simple-watch-playwright.py` 
- `playwright-template.py`

---

**Created**: June 23, 2025  
**Context**: ASAPWebNew CSS debugging and automation  
**Status**: Production-ready, battle-tested patterns  
**Last Updated**: Generator Parts white space resolution session
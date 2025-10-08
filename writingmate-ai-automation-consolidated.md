# WritingMate.ai Automation - Consolidated Reference Guide
**Last Updated:** June 25, 2025  
**Purpose:** Single reference for all WritingMate.ai browser automation knowledge

## 🚀 Quick Reference

### Essential Selectors
| Element | Selector | Purpose |
|---------|----------|---------|
| Message Input | `textarea[data-testid="multimodal-input"]` | Send messages |
| Model Selector | `button[aria-haspopup="dialog"]` | Open model dropdown |
| Search Box | `input[placeholder*="Search"]` | Filter models |
| Model Options | `span.block.truncate.font-medium` | Available models |
| Reasoning Toggle | `button[data-testid="message-reasoning-toggle"]` | Expand thinking |
| Reasoning Content | `div[data-testid="message-reasoning"]` | Thought process |
| Assistant Messages | `[data-testid="message-assistant"]` | AI responses |
| Message Content | `[data-testid="message-content"] .prose` | Response text |

### Command Line Usage
```bash
# Basic usage
python3 multi_llm_automation.py --model="gpt-4" --message="Your question here"

# Examples
python3 multi_llm_automation.py --model="gpt-4.1" --message="Explain quantum computing"
python3 multi_llm_automation.py --model="claude" --message="Write a Python function"
python3 multi_llm_automation.py --model="gemini-thinking" --message="Solve: 25×4 + 15÷3"
```

### Claude Trigger Phrases
- "check what **[model]** via writingmate has to say"
- "ask **[model]** via WritingMate: **[question]**"
- "use WritingMate to ask **[model]**: **[question]**"
- "get **[model]**'s response via WritingMate"

## 🎯 Model Name Mapping

### GPT Models
- Input: `"gpt4"`, `"gpt-4"`, `"chatgpt4"`, `"gpt4o"`, `"gpt-4.1"`, `"gpt4.1"`
- Target: `"GPT-4o"` or `"GPT-4.1"`

### Claude Models
- Input: `"claude"`, `"claude3.5"`, `"sonnet"`, `"haiku"`
- Target: `"Claude 3.5 Sonnet"` or `"Claude 3.5 Haiku"`

### Gemini Models
- Input: `"gemini"`, `"gemini2.5"`, `"thinking"`, `"reasoning"`
- Target: `"Gemini 2.5 Flash Preview 05-20 (thinking)"`

### Other Models
- Llama, Mistral, Cohere - use exact model names

## 💻 Working Code Examples

### 1. Browser Launch with Persistent Session
```python
from playwright.async_api import async_playwright

browser = await p.chromium.launch_persistent_context(
    user_data_dir="/tmp/writingmate_session",
    headless=False,
    devtools=True,
    args=['--start-maximized']
)
page = browser.pages[0] if browser.pages else await browser.new_page()
await page.goto("https://app.writingmate.ai/")
```

### 2. Send Message (Enter Key Method)
```python
# Wait for and fill textarea
textarea = await page.wait_for_selector('textarea[data-testid="multimodal-input"]')
await textarea.click()
await textarea.fill(message)
await textarea.press('Enter')  # This works reliably!
```

### 3. Model Switching
```python
# Click model selector
model_button = await page.wait_for_selector('button[aria-haspopup="dialog"]')
await model_button.click()

# Search for model
search_input = await page.wait_for_selector('input[placeholder*="Search"]')
await search_input.fill(model_name)

# Select specific model
model_spans = await page.query_selector_all('span.block.truncate.font-medium')
for span in model_spans:
    text = await span.text_content()
    if target_text in text:
        await span.click()
        break
```

### 4. Response Capture (Fixed)
```python
# Get assistant messages
assistant_messages = await page.query_selector_all('[data-testid="message-assistant"]')
if assistant_messages:
    last_message = assistant_messages[-1]
    
    # Try multiple content selectors
    content_selectors = [
        '[data-testid="message-content"] .prose',
        '[data-testid="message-content"]', 
        '.prose.prose-md',
        '.prose'
    ]
    
    for selector in content_selectors:
        content_elem = await last_message.query_selector(selector)
        if content_elem:
            response_text = await content_elem.text_content()
            break
```

### 5. Reasoning Extraction
```python
# Check for reasoning content
reasoning_button = await page.query_selector('button[data-testid="message-reasoning-toggle"]')
if reasoning_button:
    await reasoning_button.click()
    await page.wait_for_timeout(1000)
    
    reasoning_div = await page.query_selector('div[data-testid="message-reasoning"]')
    if reasoning_div:
        reasoning_text = await reasoning_div.text_content()
```

## 🔧 Common Issues & Solutions

### Issue 1: Response Capture Gets User Message
**Problem:** Script captures user's message instead of AI response  
**Root Cause:** Wrong DOM selector targeting  
**Solution:** Use `[data-testid="message-assistant"]` not generic message selectors

### Issue 2: Model Search Fails
**Problem:** Can't find model in dropdown  
**Root Cause:** Timing issues or incorrect search term  
**Solution:** Add delays and use exact model names from mapping

### Issue 3: Send Button Not Working
**Problem:** Click on send button fails  
**Solution:** Use Enter key method instead - much more reliable

### Issue 4: Reasoning Not Captured
**Problem:** Thinking/reasoning content missing  
**Solution:** Look for "Reasoned for X seconds" text and click toggle button

## ⏱️ Critical Timing Requirements
- Model selector click → search input: **3+ seconds**
- Search typing → results: **2 seconds**
- Model selection → verification: **4 seconds**
- Message send → response: **10-15 seconds**
- Character typing speed: **0.05s per character**

## 📁 Script Locations
- **Main automation:** `/home/user1/shawndev1/claude-code-with-other-llms-via-browser/multi_llm_automation.py`
- **Interactive version:** `writingmate_devtools_interactive.py`
- **Gemini-specific:** `final_gemini_switch.py`
- **Production ready:** `fixed_model_switching.py`
- **Debug tools:** `debug_search_input.py`

## 🎭 Interactive Commands (When Using Interactive Script)
```bash
send <message>     # Send message to current model
switch <model>     # Change AI model  
models            # List available models
current           # Show active model
gemini            # Quick switch to Gemini thinking
screenshot        # Document current state
quit              # Exit cleanly
```

## 🔍 Debugging Tips

### Enable Console Logging
```python
# Add to see what's happening
page.on("console", lambda msg: print(f"Browser console: {msg.text}"))
```

### Take Screenshots
```python
await page.screenshot(path=f"debug_{datetime.now():%Y%m%d_%H%M%S}.png")
```

### Check Element Visibility
```python
element = await page.query_selector(selector)
if element:
    is_visible = await element.is_visible()
    bounding_box = await element.bounding_box()
```

## 🚨 Important Notes

### Authentication
- WritingMate requires login (Google/email)
- Session persists with `user_data_dir`
- May need manual login on first run

### Model Availability
- Not all models always available
- Some require specific subscription levels
- Gemini thinking models have special "(thinking)" suffix

### Rate Limiting
- Be respectful of the service
- Add delays between requests
- Don't automate excessive usage

## 📊 Success Indicators
- ✅ Browser launches with saved session
- ✅ Model selector shows current model name
- ✅ Messages send and responses appear
- ✅ Reasoning content expands when available
- ✅ Response text captured (not user message)

## 🔗 Related Files
- **Memory bank:** `/home/user1/shawndev1/claude-code-with-other-llms-via-browser/memory-bank/writingmate-ai-automation-session-june25-2025.md`
- **Terminal investigation:** `/home/user1/shawndev1/claude-code-wrapper/memory-bank/terminal-black-screen-investigation-2025-06-25.md`
- **CLAUDE_UNIVERSAL.md:** Contains trigger phrases for automated usage

---

**Pro Tip:** When Claude sees "check what gpt-4.1 via writingmate has to say", it will automatically run the multi_llm_automation.py script with appropriate parameters!
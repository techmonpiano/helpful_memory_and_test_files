from playwright.sync_api import sync_playwright
import time

TEST_MESSAGE = "Test message from Playwright at " + time.strftime("%Y-%m-%d %H:%M:%S")
GUI_URL = "http://localhost:3050"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, args=["--auto-open-devtools-for-tabs"])
    context = browser.new_context()
    page = context.new_page()
    print(f"Opening {GUI_URL} ...")
    page.goto(GUI_URL)

    # Wait for chat input
    page.wait_for_selector('textarea[data-testid="message-input"]', timeout=10000)
    textarea = page.locator('textarea[data-testid="message-input"]')
    textarea.fill(TEST_MESSAGE)
    textarea.press("Enter")
    print(f"Sent test message: {TEST_MESSAGE}")

    # Wait for the message to appear in chat (MessageDisplay)
    page.wait_for_selector(f'text={TEST_MESSAGE}', timeout=10000)
    print("Message appeared in chat history.")

    # Click the terminal icon/button
    page.wait_for_selector('button[title*="Open Terminal"]', timeout=10000)
    page.click('button[title*="Open Terminal"]')
    print("Clicked terminal icon to open xterm.js terminal.")

    # Wait for terminal to appear (look for xterm.js container)
    page.wait_for_selector('.xterm', timeout=10000)
    print("Terminal is visible.")

    # Optionally, check if the message appears in terminal output (if applicable)
    # This depends on your app's design; for now, just pause for manual inspection
    print("Test complete. Inspect the GUI and terminal window.")
    time.sleep(10)

    browser.close()

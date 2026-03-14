import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

print("☠️ Initiating Advanced Stealth Scraper (Level 3)...")

options = Options()
# 1. Real-world stealth arguments used by illegal scrapers
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

driver = webdriver.Chrome(options=options)

# 2. Chrome DevTools Protocol (CDP) Hack
# This strips the 'webdriver' flag out of the browser engine before the page even loads
driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    "source": """
        Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
        window.chrome = { runtime: {} };
    """
})

try:
    driver.get("http://localhost:3000/index.html")
    print("🕵️‍♂️ Evading UI tracking... Analyzing DOM structure...")
    time.sleep(2) # Brief wait to let the page load
    
    # 3. DOM INJECTION ATTACK (Bypassing the physical mouse completely)
    # Scrapers execute JS directly to trigger events and extract data instantly
    print("💥 Executing JavaScript DOM Injection to extract data...")
    target_btn = driver.find_element(By.CLASS_NAME, "trap-btn")
    
    # We command the browser to click the button via code, not via the mouse
    driver.execute_script("arguments[0].click();", target_btn)
    
    print("📡 Payload injected bypassing physical kinematics. Awaiting data...")
    time.sleep(5)

finally:
    driver.quit()
    print("✅ Scraper connection terminated.")
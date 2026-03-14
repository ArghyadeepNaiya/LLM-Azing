import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains

# ==========================================
# 🛑 HACKATHON TOGGLE: SWITCH BOT MODES HERE
# Modes: "ILLEGAL" (Bad Scraper) or "LEGAL" (Googlebot/Copyright Scanner)
BOT_MODE = "LEGAL" 
# ==========================================

print(f"🚀 Launching Bot in {BOT_MODE} mode...")

chrome_options = Options()

# Configure bot identity based on mode
if BOT_MODE == "LEGAL":
    # Good bots proudly announce who they are
    chrome_options.add_argument("user-agent=Googlebot/2.1 (+http://www.google.com/bot.html)")
else:
    # Bad bots spoof a normal Windows machine
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)

driver = webdriver.Chrome(options=chrome_options)

# --- FCrDNS / ASN SIMULATION FIX ---
# We must use CDP (Chrome DevTools Protocol) to natively inject headers in Selenium.
if BOT_MODE == "LEGAL":
    driver.execute_cdp_cmd('Network.setExtraHTTPHeaders', {
        'headers': {'x-verified-asn': 'TRUE'}
    })

try:
    driver.get("http://localhost:3000/index.html")
    driver.maximize_window()
    time.sleep(2)

    if BOT_MODE == "ILLEGAL":
        print("🕵️ Executing illegal spoofing maneuvers...")
        # Bad bots try to fake kinematics, which our ML catches
        driver.execute_script("window.scrollTo({top: 500, behavior: 'smooth'});")
        time.sleep(1)
        
        target = driver.find_element(By.CLASS_NAME, "trap-btn")
        actions = ActionChains(driver)
        actions.move_to_element_with_offset(target, 10, 10).perform()
        time.sleep(0.5)
        target.click()
        
    elif BOT_MODE == "LEGAL":
        print("✅ Executing polite, legal crawl...")
        # Good bots don't spoof kinematics. They just click instantly, but their ASN header protects them.
        target = driver.find_element(By.CLASS_NAME, "trap-btn")
        target.click()

    print(f"📡 {BOT_MODE} payload delivered. Check the Admin Dashboard!")
    time.sleep(8)

finally:
    driver.quit()
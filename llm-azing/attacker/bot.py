import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains

print("="*50)
print("🏴‍☠️ THREATSHIELD ATTACK SIMULATOR")
print("="*50)
mode = input("Enter 'legal' to simulate an authorized crawler, or 'illegal' for a fraud bot: ").strip().lower()

chrome_options = Options()

if mode == 'legal':
    print("\n✅ Configuring as 'Googlebot' (Legal Crawler)...")
    chrome_options.add_argument("user-agent=Googlebot/2.1 (+http://www.google.com/bot.html)")
else:
    print("\n🛑 Configuring as Malicious Fraud Bot (Illegal)...")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)

driver = webdriver.Chrome(options=chrome_options)
actions = ActionChains(driver)

try:
    # 1. Load the Financial Portal
    driver.get("http://127.0.0.1:3000/index.html")
    driver.maximize_window()
    time.sleep(1)

    if mode == 'illegal':
        print("⚡ Executing high-speed credential stuffing & wire fraud...")
        
        # DEMO TRICK: Inject JS to spoof BOTH hardware fingerprints!
        print("💉 Spoofing Headless CPU & Dummy Audio DAC for guaranteed detection...")
        driver.execute_script("""
            ThreatShield.telemetry.canvasHash = 999999999;
            ThreatShield.telemetry.audioHash = 888888888;
        """)
        
        inputs = driver.find_elements(By.CLASS_NAME, "auth-input")
        inputs[0].send_keys("admin@threatshield.corp")
        inputs[1].send_keys("hacked_password_123")
        inputs[2].send_keys("0xBadGuyWalletAddress")
        inputs[3].send_keys("500000")
        
        target = driver.find_element(By.CLASS_NAME, "trap-btn")
        actions.move_to_element(target).perform()
        time.sleep(0.1)
        target.click()

    else:
        print("🔍 Executing polite indexing scan...")
        time.sleep(2)
        target = driver.find_element(By.CLASS_NAME, "trap-btn")
        target.click()

    print("📡 Payload delivered! Check the ThreatShield Admin Dashboard.")
    time.sleep(6) # Leave window open to see the Active Defense trap!

finally:
    driver.quit()
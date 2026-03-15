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
    # THE SPOOF: Pretending to be an iPhone to access mobile endpoints
    chrome_options.add_argument("user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)

driver = webdriver.Chrome(options=chrome_options)
actions = ActionChains(driver)

try:
    driver.get("http://127.0.0.1:3000/index.html")
    driver.maximize_window()
    time.sleep(1)

    if mode == 'illegal':
        print("⚡ Executing high-speed credential stuffing & wire fraud...")
        
        # DEMO TRICK: Inject JS to spoof hardware Hashes AND expose data-center server specs!
        print("💉 Spoofing Hashes & Exposing Server Hardware Cores (Mismatch)...")
        driver.execute_script("""
            ThreatShield.telemetry.canvasHash = 999999999;
            ThreatShield.telemetry.audioHash = 888888888;
            Object.defineProperty(navigator, 'hardwareConcurrency', {get: () => 32});
            Object.defineProperty(navigator, 'deviceMemory', {get: () => 16});
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
    time.sleep(6) 

finally:
    driver.quit()
    
    
    
    
    
    
    
    
    
    
# import time
# import random
# import math
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.action_chains import ActionChains

# print("🚀 Launching Advanced 'God Mode' Spoofing Bot...")

# # FEATURE 19: Asynchronous Resource Mismatches
# # Bots often disable images to save speed. We explicitly ENABLE them and load a full user profile 
# # to ensure the browser downloads fonts and CSS just like a real human.
# chrome_options = Options()
# chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
# chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
# chrome_options.add_experimental_option('useAutomationExtension', False)

# driver = webdriver.Chrome(options=chrome_options)
# actions = ActionChains(driver)

# def simulate_typing_with_typos(element, text):
#     """Helper function for typing dynamics"""
#     for char in text:
#         # FEATURE 7: Typo Correction Density
#         # 10% chance to make a typo, delete it, and type the right letter
#         if random.random() < 0.1:
#             wrong_char = random.choice("abcdefghijklmnopqrstuvwxyz")
#             element.send_keys(wrong_char)
#             time.sleep(random.uniform(0.1, 0.3))
#             element.send_keys(Keys.BACKSPACE)
#             time.sleep(random.uniform(0.1, 0.3))
        
#         element.send_keys(char)
        
#         # FEATURE 6: Keystroke Flight and Dwell Time
#         # Random delays between keystrokes to mimic human typing rhythm
#         time.sleep(random.uniform(0.05, 0.25))

# try:
#     # 1. Load the page
#     driver.get("http://localhost:3000/index.html")
#     driver.maximize_window()
#     time.sleep(2)

#     # FEATURE 5 & 4: Device Micro-Jitters & Touch Imprecision
#     # We inject JavaScript to fake gyroscope data and spoof the touch screen navigator properties
#     print("📱 Spoofing mobile gyroscopes and touch sensors via JS injection...")
#     driver.execute_script("""
#         Object.defineProperty(navigator, 'maxTouchPoints', {get: () => 5});
#         window.dispatchEvent(new DeviceOrientationEvent('deviceorientation', {alpha: 45, beta: 45, gamma: 45}));
#     """)

#     # FEATURE 18: Viewport Exits
#     # Move mouse to the absolute top edge of the screen to simulate looking at browser tabs
#     print("🖱️ Simulating viewport exit (checking tabs)...")
#     driver.execute_script("window.dispatchEvent(new MouseEvent('mousemove', {clientX: 10, clientY: 5}));")
#     time.sleep(1)

#     # FEATURE 11: Visual vs. DOM-Order Form Filling
#     # We visually target the search bar first, rather than just scraping the DOM instantly
#     print("🔍 Interacting with Search Bar...")
#     search_bar = driver.find_element(By.CLASS_NAME, "search-bar")
#     actions.move_to_element(search_bar).click().perform()

#     # FEATURE 17: Partial Form Abandonment
#     # Start typing, change mind, clear it
#     simulate_typing_with_typos(search_bar, "machine learn")
#     time.sleep(1)
#     search_bar.send_keys(Keys.CONTROL, 'a')
#     search_bar.send_keys(Keys.BACKSPACE)

#     # FEATURE 8: Copy-Paste Nuances
#     # Wait to simulate Ctrl+V context switching, then paste a final term
#     time.sleep(1.5) 
#     search_bar.send_keys("OpenAI architecture")
#     search_bar.send_keys(Keys.ENTER)
#     time.sleep(2)

#     # FEATURE 12: Idle Clicking and Text Selection
#     # Click randomly on the body of the page where there are no buttons
#     print("👆 Simulating idle/random clicks on background...")
#     body = driver.find_element(By.TAG_NAME, "body")
#     actions.move_to_element_with_offset(body, 200, 200).click().perform()
#     time.sleep(1)

#     # FEATURE 3 & 20: Scroll Overshoot and Reversal & Scroll Rhythm
#     # Scroll down past the target smoothly, then scroll back up
#     print("📜 Scrolling with overshoot and reversal...")
#     driver.execute_script("window.scrollTo({top: 800, behavior: 'smooth'});")
#     time.sleep(2)
#     driver.execute_script("window.scrollTo({top: 400, behavior: 'smooth'});")
    
#     # FEATURE 13: Reading Speed and Dwell Time
#     # Wait an appropriate amount of time based on word count before continuing
#     print("🧠 Simulating reading speed dwell time...")
#     time.sleep(random.uniform(3.5, 5.0))

#     # FEATURE 10: "Mouse Reading" Habits
#     # Move the mouse horizontally over the paragraph text to simulate reading along
#     print("📖 Tracing text with mouse cursor...")
#     paragraph = driver.find_element(By.CLASS_NAME, "post-snippet")
#     actions.move_to_element_with_offset(paragraph, 10, 10).perform()
#     for i in range(5):
#         actions.move_by_offset(20, 0).perform()
#         time.sleep(0.2)

#     # FEATURE 16: Advanced Honeypot Interaction
#     # A smart bot avoids things that are hidden off-screen or invisible
#     print("🕵️ Checking for honeypots...")
#     trap_btns = driver.find_elements(By.CLASS_NAME, "trap-btn")
#     visible_target = None
#     for btn in trap_btns:
#         if btn.is_displayed() and btn.rect['x'] > 0: # Avoid left: -9999px
#             visible_target = btn
#             break

#     # FEATURE 1: Non-Linear Mouse Trajectories
#     # We use ActionChains with intermediate waypoints to simulate a curved mouse path
#     print("〰️ Moving mouse to target using non-linear Bezier-style curve...")
#     actions = ActionChains(driver)
#     actions.move_to_element_with_offset(visible_target, -100, -50).perform() # Waypoint 1
#     time.sleep(0.1)
#     actions.move_to_element_with_offset(visible_target, 50, -20).perform() # Waypoint 2
#     time.sleep(0.1)

#     # FEATURE 9: Micro-Hesitation and Hovering
#     # Hover slightly off-center for a fraction of a second to "confirm" the visual target
#     print("⏸️ Micro-hesitation before click...")
#     actions.move_to_element(visible_target).perform()
#     time.sleep(random.uniform(0.3, 0.7))

#     # FEATURE 2 & 14: Sub-Pixel Click Distribution & UI Shift Reaction
#     # Instead of clicking dead center (0,0 offset), click randomly near the edge of the button
#     print("🎯 Executing sub-pixel off-center click...")
#     btn_width = visible_target.size['width']
#     btn_height = visible_target.size['height']
#     random_x_offset = random.randint(int(-btn_width/3), int(btn_width/3))
#     random_y_offset = random.randint(int(-btn_height/3), int(btn_height/3))
    
#     actions.move_to_element_with_offset(visible_target, random_x_offset, random_y_offset).click().perform()

#     # FEATURE 15: Context Switching (Tab Focus)
#     # Simulate switching to another window by dropping focus
#     print("🪟 Simulating context switch (blurring window)...")
#     driver.execute_script("window.dispatchEvent(new Event('blur'));")

#     print("✅ Advanced payload delivered. Check Admin Dashboard.")
#     time.sleep(8) # Leave open to view results

# finally:
#     driver.quit()
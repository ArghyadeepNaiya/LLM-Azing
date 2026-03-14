import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains

print("🚀 Launching Advanced (but Detectable) Bot...")

chrome_options = Options()
# We still spoof the user agent so it's not caught by basic headers
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])

driver = webdriver.Chrome(options=chrome_options)
actions = ActionChains(driver)

try:
    # 1. Load the page
    driver.get("http://127.0.0.1:3000/index.html")
    driver.maximize_window()
    time.sleep(1)

    # --- DETECTION TRIGGER 1: STRAIGHT LINE MOVEMENT ---
    # We move to the button, but in one perfectly straight line.
    # Because sensor.js checks if the last 10 angles are identical,
    # this perfectly straight line will spike the linearityScore.
    print("🖱️ Moving in a mathematically perfect straight line...")
    target = driver.find_element(By.CLASS_NAME, "trap-btn")
    
    # move_to_element in Selenium is a direct linear path
    actions.move_to_element(target).perform()
    time.sleep(0.5)

    # --- DETECTION TRIGGER 2: RAPID INTERACTION ---
    # We will click the button before the 3-second mark.
    # This triggers the 'Rapid Interaction' penalty in your main.py.
    print("⚡ Clicking before the 3-second human threshold...")
    target.click()

    print("📡 Payload delivered. Your system should flag 'Non-human Kinematics'.")
    time.sleep(5)

finally:
    driver.quit()
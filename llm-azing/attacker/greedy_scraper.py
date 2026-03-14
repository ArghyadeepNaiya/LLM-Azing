# attacker/greedy_scraper.py
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

print("🏴‍☠️ Launching Greedy Scraper...")

chrome_options = Options()
# A basic bot that doesn't try to hide its automated nature well
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)")
driver = webdriver.Chrome(options=chrome_options)

try:
    driver.get("http://127.0.0.1:3000/index.html")
    driver.maximize_window()
    print("🕸️ Connected. Searching for data to steal...")
    
    # Simulate a bad bot immediately triggering the trap button to "Load More"
    time.sleep(1)
    trap = driver.find_element(By.CLASS_NAME, "trap-btn")
    print("🖱️ Clicking 'Load More' without any human kinematics...")
    trap.click()

    # The active_defense.js will now freeze this browser window with the CPU burner.
    print("⏳ Waiting for data to load (The trap is currently burning our CPU...)")
    time.sleep(5) # Wait for the Proof of Work to finish

    print("💰 Scraping posts...")
    titles = driver.find_elements(By.CLASS_NAME, "post-title")
    snippets = driver.find_elements(By.CLASS_NAME, "post-snippet")
    
    print("\n--- STOLEN DATA LOG ---")
    for i in range(len(titles)):
        print(f"Title: {titles[i].text}")
        print(f"Data: {snippets[i].text[:50]}...\n")
        
    print("😭 Wait... this data looks fake. The database is ruined!")

finally:
    driver.quit()
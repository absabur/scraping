from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import time
import re
import pyautogui
import logging
from selenium.webdriver.common.action_chains import ActionChains


# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize WebDriver with debugging options
options = webdriver.ChromeOptions()
options.debugger_address = "127.0.0.1:9210"
options.add_argument("user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 13_2 like Mac OS X)...")
driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 10)

# "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9210 --user-data-dir="C:\Users\absab\AppData\Local\Google\Chrome\User Data\Profile 1"
# %LOCALAPPDATA%
# chrome://version/
# https://chatgpt.com/c/dcbf62ec-e118-4299-a10c-4c182966cd8c

# setInterval(() => {
#   document.querySelectorAll("tr").forEach(tr => {
#     const tds = tr.querySelectorAll("td");
#     // প্রথম td বাদ দিয়ে বাকি সব remove করো
#     for (let i = 1; i < tds.length; i++) {
#       tds[i].remove();
#     }
#   });
# }, 4000);


# setInterval(() => {
#   document.querySelectorAll("tr").forEach(tr => {
#     // 1. Check if this <tr> contains the specific <span> inside .sn-investor-name-wrapper
#     const match = tr.querySelector('.sn-small-link.hidden-xs.null');
#     if (match) {
#       tr.remove(); // Remove the entire row
#       return; // Skip further processing for this <tr>
#     }
#     // 2. Keep only the first <td>, remove the rest
#     const tds = tr.querySelectorAll("td");
#     for (let i = 1; i < tds.length; i++) {
#       tds[i].remove();
#     }
#   });
# }, 4000);



def process_keywords(input_file, output_file):
    """Process keywords and save LinkedIn profile URLs to an output file."""
    try:
        # count = 1
        # while True:
        #     try:
        #         xpath = "//button[contains(text(), 'Load More Investors')]"
        #         # Wait for the button to be clickable
        #         button = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        #         # Scroll into view (optional)
        #         ActionChains(driver).move_to_element(button).perform()
        #         # Click the button
        #         print(f"Clicking 'Load More Investors'...({count})")
        #         button.click()
        #         # Wait for new content to load
        #         time.sleep(1)
        #         count += 1
        #     except Exception as e:
        #         continue
        
        
        
        xpath = "//tr//a[1]"
        # Find all matching elements
        elements = driver.find_elements(By.XPATH, xpath)
        # Extract hrefs
        hrefs = [el.get_attribute("href") for el in elements if el.get_attribute("href")]
        # Use pandas to store in DataFrame
        df = pd.DataFrame(hrefs, columns=["href"])
        # Save to Excel
        df.to_excel("15m-.xlsx", index=False)
        print(f"Extracted {len(hrefs)} hrefs and saved to 'hrefs_pandas.xlsx'.")

    except Exception as e:
        logging.error(f"Error processing keywords: {e}")

# Example usage
input_excel = "input.xlsx"  # Input file with keywords
output_excel = "output.xlsx"  # Output file to save URLs
process_keywords(input_excel, output_excel)
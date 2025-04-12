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
from selenium.common.exceptions import NoSuchElementException
import urllib.parse
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# print("Waiting 5500 second to load data: ---------------------")
# for i in range(1,5000):
#     time.sleep(1)
#     if i % 5 == 0:
#         print(f"{i} second passed away.")
    

# Initialize WebDriver with debugging options
options = webdriver.ChromeOptions()
options.debugger_address = "127.0.0.1:9230"
driver = webdriver.Chrome(options=options)

# "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9230 --user-data-dir="C:\Users\absab\AppData\Local\Google\Chrome\User Data\Profile 5"
# %LOCALAPPDATA%
# chrome://version/
# https://chatgpt.com/c/dcbf62ec-e118-4299-a10c-4c182966cd8c

def process_keywords():
    """Process keywords and save LinkedIn profile URLs to an output file."""
    try:
        urls = driver.find_elements(By.XPATH, "//a[@class='center-block']")

        data = []
        print(len(urls))
        
        for url in urls:
            text = url.text.strip()
            href = url.get_attribute("href")
            data.append([text, href])

        df = pd.DataFrame(data, columns=["Text", "URL"])
        df.to_excel(f"rest-s-f-A-Z-urls-{len(urls)}.xlsx", index=False, engine="openpyxl")

    except Exception as e:
        logging.error(f"Error processing keywords: {e}")

    finally:
        driver.quit()
        
process_keywords()


logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# Initialize WebDriver with debugging options
options = webdriver.ChromeOptions()
options.debugger_address = "127.0.0.1:9231"
driver = webdriver.Chrome(options=options)

# "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9231 --user-data-dir="C:\Users\absab\AppData\Local\Google\Chrome\User Data\Profile 6"
# %LOCALAPPDATA%
# chrome://version/
# https://chatgpt.com/c/dcbf62ec-e118-4299-a10c-4c182966cd8c

def process_keywords():
    """Process keywords and save LinkedIn profile URLs to an output file."""
    try:
        urls = driver.find_elements(By.XPATH, "//a[@class='center-block']")

        data = []
        print(len(urls))
        
        for url in urls:
            text = url.text.strip()
            href = url.get_attribute("href")
            data.append([text, href])

        df = pd.DataFrame(data, columns=["Text", "URL"])
        df.to_excel(f"food-b-A-Z-urls-{len(urls)}.xlsx", index=False, engine="openpyxl")

    except Exception as e:
        logging.error(f"Error processing keywords: {e}")

    finally:
        driver.quit()
        
process_keywords()

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
import re

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize WebDriver with debugging options
options = webdriver.ChromeOptions()
options.debugger_address = "127.0.0.1:9222"
driver = webdriver.Chrome(options=options)

# "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="C:\Users\absab\AppData\Local\Google\Chrome\User Data\Profile 1"
# %LOCALAPPDATA%
# chrome://version/
# https://chatgpt.com/c/dcbf62ec-e118-4299-a10c-4c182966cd8c


def get_first_samakai_profile(page):
    all_data = []

    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//div[@role="link"]')))
        
        results = driver.find_elements(By.XPATH, '//div[@role="link"]')

        for i in range(1, len(results)+1):
            element = driver.find_element(By.XPATH, "//input[@disabled]")
            value = element.get_attribute("value")
            while int(value) < page:
                back_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//button[@title="Next Page"]'))
                )
                time.sleep(1)
                driver.execute_script("arguments[0].click();", back_button)
                print(f"value: =================={value}")
                print(f"page: ==================={page}")
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//div[@role="link"]'))
                )
                element = driver.find_element(By.XPATH, "//input[@disabled]")
                value = element.get_attribute("value")
            logging.info(f"Processing item {i}...")

            try:
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//div[@role="link"]')))
                results = driver.find_elements(By.XPATH, '//div[@role="link"]')
                print("total result: =====",len(results))
                # Re-fetch fresh elements

                if i-1 >= len(results):
                    logging.warning("No more results available to process.")
                    break

                # Click profile
                driver.execute_script("arguments[0].scrollIntoView(true);", results[i-1])
                time.sleep(0.5)
                print(f"before click: =========={i-1}")
                
                
                MAX_RETRIES = 3
                for attempt in range(MAX_RETRIES):
                    try:
                        results = driver.find_elements(By.XPATH, '//div[@role="link"]')  # re-fetch elements
                        driver.execute_script("arguments[0].scrollIntoView(true);", results[i - 1])
                        time.sleep(0.5)
                        results[i - 1].click()

                        # Wait for profile detail to load
                        WebDriverWait(driver, 5).until(
                            EC.presence_of_element_located((By.XPATH, '//div[@id="fontevaDetailFields"]'))
                        )
                        break  # Success, exit retry loop

                    except Exception as e:
                        logging.warning(f"Attempt {attempt + 1} failed to open profile {i}: {e}")
                        if attempt == MAX_RETRIES - 1:
                            logging.error(f"Profile {i} could not be opened after {MAX_RETRIES} attempts.")
                        else:
                            time.sleep(1)  # small delay before retry
                            
                            
                print("afterclick: ==========")

                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//div[@id="fontevaDetailFields"]'))
                )

                data = {"name": "", "consultant": ""}
                try:
                    data["name"] = driver.find_element(
                        By.XPATH, '//div[@class="slds-grid slds-grid--align-spread slds-size--1-of-1"]'
                    ).text
                except Exception as e:
                    logging.error(f"Name not found for item {i}: {e}")

                try:
                    data["consultant"] = driver.find_element(
                        By.XPATH, '//div[@class="slds-p-bottom--xx-small fonteva-slds-text"]'
                    ).text
                except Exception as e:
                    logging.error(f"Consultant not found for item {i}: {e}")

                # Key-value pairs
                try:
                    keyvalues = driver.find_elements(
                        By.XPATH, '//div[@class="slds-p-vertical--xx-small slds-cell-wrap slds-text-body_medium"]'
                    )
                    for val in keyvalues:
                        if ':' in val.text:
                            key, value = val.text.split(':', 1)
                            data[key.strip()] = value.strip()
                except Exception as e:
                    logging.error(f"Key-value fields failed for item {i}: {e}")

                all_data.append(data)
                logging.info(f"Collected data for item {i}: {data}")

                # Click back
                try:
                    back_button = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, '//button[@class="slds-button"]'))
                    )
                    time.sleep(1)
                    driver.execute_script("arguments[0].click();", back_button)
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, '//div[@role="link"]'))
                    )
                except Exception as e:
                    logging.error(f"Back navigation failed for item {i}: {e}")
                    break  # Can't return, stop loop

            except Exception as e:
                logging.error(f"Error in item {i}: {e}")
                continue  # Go to next item

    except Exception as e:
        logging.error(f"Critical failure during scraping start: {e}")

    return all_data


def process_keywords():
    """Process keywords and save profile data to Excel."""
    try:
        results = []
        for i in range(20,21):
            page_results = get_first_samakai_profile(i)
            results.extend(page_results)
            if i % 3 == 0:
                df = pd.DataFrame(results)
                df.to_excel(f"output-a-{i*20}.xlsx", index=False, engine="openpyxl")
            

        if not results:
            logging.warning("No data was collected.")
            return

        df = pd.DataFrame(results)
        df.to_excel("output-a.xlsx", index=False, engine="openpyxl")
        logging.info("Data successfully written to output-a.xlsx")

    except Exception as e:
        logging.error(f"Unexpected error in process_keywords: {e}")

    finally:
        driver.quit()


process_keywords()
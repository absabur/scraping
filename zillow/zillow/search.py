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

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize WebDriver with debugging options
options = webdriver.ChromeOptions()
options.debugger_address = "127.0.0.1:9224"
driver = webdriver.Chrome(options=options)

# "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9224 --user-data-dir="C:\Users\absab\AppData\Local\Google\Chrome\User Data\Profile 3"
# %LOCALAPPDATA%
# chrome://version/
# https://chatgpt.com/c/dcbf62ec-e118-4299-a10c-4c182966cd8c

def detect_recaptcha(soup):
    print("=======================")
    """Check if a reCAPTCHA is present on the page."""
    # Check for common reCAPTCHA elements
    if (
        soup.find_all(class_="g-recaptcha")
        or soup.find_all("script", src=lambda src: src and "recaptcha" in src)
        or soup.find_all(class_="recaptcha-checkbox-border")
        or soup.find_all(class_="recaptcha")
    ):
        return True
    return False

def get_first_samakai_profile(url):
    """Search Google for a keyword and return the first valid LinkedIn profile link."""
    data = {
        "zillow_profile": "",
        "zillow_email": "",
        "zillow_phone": ""
    }

    try:
        email = ""
        phone = ""
        try:
            driver.get(url)
            WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, "//a[starts-with(@href, 'mailto:')]")))
            email = driver.find_element(By.XPATH, "//a[starts-with(@href, 'mailto:')]").get_attribute("href").replace("mailto:", "")
            phone = driver.find_element(By.XPATH, "//a[starts-with(@href, 'tel:')]").get_attribute("href").replace("tel:", "")
            print(email, phone)
        except Exception:
            pass
        data.update({
            "zillow_profile": url,
            "zillow_phone": phone,
            "zillow_email": email
        })

    except Exception as e:
        logging.error(f"Error processing keyword {url}: {e}")

    return data


def process_keywords(input_file):
    """Process keywords and save LinkedIn profile URLs to an output file."""
    try:
        keywords_df = pd.read_excel(input_file)
        # if "Search" not in keywords_df.columns:
        #     raise ValueError("Input Excel must have a 'Search' column")

        results = []
        for count, (_, row) in enumerate(keywords_df.iterrows()):
            if count >=5:  # Limit to 5 iterations for testing
                break

            url_data2 = get_first_samakai_profile(row["zillow_profile"])
                
            results.append({**row.to_dict(), **url_data2})
            if count % 50 == 0:
                results_df1 = pd.DataFrame(results)
                results_df1.to_excel(f"output-zillow-{count}.xlsx", index=False, engine="openpyxl")
                

        results_df = pd.DataFrame(results)
        results_df.to_excel(f"output-zillow-{count}.xlsx", index=False, engine="openpyxl")

    except Exception as e:
        logging.error(f"Error processing keywords: {e}")

    finally:
        driver.quit()

# Example usage
input_excel = "input.xlsx"  # Input file with keywords
process_keywords(input_excel)
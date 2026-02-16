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
from selenium.common.exceptions import TimeoutException, NoSuchElementException
def clear_browser_data(driver, origin_url):
    driver.delete_all_cookies()
    driver.execute_script("window.localStorage.clear();")
    driver.execute_script("window.sessionStorage.clear();")
    
    driver.execute_cdp_cmd("Storage.clearDataForOrigin", {
        "origin": origin_url,
        "storageTypes": "all"
    })


# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize WebDriver with debugging options
options = webdriver.ChromeOptions()
options.debugger_address = "127.0.0.1:9212"
driver = webdriver.Chrome(options=options)

# "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9212 --user-data-dir="C:\Users\absab\AppData\Local\Google\Chrome\User Data\Profile 3"
# %LOCALAPPDATA%
# chrome://version/
# https://chatgpt.com/c/dcbf62ec-e118-4299-a10c-4c182966cd8c


def get_first_linkedin_profile(keyword, count):
    """Search Google for a keyword and return the first valid LinkedIn profile link."""
    data = dict()

    try:
        try:
            driver.get(f"{keyword}")
            if count % 1 == 0:
                clear_browser_data(driver, "https://signal.nfx.com")
        except Exception as e:
            print(f"[GET ERROR] Failed to load URL: {e}")

        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//h1[contains(text(), ' ')]")))
        except TimeoutException:
            print("[WAIT ERROR] Timed out waiting for main <h1> element.")

        try:
            name = driver.find_element(By.XPATH, '//h1[@class="f3 f1-ns mv1"]')
            data["name"] = name.text
        except NoSuchElementException:
            print("[NAME ERROR] Could not find name <h1> tag.")

        try:
            titletext = driver.find_element(By.XPATH, '//div[@class="subheader white-subheader b pb1"]')
            spans = titletext.find_elements(By.TAG_NAME, "span")
            title = " ".join([span.text.strip() for span in spans])
            data["title"] = title
        except NoSuchElementException:
            print("[TITLE ERROR] Could not find title spans.")

        try:
            positionandcompany = driver.find_element(By.XPATH, '//div[@class="subheader lower-subheader pb2"]')
            data["positionandcompany"] = positionandcompany.text
        except NoSuchElementException:
            print("[POSITION ERROR] Could not find position and company.")

        try:
            address = driver.find_element(By.XPATH, "(//div[contains(@class, 'subheader') and contains(@class, 'lower-subheader')])[last()]//span[@class='nowrap']")
            data["address"] = address.text
        except NoSuchElementException:
            print("[ADDRESS ERROR] Could not find address.")

        try:
            companysite = driver.find_element(By.XPATH, "//span[@class='sn-linkset']//a")
            data["companysite"] = companysite.get_attribute("href")
        except NoSuchElementException:
            print("[COMPANYSITE ERROR] Could not find company site link.")

        # Optional: fallback values if above not found
        data.setdefault("name", "")
        data.setdefault("title", "")
        data.setdefault("positionandcompany", "")
        data.setdefault("address", "")
        data.setdefault("companysite", "")

        # Extract social links
        try:
            results = driver.find_elements(By.XPATH, '//a')
            for result in results:
                url = result.get_attribute("href")
                if not url:
                    continue

                if "linkedin.com/in/" in url:
                    data["linkedin"] = url
                elif "crunchbase.com" in url:
                    data["crunchbase"] = url
                elif "twitter.com" in url:
                    data["twitter"] = url
                elif "angel.com" in url:
                    data["angel"] = url
        except Exception as e:
            print(f"[SOCIAL LINK ERROR] Failed to extract links: {e}")

    except Exception as e:
        logging.error(f"Error processing keyword {keyword}: {e}")

    return data

def process_keywords(input_file, output_file):
    """Process keywords and save LinkedIn profile URLs to an output file."""
    try:
        keywords_df = pd.read_excel(input_file)

        results = []
        for count, (_, row) in enumerate(keywords_df.iterrows()):
            # if count >= 10:  # Limit to 5 iterations for testing
            #     break
            if count % 15 == 0:  # Limit to 5 iterations for testing
                time.sleep(10)

            keyword = f"{row["href"]}"
            logging.info(f"Processing keyword ({count}): {keyword}")
            url_data = get_first_linkedin_profile(keyword, count)
            time.sleep(1.5)  # Add a small delay to avoid overwhelming the server
            results.append({**row.to_dict(), **url_data})
            
            
            if count % 100 == 0:
                results_df = pd.DataFrame(results)
                results_df.to_excel(f"backup-{count}.xlsx", index=False, engine="openpyxl")
                logging.info(f"Results saved to {f"backup-{count}.xlsx"}")

        results_df = pd.DataFrame(results)
        results_df.to_excel(output_file, index=False, engine="openpyxl")
        logging.info(f"Results saved to {output_file}")

    except Exception as e:
        logging.error(f"Error processing keywords: {e}")

    finally:
        results_df = pd.DataFrame(results)
        results_df.to_excel(output_file, index=False, engine="openpyxl")
        logging.info(f"Results saved to {output_file}")
        driver.quit()

# Example usage
input_excel = "input2.xlsx"  # Input file with keywords
output_excel = "output.xlsx"  # Output file to save URLs
process_keywords(input_excel, output_excel)
# print(pyautogui.position())
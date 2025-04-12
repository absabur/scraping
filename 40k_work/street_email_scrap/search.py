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
options.debugger_address = "127.0.0.1:9222"
driver = webdriver.Chrome(options=options)

email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"

# "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="C:\Users\absab\AppData\Local\Google\Chrome\User Data\Profile 2"
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
def get_first_samakai_profile(keyword):
    """Search Google for a keyword and return the first valid LinkedIn profile link."""
    data = {
        "street_name": "",
        "street_company": "",
        "street_email": "",
        "street_licence": "",
    }

    try:
        driver.get(keyword)
        try:
            WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH, '//p[@id="IKeOjgzSDlbgvvo"]')))
            captcha = driver.find_element(By.XPATH, '//p[@id="IKeOjgzSDlbgvvo"]')
            if captcha:
                input("solve the captcha: ")
        except:
            pass

        licence = ""
        try:
            WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, "//div[@id='tabs-about-pane']")))
            licence = driver.find_element(By.XPATH, "//div[@id='tabs-about-pane']//p[@class='Body_base_gyzqw styled__AttributeText-uxpuhw-2 iQpCoS']").text
        except Exception:
            pass
        email = ""
        try:
            soup = BeautifulSoup(driver.page_source, "html.parser")
            scripts = soup.find_all("script")  

            emails = []
            for script in scripts:
                found_emails = re.findall(email_pattern, script.text)
                emails.extend(found_emails)

            email = emails[0] if emails else ""
            if len(emails) > 2:
                email = ",".join(map(str, emails))
        except Exception:
            pass
        name = ""
        company = ""
        try:
            name = driver.find_element(By.XPATH, "//h1[@class='PrimarySmall_base_-Z8WB PrimarySmall_fontWeightLight_vgc7E styled__NameComponentPrimaryHeader-sc-1iq7kub-5 kFYSmH']").text
            company = driver.find_element(By.XPATH, "//div[@id='profile-header-container']//p[2]").text

        except Exception:
            pass
        
        print("===")
        print(f"{name}, {company}, {email}, {licence}")
        print("===")
        data.update({
            "street_name": name,
            "street_company": company,
            "street_licence": licence,
            "street_email": email
        })

    except Exception as e:
        logging.error(f"Error processing keyword {keyword}: {e}")

    return data

def process_keywords(input_file):
    """Process keywords and save LinkedIn profile URLs to an output file."""
    try:
        keywords_df = pd.read_excel(input_file)
        # if "Search" not in keywords_df.columns:
        #     raise ValueError("Input Excel must have a 'Search' column")

        results = []
        for count, (_, row) in enumerate(keywords_df.iterrows()):
            if count == 1:  # Limit to 5 iterations for testing
                input("wait: ")
            time.sleep(2)
            pyautogui.scroll(500)
            pyautogui.scroll(-200)
            time.sleep(1)
            pyautogui.scroll(-500)
            pyautogui.scroll(300)
            time.sleep(3)
            pyautogui.scroll(500)
            pyautogui.scroll(-200)
            time.sleep(1)
            pyautogui.scroll(-500)
            pyautogui.scroll(300)
            time.sleep(2)

            url_data2 = get_first_samakai_profile(row["street_url"])
                
            results.append({**row.to_dict(), **url_data2})
            if count % 50 == 0:
                results_df1 = pd.DataFrame(results)
                results_df1.to_excel(f"output-street-{count}.xlsx", index=False, engine="openpyxl")
                

        results_df = pd.DataFrame(results)
        results_df.to_excel(f"output-street-{count}.xlsx", index=False, engine="openpyxl")

    except Exception as e:
        logging.error(f"Error processing keywords: {e}")
        results_df = pd.DataFrame(results)
        results_df.to_excel(f"output-street.xlsx", index=False, engine="openpyxl")

    finally:
        driver.quit()

# Example usage
input_excel = "input.xlsx"  # Input file with keywords
process_keywords(input_excel)


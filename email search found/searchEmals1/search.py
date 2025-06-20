from selenium import webdriver
from selenium.webdriver.common.by import By
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

# Initialize WebDriver with debugging options
options = webdriver.ChromeOptions()
options.debugger_address = "127.0.0.1:9222"
driver = webdriver.Chrome(options=options)

# "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="C:\Users\absab\AppData\Local\Google\Chrome\User Data\Profile 1"
# %LOCALAPPDATA%
# chrome://version/
# https://chatgpt.com/c/dcbf62ec-e118-4299-a10c-4c182966cd8c

email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"

def captchaSolve(count, encoded_keyword):
    print("CAPTCHA detected. Please solve it manually.")
    if count % 7 == 0:
        time.sleep(100)
    if count >= 2:
        driver.get(f"https://www.google.com/search?q={encoded_keyword}")        
        # pyautogui.click(1373, 10)
        time.sleep(0.7)

    time.sleep(0.5)
    pyautogui.click(1328, 191)
    time.sleep(0.7)
    pyautogui.click(1484, 648)
    time.sleep(5)

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


def get_search_results(encoded_keyword, name):
    keyword = urllib.parse.quote_plus(encoded_keyword)
    """Search Google for a keyword and return the first valid LinkedIn profile link."""
    data = dict()
    try:
        driver.get(f"https://www.google.com/search?q={keyword}")

        soup = BeautifulSoup(driver.page_source, "html.parser")
        count = 1

        while detect_recaptcha(soup):
            captchaSolve(count, encoded_keyword)
            soup = BeautifulSoup(driver.page_source, "html.parser")
            count += 1
        results = driver.find_elements(By.XPATH, '//div[@jscontroller="SC7lYd"]')
        if not results:
            logging.warning("No results found. Check XPath or page loading issues.")
            return data
        countEmail = 1
        for result in results:
            url = result.find_element(By.XPATH, './/a[@jsname="UWckNb"]').get_attribute(
                "href"
            )
            if not url:
                continue
            description = ""
            try:
                description = result.find_element(
                    By.XPATH, './/div[@class="kb0PBd A9Y9g"]'
                ).text
            except NoSuchElementException:
                print("Element not found.")
            except Exception as e:
                print(f"An error occurred: {e}")

            title = result.find_element(By.XPATH, ".//h3").text

            emails = re.findall(email_pattern, description)
            # Split name into words
            name_words = re.findall(r'\b\w+\b', name)

            title_words = title.lower()
            match_count = sum(1 for word in name_words if re.search(rf'\b{re.escape(word.lower())}\b', title_words))
            percentage = round((match_count / len(name_words)) * 100, 2) if name_words else 0

            words_desc = description.lower()
            match_count_desc = sum(1 for word in name_words if re.search(rf'\b{re.escape(word.lower())}\b', words_desc))
            percentage_desc = round((match_count_desc / len(name_words)) * 100, 2) if name_words else 0

            words_email = " ".join(map(str, emails)).lower()
            match_count_email = sum(1 for word in name_words if re.search(re.escape(word.lower()), words_email))
            percentage_email = round((match_count_email / len(name_words)) * 100, 2) if name_words else 0
            
            if len(emails) > 0:
                if countEmail >=3:
                    break
                data[f"email-{countEmail}"] = ",".join(map(str, emails))
                data[f"email-{countEmail}-url"] = url
                data[f"email-{countEmail}-title"] = title
                data[f"email-{countEmail}-description"] = description
                data[f"name-in-email-{countEmail}"] = percentage_email
                data[f"name-in-title-{countEmail}"] = percentage
                data[f"name-in-description-{countEmail}"] = percentage_desc
                countEmail += 1
    except Exception as e:
        logging.error(f"Error processing keyword {keyword}: No Result")

    return data

def get_search_results_email(keyword, column):
    
    """Search Google for a keyword and return the first valid LinkedIn profile link."""
    data = dict()
    try:
        driver.get(f'https://www.google.com/search?q={keyword}')

        soup = BeautifulSoup(driver.page_source, "html.parser")
        count = 1

        while detect_recaptcha(soup):
            captchaSolve(count, keyword)
            soup = BeautifulSoup(driver.page_source, "html.parser")
            count += 1

        results = driver.find_elements(By.XPATH, '//div[@jscontroller="SC7lYd"]')
        if not results:
            logging.warning("No results found. Check XPath or page loading issues.")
            return data
        for result in results:
            fulltext = result.text
            match = re.search(str(keyword), str(fulltext))
            if match:
                description = ""
                title = ""
                url = ""
                try:
                    url = result.find_element(By.XPATH, './/a[@jsname="UWckNb"]').get_attribute(
                        "href"
                    )
                    title = result.find_element(By.XPATH, ".//h3").text
                    description = result.find_element(
                        By.XPATH, './/div[@class="kb0PBd A9Y9g"]'
                    ).text
                except NoSuchElementException:
                    print("Element not found.")
                except Exception as e:
                    print(f"An error occurred: {e}")
                data[f"url-{column}"] = url
                data[f"title-{column}"] = title
                data[f"description-{column}"] = description
                break
    except Exception as e:
        print("error: ===============" + e)
    
    return data

def process_keywords(input_file):
    """Process keywords and save LinkedIn profile URLs to an output file."""
    try:
        keywords_df = pd.read_excel(input_file)
        results = []
        for count, (index, row) in enumerate(keywords_df.iterrows()):
            # if count >= 30:
            #     break
            if count % 8 == 0:
                time.sleep(13)
                
            url_data2 = dict()
            url_data3 = dict()

            cname = "" if str(row.get("Contact Name", "")).strip().lower() == "nan" else str(row.get("Contact Name", "")).strip()
            org = "" if str(row.get("Organization", "")).strip().lower() == "nan" else str(row.get("Organization", "")).strip()
            dept = "" if str(row.get("Department", "")).strip().lower() == "nan" else str(row.get("Department", "")).strip()
            position = "" if str(row.get("Position Title", "")).strip().lower() == "nan" else str(row.get("Position Title", "")).strip()


            # Create the keyword
            keyword = f"{cname} {org} {dept} {position}".strip()
            logging.info(f"Processing keyword ({count}): {keyword}")
            url_data = get_search_results(keyword, row["Contact Name"])
            time.sleep(0.7)

            keyword = ""
            keyword = f'{row["risky"]}'
            if pd.notna(keyword) and str(keyword).strip().lower() != 'nan' and str(keyword).strip():
                url_data2 = get_search_results_email(keyword, "risky")
            time.sleep(0.7)

            keyword = ""
            keyword = f'{row["First Unverifiable Email"]}'
            if pd.notna(keyword) and str(keyword).strip().lower() != 'nan' and str(keyword).strip():              
                url_data3 = get_search_results_email(keyword, "fue")
            time.sleep(0.7)
            
            results.append({**row.to_dict(), **url_data, **url_data2, **url_data3})
            if count % 100 == 0:
                results_df = pd.DataFrame(results)
                current_time = datetime.now()  # Get current date and time
                formatted_time = current_time.strftime("%Y-%m-%d_%H-%M-%S")
                results_df.to_excel(f"output-{formatted_time}-{count}.xlsx", index=False, engine="openpyxl")
                logging.info(f"Results saved to output-{formatted_time}-{count}.xlsx")

    except Exception as e:
        logging.error(f"Error processing keywords: {e}")

    finally:     
        current_time = datetime.now()  # Get current date and time
        formatted_time = current_time.strftime("%Y-%m-%d_%H-%M-%S")

        results_df = pd.DataFrame(results)
        results_df.to_excel(f"output-final-{formatted_time}.xlsx", index=False, engine="openpyxl")
        logging.info(f"Results saved to output-final-{formatted_time}.xlsx")
        driver.quit()

input_excel = "input.xlsx"
output_excel = "output.xlsx"
process_keywords(input_excel)

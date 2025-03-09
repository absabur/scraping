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

def get_first_zillow_profile(keyword):
    """Search Google for a keyword and return the first valid LinkedIn profile link."""
    data = {
        "zillow_profile": "",
        "match_percentage_zillow": "",
        "zillow_title": "",
        "zillow_email": ""
    }

    try:
        driver.get(f"https://www.google.com/search?q={keyword + ' "zillow"'}")
        
        soup = BeautifulSoup(driver.page_source, "html.parser")
        count = 1
        
        while detect_recaptcha(soup):
            print("CAPTCHA detected. Please solve it manually.")
            if count >= 3:
                pyautogui.click(2657,10)
                time.sleep(1)
                
            time.sleep(0.5)
            pyautogui.click(2617,142)
            time.sleep(1)
            pyautogui.click(2768,602)
            time.sleep(5)
            soup = BeautifulSoup(driver.page_source, "html.parser")
            count+=1
            
        WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, '//a[@jsname="UWckNb"]')))

        results = driver.find_elements(By.XPATH, '//a[@jsname="UWckNb"]')
        if not results:
            logging.warning("No results found. Check XPath or page loading issues.")
            return data

        def preprocess(text):
            """Preprocess text for keyword matching."""
            cleaned_text = re.sub(r'[^a-zA-Z\s]', '', text)
            return set(cleaned_text.lower().split())

        for result in results:
            url = result.get_attribute("href")
            if not url:
                continue

            if "zillow.com/profile/" in url:
                title = result.find_element(By.XPATH, './/h3').text
                keywords1 = preprocess(title)
                keywords2 = preprocess(keyword)
                matching_keywords = [kw for kw in keywords2 if kw in keywords1]
                match_percentage = f"{round((len(matching_keywords) / len(keywords2)) * 100, 2)}%"
                # driver.get(url)
                email = ""
                # try:
                #     email = driver.find_element(By.XPATH, "//a[starts-with(@href, 'mailto:')]").text
                # except Exception:
                #     pass
                data.update({
                    "zillow_profile": url,
                    "match_percentage_zillow": match_percentage,
                    "zillow_title": title,
                    "zillow_email": email
                })
                break

    except Exception as e:
        logging.error(f"Error processing keyword {keyword}: {e}")

    return data
def get_first_samakai_profile(keyword):
    """Search Google for a keyword and return the first valid LinkedIn profile link."""
    data = {
        "samaki_profile": "",
        "match_percentage_samaki": "",
        "samaki_title": "",
        "samaki_email": ""
    }

    try:
        driver.get(f"https://www.google.com/search?q={keyword}")
        
        soup = BeautifulSoup(driver.page_source, "html.parser")
        count = 1
        
        while detect_recaptcha(soup):
            print("CAPTCHA detected. Please solve it manually.")
            if count >= 3:
                pyautogui.click(2657,10)
                time.sleep(1)
                
            time.sleep(0.5)
            pyautogui.click(2617,142)
            time.sleep(1)
            pyautogui.click(2768,602)
            time.sleep(5)
            soup = BeautifulSoup(driver.page_source, "html.parser")
            count+=1
            
        WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, '//a[@jsname="UWckNb"]')))

        results = driver.find_elements(By.XPATH, '//a[@jsname="UWckNb"]')
        if not results:
            logging.warning("No results found. Check XPath or page loading issues.")
            return data

        def preprocess(text):
            """Preprocess text for keyword matching."""
            cleaned_text = re.sub(r'[^a-zA-Z\s]', '', text)
            return set(cleaned_text.lower().split())

        for result in results:
            url = result.get_attribute("href")
            if not url:
                continue

            if "samaki.com/profile" in url:
                title = result.find_element(By.XPATH, './/h3').text
                keywords1 = preprocess(title)
                keywords2 = preprocess(keyword)
                matching_keywords = [kw for kw in keywords2 if kw in keywords1]
                match_percentage = f"{round((len(matching_keywords) / len(keywords2)) * 100, 2)}%"
                driver.get(url)
                email = ""
                phone = ""
                try:
                    WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, "//a[starts-with(@href, 'mailto:')]")))
                    email = driver.find_element(By.XPATH, "//a[starts-with(@href, 'mailto:')]").text
                    phone = driver.find_element(By.XPATH, "//span[@class='text-nowrap num']").text
                except Exception:
                    pass
                data.update({
                    "samaki_profile": url,
                    "match_percentage_samaki": match_percentage,
                    "samaki_title": title,
                    "samaki_phone": phone,
                    "samaki_email": email
                })
                break

    except Exception as e:
        logging.error(f"Error processing keyword {keyword}: {e}")

    return data

def get_first_linkedin_profile(keyword):
    """Search Google for a keyword and return the first valid LinkedIn profile link."""
    data = {
        "linkedinProfile": "",
        "linkedinPost": "",
        "rocket": "",
        "linkedin_title": ""
    }

    try:
        driver.get(f"https://www.google.com/search?q={keyword}")
        
        soup = BeautifulSoup(driver.page_source, "html.parser")
        count = 1
        
        while detect_recaptcha(soup):
            print("CAPTCHA detected. Please solve it manually.")
            if count >= 3:
                pyautogui.click(2657,10)
                time.sleep(1)
                
            time.sleep(0.5)
            pyautogui.click(2617,142)
            time.sleep(1)
            pyautogui.click(2768,602)
            time.sleep(5)
            soup = BeautifulSoup(driver.page_source, "html.parser")
            count+=1
            
        WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, '//a[@jsname="UWckNb"]')))

        results = driver.find_elements(By.XPATH, '//a[@jsname="UWckNb"]')
        if not results:
            logging.warning("No results found. Check XPath or page loading issues.")
            return data

        def preprocess(text):
            """Preprocess text for keyword matching."""
            cleaned_text = re.sub(r'[^a-zA-Z\s]', '', text)
            return set(cleaned_text.lower().split())

        for result in results:
            url = result.get_attribute("href")
            if not url:
                continue

            if "linkedin.com/in/" in url:
                title = result.find_element(By.XPATH, './/h3').text
                keywords1 = preprocess(title)
                keywords2 = preprocess(keyword)
                matching_keywords = [kw for kw in keywords2 if kw in keywords1]
                match_percentage = f"{round((len(matching_keywords) / len(keywords2)) * 100, 2)}%"
                data.update({
                    "linkedinProfile": url,
                    "match_percentage_linkedin": match_percentage,
                    "linkedin_title": title
                })
                break

        for result in results:
            url = result.get_attribute("href")
            if url and "linkedin.com/posts/" in url:
                data["linkedinPost"] = url
                break

        for result in results:
            url = result.get_attribute("href")
            if url and "rocketreach.co" in url:
                data["rocket"] = url
                break

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
            # if count >= 20:  # Limit to 5 iterations for testing
            #     break

            keyword = row["First"]+" "+row["Last"]+" "+row["COMPANY"]
            logging.info(f"Processing keyword ({count}): {keyword}")
            url_data1 = get_first_zillow_profile(row["First"]+" "+row["Last"]+" "+row["COMPANY"]+' "zillow"')
            url_data2 = get_first_samakai_profile(row["First"]+" "+row["Last"]+" "+row["COMPANY"]+' "samaki"')
            url_data3 = get_first_linkedin_profile(row["First"]+" "+row["Last"]+" "+row["COMPANY"]+", "+row["License Type"])
                
            results.append({**row.to_dict(), **url_data1, **url_data2, **url_data3})
            if count % 1000 == 0:
                results_df1 = pd.DataFrame(results)
                results_df1.to_excel(f"output-2nd-{count}.xlsx", index=False, engine="openpyxl")
                

        results_df = pd.DataFrame(results)
        results_df.to_excel(f"output-2nd-{count}.xlsx", index=False, engine="openpyxl")

    except Exception as e:
        logging.error(f"Error processing keywords: {e}")

    finally:
        driver.quit()

# Example usage
input_excel = "input.xlsx"  # Input file with keywords
process_keywords(input_excel)
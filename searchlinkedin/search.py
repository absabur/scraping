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
options.debugger_address = "127.0.0.1:9210"
driver = webdriver.Chrome(options=options)

# "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9210 --user-data-dir="C:\Users\absab\AppData\Local\Google\Chrome\User Data\Profile 7"
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

def get_first_linkedin_profile(keyword, name):
    """Search Google for a keyword and return the first valid LinkedIn profile link."""
    data = {
        "linkedin_title": "",
        "linkedinProfile": "",
        "match_linkedin_full": "",
        "match_linkedin_name": "",
    }

    try:
        driver.get(f"https://www.google.com/search?q={keyword}")
        
        soup = BeautifulSoup(driver.page_source, "html.parser")
        count = 1
        
        while detect_recaptcha(soup):
            print("CAPTCHA detected. Please solve it manually.")
            if count >= 3:
                pyautogui.click(1373,10)
                time.sleep(1)
                
            time.sleep(0.5)
            pyautogui.click(1337,142)
            time.sleep(1)
            pyautogui.click(1480,301)
            time.sleep(5)
            soup = BeautifulSoup(driver.page_source, "html.parser")
            count+=1
            
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//a[@jsname="UWckNb"]')))

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
                keywords2 = preprocess(name)
                keywords1_name = preprocess(title.partition(" - ")[0].strip())
                keywords2_name = keywords2
                matching_keywords = [kw for kw in keywords2 if kw in keywords1]
                match_percentage = f"{round((len(matching_keywords) / len(keywords2)) * 100, 2)}%"
                matching_keywords_name = [kw for kw in keywords2_name if kw in keywords1_name]
                match_linkedin_name = f"{round((len(matching_keywords_name) / len(keywords2_name)) * 100, 2)}%"
                data.update({
                    "linkedin_title": title,
                    "linkedinProfile": url,
                    "match_linkedin_full": match_percentage,
                    "match_linkedin_name": match_linkedin_name,
                })
                break

        # for result in results:
        #     keywords1 = preprocess(title)
        #     keywords2 = preprocess(name)
        #     keywords1_name = preprocess(title.partition(" - ")[0].strip())
        #     keywords2_name = keywords2
        #     matching_keywords = [kw for kw in keywords2 if kw in keywords1]
        #     match_percentage = f"{round((len(matching_keywords) / len(keywords2)) * 100, 2)}%"
        #     matching_keywords_name = [kw for kw in keywords2_name if kw in keywords1_name]
        #     match_linkedin_name = f"{round((len(matching_keywords_name) / len(keywords2_name)) * 100, 2)}%"
        #     url = result.get_attribute("href")
        #     title = result.find_element(By.XPATH, './/h3').text
        #     if url and "crunchbase.com/person" in url:
        #         data["CrunchbaseUrl"] = url
        #         data["CrunchbaseTitle"] = title
        #         data['CrunchbaseMatch'] = match_percentage
        #         data['CrunchbaseMatchName'] = match_linkedin_name
        #         break
            
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

def process_keywords(input_file, output_file):
    """Process keywords and save LinkedIn profile URLs to an output file."""
    try:
        keywords_df = pd.read_excel(input_file)
        # if "Search" not in keywords_df.columns:
        #     raise ValueError("Input Excel must have a 'Search' column")

        results = []
        for count, (_, row) in enumerate(keywords_df.iterrows()):
            # if count >= 20:  # Limit to 5 iterations for testing
            #     break
            if count % 27 == 0:  # Limit to 5 iterations for testing
                time.sleep(12)

            keyword = f"{row["First Name"]} {row["Last Name"]} - {row["Title"]} - {row["Organization"]}"
            logging.info(f"Processing keyword ({count}): {keyword}")
            url_data = get_first_linkedin_profile(keyword, f"{row["First Name"]} {row["Last Name"]}")
            results.append({**row.to_dict(), **url_data})
            time.sleep(0.8)

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
input_excel = "input.xlsx"  # Input file with keywords
output_excel = "output.xlsx"  # Output file to save URLs
process_keywords(input_excel, output_excel)
# print(pyautogui.position())
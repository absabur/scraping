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

# Initialize WebDriver with debugging options
options = webdriver.ChromeOptions()
options.debugger_address = "127.0.0.1:9224"
driver = webdriver.Chrome(options=options)

# "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9224 --user-data-dir="C:\Users\absab\AppData\Local\Google\Chrome\User Data\Profile 3"
# %LOCALAPPDATA%
# chrome://version/
# https://chatgpt.com/c/dcbf62ec-e118-4299-a10c-4c182966cd8c


email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
keywordArray = [
    "real estate",
    "realtor",
    "salesperson",
    "investor",
    "broker",
    "agent",
    "associate",
]

def captchaSolve(count, encoded_keyword):
    print("CAPTCHA detected. Please solve it manually.")
    if count % 7 == 0:
        time.sleep(240)
    if count >= 2:
        driver.get(f"https://www.google.com/search?q={encoded_keyword}")
        # pyautogui.click(2657,10)
        time.sleep(1)
        
    time.sleep(0.5)
    pyautogui.click(2617,142)
    time.sleep(1)
    pyautogui.click(2768,602)
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


def get_search_results(encoded_keyword, keywordWithHyphen, licence):
    keyword = urllib.parse.quote_plus(encoded_keyword)
    """Search Google for a keyword and return the first valid LinkedIn profile link."""
    data = {
        "linkedin_title": "",
        "linkedin_profile": "",
        "linkedin_percentage_full": "",
        "linkedin_percentage_name": "",
        "linkedin_keyword_count": "",
        "linkedin_keyword_match": "",
        "linkedin_location": "",
        "linkedin_description": "",
        "zillow_title": "",
        "zillow_profile": "",
        "zillow_path": "",
        "zillow_percentage_full": "",
        "zillow_percentage_name": "",
        "zillow_location": "",
        "zillow_description": "",
        "samaki_profile": "",
        "match_percentage_samaki_full": "",
        "match_percentage_samaki_name": "",
        "samaki_title": "",
        "samaki_licence": "",
        "samaki_licence_status": "",
        "samaki_phone": "",
        "samaki_email": "",
        "nystatemls_title": "",
        "nystatemls_profile": "",
        "nystate_email": "",
        "nystatemls_percentage_name": "",
        "nystatemls_keyword_count": "",
        "nystatemls_keyword_match": "",
        "nystatemls_location": "",
        "nystatemls_description": "",
        "our_team_url":   "",
        "our_team_title": "",
        "our_team_location":  "",
        "our_team_keyword_count": "",
        "our_team_keyword_match": "",
        "our_team_description":   "",
        "compass_listing": "",
        "compass_email": "",
        "compass_keyword_count": "",
        "compass_keyword_match": "",
        "compass_description": "",
        "homes_url": "",
        "homes_title": "",
        "homes_email": "",
        "homes_keyword_count": "",
        "homes_keyword_match": "",
        "homes_description": "",
        "onekey_title": "",
        "onekey_url": "",
        "onekey_email": "",
        "onekey_keyword_count": "",
        "onekey_keyword_match": "",
        "onekey_match": "",
        "onekey_match_name": "",
        "onekey_description": "",
        "mystate_title": "",
        "mystate_url": "",
        "mystate_email": "",
        "mystate_keyword_count": "",
        "mystate_keyword_match": "",
        "mystate_match": "",
        "mystate_match_name": "",
        "mystate_description": "",
        "street_title": "",
        "street_url": "",
        "street_match": "",
        "street_match_name": "",
    }

    try:
        driver.get(f"https://www.google.com/search?q={keyword}")

        soup = BeautifulSoup(driver.page_source, "html.parser")
        count = 1

        while detect_recaptcha(soup):
            captchaSolve(count, encoded_keyword)
            soup = BeautifulSoup(driver.page_source, "html.parser")
            count += 1

        # try:
        #     WebDriverWait(driver, 3).until(
        #         EC.presence_of_element_located((By.XPATH, '//a[@jsname="UWckNb"]'))
        #     )
        # except:
        #     pass

        results = driver.find_elements(By.XPATH, '//div[@jscontroller="SC7lYd"]')
        if not results:
            logging.warning("No results found. Check XPath or page loading issues.")
            return data

        def preprocess(text):
            """Preprocess text for keyword matching."""
            cleaned_text = re.sub(r"[^a-zA-Z\s]", "", text)
            return set(cleaned_text.lower().split())

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
            location = ""
            if "new york" in description.lower():
                location = "New York"
            elif "ny" in description.lower():
                location = "NY"
            keywordCountLinkedin = 0
            keywordMatch = ""
            for keywordA in keywordArray:
                if keywordA in description.lower():
                    keywordCountLinkedin += 1
                    keywordMatch += f"{keywordA}, "

            keywords1 = preprocess(title)
            keywords2 = preprocess(keywordWithHyphen)
            keywords1_name = preprocess(title.partition(" - ")[0].strip())
            keywords2_name = preprocess(keywordWithHyphen.partition(" - ")[0].strip())
            matching_keywords = [kw for kw in keywords2 if kw in keywords1]
            match_percentage = (
                f"{round((len(matching_keywords) / len(keywords2)) * 100, 2)}%"
            )
            matching_keywords_name = [
                kw for kw in keywords2_name if kw in keywords1_name
            ]
            match_percentage_name = f"{round((len(matching_keywords_name) / len(keywords2_name)) * 100, 2)}%"

            emails = re.findall(email_pattern, description)

            if len(emails) > 0:
                data[f"email-{countEmail}"] = ",".join(map(str, emails))
                data[f"email-{countEmail}-url"] = url
                data[f"email-{countEmail}-title"] = title
                data[f"email-{countEmail}-description"] = description
                data[f"email-{countEmail}-location"] = location
                data[f"email-{countEmail}-keyword-count"] = keywordCountLinkedin
                data[f"email-{countEmail}-keyword-match"] = keywordMatch
                countEmail += 1

            if "linkedin.com/in" in url and data["linkedin_title"] == "":
                data.update(
                    {
                        "linkedin_title": title,
                        "linkedin_profile": url,
                        "linkedin_percentage_full": match_percentage,
                        "linkedin_percentage_name": match_percentage_name,
                        "linkedin_keyword_count": keywordCountLinkedin,
                        "linkedin_keyword_match": keywordMatch,
                        "linkedin_location": location,
                        "linkedin_description": description,
                    }
                )

            if "zillow.com/profile" in url and data["zillow_title"] == "":
                zillowPath = result.find_element(
                    By.XPATH, './/div[@class="byrV5b"]'
                ).text
                data.update(
                    {
                        "zillow_title": title,
                        "zillow_profile": url,
                        "zillow_path": zillowPath,
                        "zillow_percentage_full": match_percentage,
                        "zillow_percentage_name": match_percentage_name,
                        "zillow_location": location,
                        "zillow_description": description,
                    }
                )

            if "nystatemls.com/profiles" in url and data["nystatemls_title"] == "":
                driver.get(url)
                soup = BeautifulSoup(driver.page_source, "html.parser")
                emails = re.findall(email_pattern, soup.get_text())
                
                email = ""
                if len(emails) > 0:
                    email = ",".join(map(str, emails))
                
                keywords2 = preprocess(keywordWithHyphen)
                keywords2_name = preprocess(keywordWithHyphen.partition(" Of ")[0].strip())
                matching_keywords_name = [
                    kw for kw in keywords2_name if kw in keywords1_name
                ]
                match_percentage_name = f"{round((len(matching_keywords_name) / len(keywords2_name)) * 100, 2)}%"
                data.update(
                    {
                        "nystatemls_title": title,
                        "nystatemls_profile": url,
                        "nystate_email": email,
                        "nystatemls_percentage_name": match_percentage_name,
                        "nystatemls_keyword_count": keywordCountLinkedin,
                        "nystatemls_keyword_match": keywordMatch,
                        "nystatemls_location": location,
                        "nystatemls_description": description,
                    }
                )
            if "compass.com/listing" in url and data["compass_listing"] == "":
                driver.get(url)
                soup = BeautifulSoup(driver.page_source, "html.parser")

                emails = re.findall(email_pattern, soup.get_text())
                
                email = ""
                if len(emails) > 0:
                    email = ",".join(map(str, emails))
                data.update(
                    {
                        "compass_listing": url,
                        "compass_email": email,
                        "compass_keyword_count": keywordCountLinkedin,
                        "compass_keyword_match": keywordMatch,
                        "compass_description": description,
                    }
                )
                driver.back()
            
            if "our team" in title.lower():
                data.update(
                    {
                        "our_team_url": url,
                        "our_team_title": title,
                        "our_team_location": location,
                        "our_team_keyword_count": keywordCountLinkedin,
                        "our_team_keyword_match": keywordMatch,
                        "our_team_description": description,
                    }
                )

            if "samaki.com/profile" in url and data["samaki_profile"] == "":
                driver.get(url)
                licenceN = driver.find_element(By.XPATH, "//div[@id='userInfoFlexBox']//div[2]//h5[1]").text
                license_number = re.search(r'\d+', licenceN).group()
                email = ""
                phone = ""
                try:
                    WebDriverWait(driver, 3).until(
                        EC.presence_of_element_located(
                            (By.XPATH, ".//a[starts-with(@href, 'mailto:')]")
                        )
                    )
                    email = driver.find_element(
                        By.XPATH, ".//a[starts-with(@href, 'mailto:')]"
                    ).text
                    phone = driver.find_element(
                        By.XPATH, ".//span[@class='text-nowrap num']"
                    ).text
                except Exception:
                    pass
                licence_status = "Not Match"
                if license_number == licence:
                    licence_status = "Match"
                data.update(
                    {
                        "samaki_profile": url,
                        "match_percentage_samaki_full": match_percentage,
                        "match_percentage_samaki_name": match_percentage_name,
                        "samaki_title": title,
                        "samaki_licence": license_number,
                        "samaki_licence_status": licence_status,
                        "samaki_phone": phone,
                        "samaki_email": email,
                    }
                )
                driver.back()

            if "mystatemls.com/profiles" in url and data["mystate_url"] == "":
                driver.get(url)
                soup = BeautifulSoup(driver.page_source, "html.parser")
                emails = re.findall(email_pattern, soup.get_text())
                
                email = ""
                if len(emails) > 0:
                    email = ",".join(map(str, emails))
                
                keywords2 = preprocess(keywordWithHyphen)
                keywords2_name = preprocess(keywordWithHyphen.partition(" Of ")[0].strip())
                matching_keywords_name = [
                    kw for kw in keywords2_name if kw in keywords1_name
                ]
                match_percentage_name = f"{round((len(matching_keywords_name) / len(keywords2_name)) * 100, 2)}%"
                data.update(
                    {
                        "mystate_url": url,
                        "mystate_title": title,
                        "mystate_email": email,
                        "mystate_keyword_count": keywordCountLinkedin,
                        "mystate_keyword_match": keywordMatch,
                        "mystate_match": match_percentage,
                        "mystate_match_name": match_percentage_name,
                        "mystate_description": description,
                    }
                )
                driver.back()
            
            if "streeteasy.com/profile" in url and data["street_url"] == "":
                keywords2 = preprocess(keywordWithHyphen)
                keywords2_name = preprocess(keywordWithHyphen.partition(" Bio, ")[0].strip())
                matching_keywords_name = [
                    kw for kw in keywords2_name if kw in keywords1_name
                ]
                match_percentage_name = f"{round((len(matching_keywords_name) / len(keywords2_name)) * 100, 2)}%"
                    
                data.update(
                    {
                        "street_url": url,
                        "street_title": title,
                        "street_match": match_percentage,
                        "street_match_name": match_percentage_name,
                    }
                )

            if "homes.com/property" in url and data["homes_url"] == "":
                driver.get(url)
                soup = BeautifulSoup(driver.page_source, "html.parser")

                scripts = soup.find_all("script")                

                emails = []
                for script in scripts:
                    found_emails = re.findall(email_pattern, script.text)
                    emails.extend(found_emails)
                
                if len(emails) > 2:
                    email = ",".join(map(str, emails))

                data.update(
                    {
                        "homes_url": url,
                        "homes_title": title,
                        "homes_email": email,
                        "homes_keyword_count": keywordCountLinkedin,
                        "homes_keyword_match": keywordMatch,
                        "homes_description": description,
                    }
                )
                driver.back()
                
            if "onekeymls.com/realtor/agents" in url and data["onekey_url"] == "":
                driver.get(url)
                soup = BeautifulSoup(driver.page_source, "html.parser")

                scripts = soup.find_all("script")  

                emails = []
                for script in scripts:
                    found_emails = re.findall(email_pattern, script.text)
                    emails.extend(found_emails)

                filtered_emails = [e for e in emails if e != "contact@onekeymls.com"]

                email = filtered_emails[0] if filtered_emails else ""
                if len(filtered_emails) > 2:
                    email = ",".join(map(str, filtered_emails))

                data.update(
                    {
                        "onekey_url": url,
                        "onekey_title": title,
                        "onekey_email": email,
                        "onekey_keyword_count": keywordCountLinkedin,
                        "onekey_keyword_match": keywordMatch,
                        "onekey_match": match_percentage,
                        "onekey_match_name": match_percentage_name,
                        "onekey_description": description,
                    }
                )
                driver.back()

    except Exception as e:
        logging.error(f"Error processing keyword {keyword}: No Result")

    return data

def get_search_results_zillow(encoded_keyword, keywordWithHyphen):
    keyword = urllib.parse.quote_plus(encoded_keyword)
    """Search Google for a keyword and return the first valid LinkedIn profile link."""
    data = {
        "z_zillow_title": "",
        "z_zillow_profile": "",
        "z_zillow_path": "",
        "z_zillow_percentage_full": "",
        "z_zillow_percentage_name": "",
        "z_zillow_location": "",
        "z_zillow_description": "",
        "z_street_url": "",
        "z_street_title": "",
        "z_street_match": "",
        "z_street_match_name": "",
        "z_onekey_url": "",
        "z_onekey_title": "",
        "z_onekey_email": "",
        "z_onekey_keyword_count": "",
        "z_onekey_keyword_match": "",
        "z_onekey_match": "",
        "z_onekey_match_name": "",
        "z_onekey_description": "",
        "Z_samaki_profile": "",
        "Z_match_percentage_samaki_full": "",
        "Z_match_percentage_samaki_name": "",
        "Z_samaki_title": "",
        "Z_samaki_licence": "",
        "Z_samaki_licence_status": "",
        "Z_samaki_phone": "",
        "Z_samaki_email": "",
    }

    try:
        driver.get(f"https://www.google.com/search?q={keyword}")

        soup = BeautifulSoup(driver.page_source, "html.parser")
        count = 1

        while detect_recaptcha(soup):
            captchaSolve(count, encoded_keyword)
            soup = BeautifulSoup(driver.page_source, "html.parser")
            count += 1

        # try:
        #     WebDriverWait(driver, 3).until(
        #         EC.presence_of_element_located((By.XPATH, '//a[@jsname="UWckNb"]'))
        #     )
        # except:
        #     pass

        results = driver.find_elements(By.XPATH, '//div[@jscontroller="SC7lYd"]')
        if not results:
            logging.warning("No results found. Check XPath or page loading issues.")
            return data

        def preprocess(text):
            """Preprocess text for keyword matching."""
            cleaned_text = re.sub(r"[^a-zA-Z\s]", "", text)
            return set(cleaned_text.lower().split())

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
            location = ""
            if "new york" in description.lower():
                location = "New York"
            elif "ny" in description.lower():
                location = "NY"
            keywordCountLinkedin = 0
            keywordMatch = ""
            for keywordA in keywordArray:
                if keywordA in description.lower():
                    keywordCountLinkedin += 1
                    keywordMatch += f"{keywordA}, "

            keywords1 = preprocess(title)
            keywords2 = preprocess(keywordWithHyphen)
            keywords1_name = preprocess(title.partition(" - ")[0].strip())
            keywords2_name = preprocess(keywordWithHyphen.partition(" - ")[0].strip())
            matching_keywords = [kw for kw in keywords2 if kw in keywords1]
            match_percentage = (
                f"{round((len(matching_keywords) / len(keywords2)) * 100, 2)}%"
            )
            matching_keywords_name = [
                kw for kw in keywords2_name if kw in keywords1_name
            ]
            match_percentage_name = f"{round((len(matching_keywords_name) / len(keywords2_name)) * 100, 2)}%"

            if "zillow.com/profile" in url and data["z_zillow_profile"] == "":
                zillowPath = result.find_element(
                    By.XPATH, './/div[@class="byrV5b"]'
                ).text
                data.update(
                    {
                        "z_zillow_title": title,
                        "z_zillow_profile": url,
                        "z_zillow_path": zillowPath,
                        "z_zillow_percentage_full": match_percentage,
                        "z_zillow_percentage_name": match_percentage_name,
                        "z_zillow_location": location,
                        "z_zillow_description": description,
                    }
                )
                
            if "streeteasy.com/profile" in url and data["z_street_url"] == "":
                keywords2 = preprocess(keywordWithHyphen)
                keywords2_name = preprocess(keywordWithHyphen.partition(" Bio, ")[0].strip())
                matching_keywords_name = [
                    kw for kw in keywords2_name if kw in keywords1_name
                ]
                match_percentage_name = f"{round((len(matching_keywords_name) / len(keywords2_name)) * 100, 2)}%"
                    
                data.update(
                    {
                        "z_street_url": url,
                        "z_street_title": title,
                        "z_street_match": match_percentage,
                        "z_street_match_name": match_percentage_name,
                    }
                )
                
            if "onekeymls.com/realtor/agents" in url and data["z_onekey_url"] == "":
                driver.get(url)
                soup = BeautifulSoup(driver.page_source, "html.parser")

                scripts = soup.find_all("script")  

                emails = []
                for script in scripts:
                    found_emails = re.findall(email_pattern, script.text)
                    emails.extend(found_emails)

                filtered_emails = [e for e in emails if e != "contact@onekeymls.com"]

                email = filtered_emails[0] if filtered_emails else ""
                if len(filtered_emails) > 2:
                    email = ",".join(map(str, filtered_emails))

                data.update(
                    {
                        "z_onekey_url": url,
                        "z_onekey_title": title,
                        "z_onekey_email": email,
                        "z_onekey_keyword_count": keywordCountLinkedin,
                        "z_onekey_keyword_match": keywordMatch,
                        "z_onekey_match": match_percentage,
                        "z_onekey_match_name": match_percentage_name,
                        "z_onekey_description": description,
                    }
                )
                driver.back()
        
            if "samaki.com/profile" in url and data["z_samaki_profile"] == "":
                driver.get(url)
                licenceN = driver.find_element(By.XPATH, "//div[@id='userInfoFlexBox']//div[2]//h5[1]").text
                license_number = re.search(r'\d+', licenceN).group()
                email = ""
                phone = ""
                try:
                    WebDriverWait(driver, 3).until(
                        EC.presence_of_element_located(
                            (By.XPATH, ".//a[starts-with(@href, 'mailto:')]")
                        )
                    )
                    email = driver.find_element(
                        By.XPATH, ".//a[starts-with(@href, 'mailto:')]"
                    ).text
                    phone = driver.find_element(
                        By.XPATH, ".//span[@class='text-nowrap num']"
                    ).text
                except Exception:
                    pass
                licence_status = "Not Match"
                if license_number == licence:
                    licence_status = "Match"
                data.update(
                    {
                        "Z_samaki_profile": url,
                        "Z_match_percentage_samaki_full": match_percentage,
                        "Z_match_percentage_samaki_name": match_percentage_name,
                        "Z_samaki_title": title,
                        "Z_samaki_licence": license_number,
                        "Z_samaki_licence_status": licence_status,
                        "Z_samaki_phone": phone,
                        "Z_samaki_email": email,
                    }
                )

    except Exception as e:
        logging.error(f"Error processing keyword {keyword}: No Result")

    return data
def get_search_results_samaki(encoded_keyword, keywordWithHyphen, licence):
    keyword = urllib.parse.quote_plus(encoded_keyword)
    """Search Google for a keyword and return the first valid LinkedIn profile link."""
    data = {
        "s_samaki_profile": "",
        "s_match_percentage_samaki_full": "",
        "s_match_percentage_samaki_name": "",
        "s_samaki_title": "",
        "s_samaki_licence": "",
        "s_samaki_licence_status": "",
        "s_samaki_phone": "",
        "s_samaki_email": "",
        "s_zillow_title": "",
        "s_zillow_profile": "",
        "s_zillow_path": "",
        "s_zillow_percentage_full": "",
        "s_zillow_percentage_name": "",
        "s_zillow_location": "",
        "s_zillow_description": "",
        "s_street_url": "",
        "s_street_title": "",
        "s_street_match": "",
        "s_street_match_name": "",
        "s_onekey_url": "",
        "s_onekey_title": "",
        "s_onekey_email": "",
        "s_onekey_keyword_count": "",
        "s_onekey_keyword_match": "",
        "s_onekey_match": "",
        "s_onekey_match_name": "",
        "s_onekey_description": "",
        "s_samaki_profile": "",
        "s_match_percentage_samaki_full": "",
        "s_match_percentage_samaki_name": "",
    }

    try:
        driver.get(f"https://www.google.com/search?q={keyword}")

        soup = BeautifulSoup(driver.page_source, "html.parser")
        count = 1

        while detect_recaptcha(soup):
            captchaSolve(count, encoded_keyword)
            soup = BeautifulSoup(driver.page_source, "html.parser")
            count += 1

        # try:
        #     WebDriverWait(driver, 3).until(
        #         EC.presence_of_element_located((By.XPATH, '//a[@jsname="UWckNb"]'))
        #     )
        # except:
        #     pass

        results = driver.find_elements(By.XPATH, '//div[@jscontroller="SC7lYd"]')
        if not results:
            logging.warning("No results found. Check XPath or page loading issues.")
            return data

        def preprocess(text):
            """Preprocess text for keyword matching."""
            cleaned_text = re.sub(r"[^a-zA-Z\s]", "", text)
            return set(cleaned_text.lower().split())

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
            location = ""
            if "new york" in description.lower():
                location = "New York"
            elif "ny" in description.lower():
                location = "NY"
            keywordCountLinkedin = 0
            keywordMatch = ""
            for keywordA in keywordArray:
                if keywordA in description.lower():
                    keywordCountLinkedin += 1
                    keywordMatch += f"{keywordA}, "

            keywords1 = preprocess(title)
            keywords2 = preprocess(keywordWithHyphen)
            keywords1_name = preprocess(title.partition(" - ")[0].strip())
            keywords2_name = preprocess(keywordWithHyphen.partition(" - ")[0].strip())
            matching_keywords = [kw for kw in keywords2 if kw in keywords1]
            match_percentage = (
                f"{round((len(matching_keywords) / len(keywords2)) * 100, 2)}%"
            )
            matching_keywords_name = [
                kw for kw in keywords2_name if kw in keywords1_name
            ]
            match_percentage_name = f"{round((len(matching_keywords_name) / len(keywords2_name)) * 100, 2)}%"

            if "samaki.com/profile" in url and data["s_samaki_profile"] == "":
                driver.get(url)
                licenceN = driver.find_element(By.XPATH, "//div[@id='userInfoFlexBox']//div[2]//h5[1]").text
                license_number = re.search(r'\d+', licenceN).group()
                email = ""
                phone = ""
                try:
                    WebDriverWait(driver, 3).until(
                        EC.presence_of_element_located(
                            (By.XPATH, ".//a[starts-with(@href, 'mailto:')]")
                        )
                    )
                    email = driver.find_element(
                        By.XPATH, ".//a[starts-with(@href, 'mailto:')]"
                    ).text
                    phone = driver.find_element(
                        By.XPATH, ".//span[@class='text-nowrap num']"
                    ).text
                except Exception:
                    pass
                licence_status = "Not Match"
                if str(license_number) == str(licence):
                    licence_status = "Match"
                data.update(
                    {
                        "s_samaki_profile": url,
                        "s_match_percentage_samaki_full": match_percentage,
                        "s_match_percentage_samaki_name": match_percentage_name,
                        "s_samaki_title": title,
                        "s_samaki_licence": license_number,
                        "s_samaki_licence_status": licence_status,
                        "s_samaki_phone": phone,
                        "s_samaki_email": email,
                    }
                )
                
            if "zillow.com/profile" in url and data["s_zillow_profile"] == "":
                zillowPath = result.find_element(
                    By.XPATH, './/div[@class="byrV5b"]'
                ).text
                data.update(
                    {
                        "z_zillow_title": title,
                        "z_zillow_profile": url,
                        "z_zillow_path": zillowPath,
                        "z_zillow_percentage_full": match_percentage,
                        "z_zillow_percentage_name": match_percentage_name,
                        "z_zillow_location": location,
                        "z_zillow_description": description,
                    }
                )
                
            if "streeteasy.com/profile" in url and data["s_street_url"] == "":
                keywords2 = preprocess(keywordWithHyphen)
                keywords2_name = preprocess(keywordWithHyphen.partition(" Bio, ")[0].strip())
                matching_keywords_name = [
                    kw for kw in keywords2_name if kw in keywords1_name
                ]
                match_percentage_name = f"{round((len(matching_keywords_name) / len(keywords2_name)) * 100, 2)}%"
                    
                data.update(
                    {
                        "s_street_url": url,
                        "s_street_title": title,
                        "s_street_match": match_percentage,
                        "s_street_match_name": match_percentage_name,
                    }
                )
                
            if "onekeymls.com/realtor/agents" in url and data["s_onekey_url"] == "":
                driver.get(url)
                soup = BeautifulSoup(driver.page_source, "html.parser")

                scripts = soup.find_all("script")  

                emails = []
                for script in scripts:
                    found_emails = re.findall(email_pattern, script.text)
                    emails.extend(found_emails)

                filtered_emails = [e for e in emails if e != "contact@onekeymls.com"]

                email = filtered_emails[0] if filtered_emails else ""
                if len(filtered_emails) > 2:
                    email = ",".join(map(str, filtered_emails))

                data.update(
                    {
                        "s_onekey_url": url,
                        "s_onekey_title": title,
                        "s_onekey_email": email,
                        "s_onekey_keyword_count": keywordCountLinkedin,
                        "s_onekey_keyword_match": keywordMatch,
                        "s_onekey_match": match_percentage,
                        "s_onekey_match_name": match_percentage_name,
                        "s_onekey_description": description,
                    }
                )
                driver.back()

    except Exception as e:
        logging.error(f"Error processing keyword {keyword}: No Result")

    return data


searched_indices = []  # To store processed rows' indices

def process_keywords(input_file, output_file):
    """Process keywords and save LinkedIn profile URLs to an output file."""
    try:
        keywords_df = pd.read_excel(input_file)
        # if "Search" not in keywords_df.columns:
        #     raise ValueError("Input Excel must have a 'Search' column")

        results = []
        for count, (index, row) in enumerate(keywords_df.iterrows()):
            # if count >= 20:  # Limit to 5 iterations for testing
            #     break

            keyword = f"{row["First"]} {row['Last']}+{row["Business Name"]}"
            keywordWithHyphen = f"{row["First"]} {row['Last']} - {row["Business Name"]}"
            logging.info(f"Processing keyword ({count}): {keyword}")
            url_data = get_search_results(keyword, keywordWithHyphen, row["License Number"])
            keyword = f'{row["First"]} {row['Last']} - {row["Business Name"]} zillow'
            url_data2 = get_search_results_zillow(keyword, keywordWithHyphen)
            keyword = f'{row["First"]} {row['Last']} - {row["Business Name"]} samaki'
            url_data3 = get_search_results_samaki(keyword, keywordWithHyphen, row["License Number"])
            time.sleep(0.5)
            searched_indices.append(index)  # Store processed row index
            
            results.append({**row.to_dict(), **url_data, **url_data2, **url_data3})
            if count % 50 == 0:
                results_df = pd.DataFrame(results)
                current_time = datetime.now()  # Get current date and time
                formatted_time = current_time.strftime("%Y-%m-%d_%H-%M-%S")
                results_df.to_excel(f"output-{formatted_time}-{count}.xlsx", index=False, engine="openpyxl")
                logging.info(f"Results saved to output-{formatted_time}-{count}.xlsx")

    except Exception as e:
        logging.error(f"Error processing keywords: {e}")

    finally:
        # Save remaining unprocessed rows with timestamp
        
        current_time = datetime.now()  # Get current date and time
        formatted_time = current_time.strftime("%Y-%m-%d_%H-%M-%S")
        
        results_df = pd.DataFrame(results)
        results_df.to_excel(f"output-final-{formatted_time}.xlsx", index=False, engine="openpyxl")
        logging.info(f"Results saved to output-final-{formatted_time}.xlsx")
        driver.quit()


# Example usage
input_excel = "input.xlsx"  # Input file with keywords
output_excel = "output.xlsx"  # Output file to save URLs
process_keywords(input_excel, output_excel)

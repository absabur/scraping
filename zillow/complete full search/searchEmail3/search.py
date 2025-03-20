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

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# Initialize WebDriver with debugging options
options = webdriver.ChromeOptions()
options.debugger_address = "127.0.0.1:9224"
driver = webdriver.Chrome(options=options)

# "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9224 --user-data-dir="C:\Users\absab\AppData\Local\Google\Chrome\User Data\Profile 32"
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


def get_search_results(encoded_keyword, keywordWithHyphen):
    keyword = urllib.parse.quote(encoded_keyword)
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
        "zillow_profile_new": "",
        "zillow_path": "",
        "zillow_percentage_full": "",
        "zillow_percentage_name": "",
        "zillow_location": "",
        "zillow_description": "",
        "nystatemls_title": "",
        "nystatemls_profile": "",
        "nystatemls_percentage_name": "",
        "nystatemls_keyword_count": "",
        "nystatemls_keyword_match": "",
        "nystatemls_location": "",
        "nystatemls_description": "",
        "compass_listing": "",
        "compass_keyword_count": "",
        "compass_keyword_match": "",
        "compass_description": "",
        "facebook_title": "",
        "facebook_profile": "",
        "facebook_percentage_full": "",
        "facebook_percentage_name": "",
        "facebook_keyword_count": "",
        "facebook_keyword_match": "",
        "facebook_location": "",
        "facebook_description": "",
        "at_the_rate_title": "",
        "at_the_rate_url": "",
        "at_the_rate_description": "",
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

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//a[@jsname="UWckNb"]'))
        )

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
                data[f"email-{countEmail}"] = emails[0]
                data[f"email-{countEmail}-url"] = url
                data[f"email-{countEmail}-title"] = title
                data[f"email-{countEmail}-description"] = description
                data[f"email-{countEmail}-location"] = location
                data[f"email-{countEmail}-keyword-count"] = keywordCountLinkedin
                data[f"email-{countEmail}-keyword-match"] = keywordMatch
                countEmail += 1
            elif "instagram.com" not in url:
                if "@" in description:
                    data.update(
                        {
                            "at_the_rate_title": title,
                            "at_the_rate_url": url,
                            "at_the_rate_description": description,
                        }
                    )

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
                        "zillow_profile_new": url,
                        "zillow_path": zillowPath,
                        "zillow_percentage_full": match_percentage,
                        "zillow_percentage_name": match_percentage_name,
                        "zillow_location": location,
                        "zillow_description": description,
                    }
                )

            if "nystatemls.com/profiles/ny" in url and data["nystatemls_title"] == "":
                data.update(
                    {
                        "nystatemls_title": title,
                        "nystatemls_profile": url,
                        "nystatemls_percentage_name": match_percentage_name,
                        "nystatemls_keyword_count": keywordCountLinkedin,
                        "nystatemls_keyword_match": keywordMatch,
                        "nystatemls_location": location,
                        "nystatemls_description": description,
                    }
                )
            if "compass.com/listing" in url and data["compass_listing"] == "":
                data.update(
                    {
                        "compass_listing": url,
                        "compass_keyword_count": keywordCountLinkedin,
                        "compass_keyword_match": keywordMatch,
                        "compass_description": description,
                    }
                )

            if "facebook.com" in url and data["facebook_title"] == "":
                data.update(
                    {
                        "facebook_title": title,
                        "facebook_profile": url,
                        "facebook_percentage_full": match_percentage,
                        "facebook_percentage_name": match_percentage_name,
                        "facebook_keyword_count": keywordCountLinkedin,
                        "facebook_keyword_match": keywordMatch,
                        "facebook_location": location,
                        "facebook_description": description,
                    }
                )

            if "samaki.com/profile" in url:
                driver.get(url)
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
                data.update(
                    {
                        "samaki_profile": url,
                        "match_percentage_samaki_full": match_percentage,
                        "match_percentage_samaki_name": match_percentage_name,
                        "samaki_title": title,
                        "samaki_phone": phone,
                        "samaki_email": email,
                    }
                )
            
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

            keyword = f"{row["First"]} {row['Last']}+{row["COMPANY"]}"
            keywordWithHyphen = f"{row["First"]} {row['Last']} - {row["COMPANY"]}"
            logging.info(f"Processing keyword ({count}): {keyword}")
            url_data = get_search_results(keyword, keywordWithHyphen)
            results.append({**row.to_dict(), **url_data})

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

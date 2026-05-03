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
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# Initialize WebDriver with debugging options
options = webdriver.ChromeOptions()
options.debugger_address = "127.0.0.1:9210"
driver = webdriver.Chrome(options=options)

# "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9210 --user-data-dir="C:\Users\absab\AppData\Local\Google\Chrome\User Data\Profile 1"
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


def get_first_linkedin_profile(
    keyword, matchKeyword="", matchKeyword2="", matchKeyword3=""
):
    """Search Google for a keyword and return the first valid LinkedIn profile link."""
    data = {
        "linkedin_name": "",
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
            if count % 7 == 0:
                time.sleep(100)
            if count >= 2:
                driver.get(f"https://www.google.com/search?q={keyword}")
                soup = BeautifulSoup(driver.page_source, "html.parser")
                # pyautogui.click(1373, 10)
                time.sleep(1)

            time.sleep(0.5)
            pyautogui.click(55, 194)
            time.sleep(1)
            pyautogui.click(205, 347)
            time.sleep(5)
            count += 1

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//a[@jsname="UWckNb"]'))
        )

        results = driver.find_elements(By.XPATH, '//a[@jsname="UWckNb"]')
        if not results:
            logging.warning("No results found. Check XPath or page loading issues.")
            return data

        def preprocess(text):
            """Preprocess text for keyword matching."""
            cleaned_text = re.sub(r"[^a-zA-Z\s]", "", text)
            return set(cleaned_text.lower().split())

        for result in results:
            url = result.get_attribute("href")
            if not url:
                continue

            if "linkedin.com/in/" in url:
                title = result.find_element(By.XPATH, ".//h3").text
                title_words = set(preprocess(title))

                # Three match keyword sets
                keywords_list = [
                    ("match_linkedin_full", preprocess(keyword)),
                    ("match_linkedin_name", preprocess(matchKeyword)),
                    ("match_linkedin_title", preprocess(matchKeyword2)),
                    ("match_linkedin_company", preprocess(matchKeyword3)),
                ]

                # Initialize result dictionary
                result_data = {}

                # Loop through all 3 keyword sets and calculate match %
                for col_name, keyword_set in keywords_list:
                    if len(keyword_set) == 0:
                        percent = "0%"
                    else:
                        matched = sum(1 for kw in keyword_set if kw in title_words)
                        percent = f"{round((matched / len(keyword_set)) * 100, 2)}%"
                    result_data[col_name] = percent

                # Update data with final info
                data.update(
                    {
                        "linkedin_title": title,
                        "linkedinProfile": url,
                        "linkedin_name": title.split("-")[0].strip(),
                        **result_data,  # Unpack all 3 match percentages
                    }
                )
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


def process_keywords(input_file, output_file):
    """Process keywords and save LinkedIn profile URLs to an output file."""
    try:
        keywords_df = pd.read_excel(input_file)
        # if "Search" not in keywords_df.columns:
        #     raise ValueError("Input Excel must have a 'Search' column")

        results = []
        for count, (_, row) in enumerate(keywords_df.iterrows()):
            # if count >= 30:  # Limit to 5 iterations for testing
            #     break
            if count % 15 == 0:  # Limit to 5 iterations for testing
                time.sleep(15)

            # if row["Company Name"] == "":
            #     continue

            keyword = f"{row["Clean Name"]} - {row["Company+Title"]}"
            logging.info(f"Processing keyword ({count}): {keyword}")
            url_data = get_first_linkedin_profile(
                keyword, row["Clean Name"], "", row["Company+Title"]
            )
            
            # keyword = f"{row["full-name"]} - {row["position"]} - {row["company-name"]}"
            # logging.info(f"Processing keyword ({count}): {keyword}")
            # url_data = get_first_linkedin_profile(
            #     keyword, row["full-name"], row["position"], row["company-name"]
            # )
            results.append({**row.to_dict(), **url_data})
            time.sleep(1.3)

            if count % 50 == 0:
                results_df = pd.DataFrame(results)
                results_df.to_excel(
                    f"backup-{count}.xlsx", index=False, engine="openpyxl"
                )
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
input_excel = "input.xlsx"  # Input file with keywords
output_excel = "final.xlsx"  # Output file to save URLs
process_keywords(input_excel, output_excel)
# print(pyautogui.position())

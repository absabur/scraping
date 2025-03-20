from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import time
import pyautogui
import logging
import datetime
import urllib.parse

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


def detect_recaptcha(soup):
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


def get_first_linkedin_profile(keyword):
    encoded_keyword = urllib.parse.quote(keyword)
    print(keyword)
    """Search Google for a keyword and return the first valid LinkedIn profile link."""
    data = {
        "email": "",
        "source": "",
        "exit": False
    }

    try:
        driver.get(f"https://www.google.com/search?q={encoded_keyword}")

        # soup = BeautifulSoup(driver.page_source, "html.parser")
        # count = 1

        # while detect_recaptcha(soup):
        #     print("CAPTCHA detected. Please solve it manually.")
        #     if count >= 3:
        #         pyautogui.click(1373, 10)
        #         time.sleep(1)

        #     time.sleep(0.5)
        #     pyautogui.click(1337, 142)
        #     time.sleep(1)
        #     pyautogui.click(1480, 301)
        #     time.sleep(5)
        #     soup = BeautifulSoup(driver.page_source, "html.parser")
        #     count += 1

        inputEmail = input("Enter Email: ")
        inputSource = ""
        
        if inputEmail == "exit":
            exit = True
        else:
            inputSource = input("Enter Source: ")
            exit = False
            
        data.update(
            {
                "email": inputEmail,
                "source": inputSource,
                "exit": exit,
            }
        )
        return data

    except Exception as e:
        print("Somthing Wrong file Saved.")
        data.update(
            {
                "email": "",
                "source": "",
                "exit": True,
            }
        )
        return data


def process_keywords(input_file):
    """Process keywords and exit LinkedIn profile URLs to an output file."""
    try:
        keywords_df = pd.read_excel(input_file)
        results = []
        searched_indices = []  # To store processed rows' indices
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")  # Generate timestamp

        for count, (index, row) in enumerate(keywords_df.iterrows()):
            row = row.fillna("")  # Replace NaN with empty strings
            keyword = f"{row['First']} {row['Middle']} {row['Last']} + {row['COMPANY']}".strip()
            
            print("==========================================================\n")
            print(f"Processing keyword ({count}): {keyword}")

            url_data = get_first_linkedin_profile(keyword)

            if url_data['exit']:
                break
            
            results.append({**row.to_dict(), **url_data})
            searched_indices.append(index)  # Store processed row index

            if count % 50 == 0 and count != 0:
                results_df1 = pd.DataFrame(results)
                results_df1.to_excel(
                    f"manual-search-{count}-({timestamp}).xlsx", index=False, engine="openpyxl"
                )


        # Save processed results with timestamp
        results_df = pd.DataFrame(results)
        results_df.to_excel(f"manual-search-{count}-({timestamp}).xlsx", index=False, engine="openpyxl")

        # Save remaining unprocessed rows with timestamp
        remaining_df = keywords_df.drop(searched_indices)
        remaining_df.to_excel(f"input.xlsx", index=False, engine="openpyxl")
        print(f"Remaining unsearched data saved in 'input.xlsx'.")

    except Exception as e:
        logging.error(f"Error processing keywords: {e}")
        results_df.to_excel(f"manual-search-final-({timestamp}).xlsx", index=False, engine="openpyxl")

    finally:
        driver.quit()


input_excel = "input.xlsx"
process_keywords(input_excel)
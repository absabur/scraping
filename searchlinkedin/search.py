from selenium import webdriver
options = webdriver.ChromeOptions()
options.debugger_address = "127.0.0.1:9222"
driver = webdriver.Chrome(options=options)
from selenium.webdriver.common.by import By
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import math
import time

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


def get_first_linkedin_profile(driver, keyword):
    """Search Google for a keyword and return the first valid LinkedIn profile link."""
    try:
        driver.get(f"https://www.google.com/search?q={keyword}")

        soup = BeautifulSoup(driver.page_source, "html.parser")
        if detect_recaptcha(soup):
            print("CAPTCHA detected. Please solve it manually.")
            input("Press Enter to continue after solving the CAPTCHA...")

        # Find all search result links
        results = driver.find_elements(By.XPATH, "//a")
        print(len(results))

        if not results:
            print("No results found. Check XPath or page loading issues.")
            return "No LinkedIn profile found"

        # Check each link to see if it is a valid LinkedIn profile
        for result in results:
            url = result.get_attribute("href")
            if url:
                if "linkedin.com/posts/" in url:
                    print(f"Valid LinkedIn profile found: {url}")
                    return url
        return (
            "No LinkedIn profile found"  # No valid LinkedIn profile in search results
        )
    except Exception as e:
        return f"Error: {e}"


def process_keywords(input_file, output_file):
    """Process keywords and save LinkedIn profile URLs to an output file."""

    keywords_df = pd.read_excel(input_file)

    # Ensure the file has the required columns
    if "name" not in keywords_df.columns or "title" not in keywords_df.columns:
        raise ValueError("Input Excel must have 'name' and 'title' columns")

    # Initialize WebDriver

    # List to store results
    results = []

    try:
        count = 0
        for _, row in keywords_df.iterrows():
            # if count >= 50:  # Stop processing after reaching the limit
            #     break
            name = row["name"]
            title = row["title"]
            image = row["image"]

            # Skip rows with missing values
            if pd.isna(name) or pd.isna(title):
                continue

            keyword = f"{name} {title}"
            print(f"Processing keyword: {keyword}")
            url = get_first_linkedin_profile(driver, keyword)
            if url == "end":
                break
            results.append({"name": name, "title": title, "LinkedIn URL": url, "image": image})
            count += 1

        # Create a DataFrame for the results
        results_df = pd.DataFrame(results)

        # Write the results to a new Excel file
        results_df.to_excel(output_file, index=False, engine="openpyxl")
        print(f"Results saved to {output_file}")

    finally:
        # Close the browser
        driver.quit()

# Example usage
input_excel = "keywords.xlsx"  # Input file with keywords
output_excel = "linkedin_results.xlsx"  # Output file to save URLs
process_keywords(input_excel, output_excel)

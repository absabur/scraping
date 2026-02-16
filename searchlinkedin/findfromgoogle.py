from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import time
import logging
import urllib.parse
import pyautogui

# "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9210 --user-data-dir="C:\Users\absab\AppData\Local\Google\Chrome\User Data\Profile 1"
# %LOCALAPPDATA%
# chrome://version/
# https://chatgpt.com/c/dcbf62ec-e118-4299-a10c-4c182966cd8c

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize WebDriver
options = webdriver.ChromeOptions()
options.debugger_address = "127.0.0.1:9210"
driver = webdriver.Chrome(options=options)

def detect_recaptcha(soup):
    """Check if a reCAPTCHA is present on the page."""
    if (
        soup.find_all(class_="g-recaptcha")
        or soup.find_all("script", src=lambda src: src and "recaptcha" in src)
        or soup.find_all(class_="recaptcha-checkbox-border")
        or soup.find_all(class_="recaptcha")
    ):
        return True
    return False

def get_social_links(keyword, site_domain, total_pages=7):
    """Search Google for a keyword on a specific site across multiple pages."""
    results_list = []
    
    for page in range(total_pages):
        # Calculate start index: Page 1 = 0, Page 2 = 10, etc.
        start_index = page * 10
        search_query = f"site:{site_domain} {keyword}"
        encoded_keyword = urllib.parse.quote_plus(search_query)
        
        # Build URL with the start parameter
        url = f"https://www.google.com/search?q={encoded_keyword}&start={start_index}"
        
        try:
            logging.info(f"Searching {site_domain} | Page {page+1} | URL: {url}")
            driver.get(url)
            
            # Wait and perform a small scroll to trigger lazy-loaded items
            time.sleep(2)
            driver.execute_script("window.scrollTo(0, 500);")
            time.sleep(1)

            soup = BeautifulSoup(driver.page_source, "html.parser")
            
            count = 1
            # Solve CAPTCHA manually if it appears
            while detect_recaptcha(soup):
                print("CAPTCHA detected. Please solve it manually.")
                if count % 7 == 0:
                    time.sleep(100)
                if count >= 2:
                    driver.get(f"https://www.google.com/search?q={encoded_keyword}&start={start_index}")        
                    soup = BeautifulSoup(driver.page_source, "html.parser")
                    # pyautogui.click(1373, 10)
                    time.sleep(1)
                    
                time.sleep(0.5)
                pyautogui.click(51, 194)
                time.sleep(1)
                pyautogui.click(225, 655)
                time.sleep(5)
                count+=1

            # Find result links
            try:
                WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//a[@jsname="UWckNb"]')))
                search_results = driver.find_elements(By.XPATH, '//a[@jsname="UWckNb"]')
            except:
                logging.warning(f"No results found on page {page+1} for {keyword}")
                break # If no results found, stop paginating for this keyword

            for result in search_results:
                try:
                    url_found = result.get_attribute("href")
                    title = result.find_element(By.XPATH, './/h3').text
                    
                    if url_found and title:
                        results_list.append({
                            "Keyword": keyword,
                            "Platform": "YouTube" if "youtube.com" in site_domain else "Facebook",
                            "Title": title,
                            "URL": url_found,
                            "Page_Source": page + 1
                        })
                except Exception:
                    continue

            # Small random-like delay between pages to avoid being blocked
            time.sleep(1.5)

        except Exception as e:
            logging.error(f"Error on page {page+1} for {site_domain}: {e}")
            break # Exit page loop if there's a major error

    return results_list

def process_keywords(output_file):
    """Main loop to process keywords from the list across multiple pages."""
    try:
        final_data = []
        # Your specific keyword list
        keywords = [
            'ওসমান "হাদি" নির্বাচনী প্রচারণা',
            'Osman "Hadi" election campaign',
            'ওসমান "হাদি" সাক্ষাৎকার',
            'Interview with Osman "Hadi"',
            'ওসমান "হাদি" টক শো',
            'Osman "Hadi" talk show',
            'ওসমান "হাদি" সংবাদ সম্মেলন',
            'Osman "Hadi" press conference',
            'ওসমান "হাদি" বক্তৃতা',
            'Osman "Hadi" speech',
        ]

        for count, kw in enumerate(keywords):
            logging.info(f"--- STARTING SEARCH FOR: {kw} ---")
            
            # 1. Search YouTube (5 pages)
            yt_results = get_social_links(kw, "youtube.com", total_pages=7)
            final_data.extend(yt_results)
            time.sleep(3) # Anti-bot delay

            # 2. Search Facebook (5 pages)
            fb_results = get_social_links(kw, "facebook.com", total_pages=7)
            final_data.extend(fb_results)
            
            # Cooldown every few searches
            if (count + 1) % 3 == 0:
                logging.info("Taking a 10-second break to prevent detection...")
                time.sleep(10)

            # Intermediate save
            pd.DataFrame(final_data).to_excel(f"backup_results.xlsx", index=False)

        # Final Save
        df_output = pd.DataFrame(final_data)
        # Drop duplicates in case the same link appears on different pages
        df_output = df_output.drop_duplicates(subset=['URL'])
        df_output.to_excel(output_file, index=False)
        logging.info(f"Successfully saved {len(df_output)} unique links to {output_file}")

    except Exception as e:
        logging.error(f"Main Loop Error: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    output_excel = "social_search_results.xlsx"
    process_keywords(output_excel)
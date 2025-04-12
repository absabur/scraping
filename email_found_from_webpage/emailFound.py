from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException
import pandas as pd
import re
import logging
from selenium.common.exceptions import TimeoutException, WebDriverException

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Setup Selenium with Chrome DevTools attached
options = webdriver.ChromeOptions()
options.debugger_address = "127.0.0.1:9222"
driver = webdriver.Chrome(options=options)

# === Utility Functions ===

# "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="C:\Users\absab\AppData\Local\Google\Chrome\User Data\Profile 1"
# %LOCALAPPDATA%
# chrome://version/
# https://chatgpt.com/c/dcbf62ec-e118-4299-a10c-4c182966cd8c



def sanitize_url(url):
    pattern = re.compile(r'^(http[s]?://)?([\w\-]+\.)+[\w\-]+')
    if not isinstance(url, str):
        return None
    if not pattern.match(url):
        return None
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
    return url

def generate_possible_contact_urls(domain):
    domain = domain.rstrip('/')
    paths = ["/contact", "/contact-us", "/support", "/get-in-touch"]
    return [domain + path for path in paths]

def find_emails(url):
    try:
        driver.set_page_load_timeout(5)
        driver.get(url)
    except TimeoutException:
        logging.error(f"⏰ Timeout loading URL: {url}. Skipping...")
    except WebDriverException as e:
        logging.error(f"❌ WebDriver error with URL: {url}. Error: ")
    except Exception as e:
        logging.error(f"❌ Unexpected error with URL: {url}. Error: ")

    found_emails = set()

    # 1. mailto: links
    try:
        mailto_links = driver.find_elements(By.XPATH, "//a[starts-with(@href, 'mailto:')]")
        for link in mailto_links:
            try:
                email = link.get_attribute("href").replace("mailto:", "").split("?")[0]
                found_emails.add(email)
            except Exception: continue
        if found_emails:
            logging.info("✅ Found emails using mailto: links.")
            return list(found_emails)
    except Exception as e:
        logging.warning(f"⚠️ Error reading mailto links")

    # 2. visible text scan
    try:
        for elem in driver.find_elements(By.XPATH, "//*"):
            try:
                text = elem.text
                if "@" in text:
                    matches = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text)
                    found_emails.update(matches)
                    if found_emails:
                        logging.info("✅ Found emails in visible text.")
                        return list(found_emails)
            except StaleElementReferenceException:
                continue
            except Exception:
                continue
    except Exception as e:
        logging.warning(f"⚠️ Error scanning visible text")

    # 3. page source regex
    try:
        page_source = driver.page_source
        emails_in_source = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', page_source)
        if emails_in_source:
            found_emails.update(emails_in_source)
            logging.info("✅ Found emails in page source.")
            return list(found_emails)
    except Exception as e:
        logging.warning(f"⚠️ Error scanning page source")

    # 4. script/meta fallback
    try:
        for tag in driver.find_elements(By.XPATH, "//script | //meta"):
            try:
                content = tag.get_attribute("innerHTML") or tag.get_attribute("content")
                if content and "@" in content:
                    matches = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', content)
                    found_emails.update(matches)
                    if found_emails:
                        logging.info("✅ Found emails in script/meta tags.")
                        return list(found_emails)
            except Exception:
                continue
    except Exception as e:
        logging.warning(f"⚠️ Error in script/meta parsing")

    logging.warning("⚠️ No emails found by any method.")
    return []

def find_facebook_url(url):
    facebook_urls = []

    try:
        driver.set_page_load_timeout(5)
        driver.get(url)
        logging.info(f"🔍 Opened URL for Facebook search: {url}")
        
        all_links = driver.find_elements(By.TAG_NAME, 'a')

        for link in all_links:
            href = link.get_attribute("href")
            if href and "facebook.com" in href.lower():
                facebook_urls.append(href)

        if facebook_urls:
            logging.info(f"✅ Found Facebook URLs: {facebook_urls}")
        else:
            logging.warning("⚠️ No Facebook URLs found.")

    except TimeoutException:
        logging.error(f"⏰ Timeout loading URL: {url}. Skipping...")
    except WebDriverException as e:
        logging.error(f"❌ WebDriver error with URL: {url}. Error: ")
    except Exception as e:
        logging.error(f"❌ Unexpected error with URL: {url}. Error: ")

    return facebook_urls


# === Main Process ===

def process_keywords(input_file):
    try:
        df = pd.read_excel(input_file)
        results = []

        for count, (_, row) in enumerate(df.iterrows()):
            try:
                raw_url = row.get("Domain")
                if pd.isna(raw_url) or not isinstance(raw_url, str) or raw_url.strip() == "":
                    logging.warning(f"⚠️ Skipping empty or invalid URL at row {count}: {raw_url}")
                    continue

                url = sanitize_url(raw_url.strip())
                if not url:
                    logging.warning(f"⚠️ Skipping unfixable URL format at row {count}: {raw_url}")
                    continue

                emails = find_emails(url)

                # Try contact page column
                if not emails:
                    raw_contact_url = row.get("Contact page")
                    if isinstance(raw_contact_url, str) and raw_contact_url.strip():
                        contact_url = sanitize_url(raw_contact_url.strip())
                        if contact_url:
                            emails = find_emails(contact_url)

                # Try guessing contact URLs
                # if not emails:
                #     for guess_url in generate_possible_contact_urls(url):
                #         emails = find_emails(guess_url)
                #         if emails:
                #             url = guess_url  # track actual source
                #             break

                facebook_urls = find_facebook_url(url)

                result_row = row.to_dict()
                result_row["Emails"] = ", ".join(emails) if emails else ""
                result_row["Used URL"] = url
                result_row["Facebook URLs"] = ", ".join(facebook_urls) if facebook_urls else ""
                results.append(result_row)

                logging.info(f"{count+1}: {url} => Emails: {emails}, Facebook: {facebook_urls}")

                # Auto save every 50 rows
                if count % 50 == 0 and count > 0:
                    pd.DataFrame(results).to_excel(f"output-emails-{count}.xlsx", index=False, engine="openpyxl")

            except Exception as row_error:
                logging.error(f"❌ Error processing row {count}: {row_error}")
                continue

        # Final write
        pd.DataFrame(results).to_excel("output-emails-final.xlsx", index=False, engine="openpyxl")

    except Exception as e:
        logging.error(f"❌ Error in process_keywords")
    finally:
        try:
            pd.DataFrame(results).to_excel("output-emails-final.xlsx", index=False, engine="openpyxl")
            driver.quit()
            logging.info("✅ Driver closed successfully.")
        except:
            pass

# === Run ===
if __name__ == "__main__":
    try:
        input_excel = "input.xlsx"
        process_keywords(input_excel)
    except Exception as e:
        logging.error(f"❌ Script failed")

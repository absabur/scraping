from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import re, time, pyautogui
from fuzzywuzzy import process
import pandas as pd

# Function to get website using Selenium

def captchaSolve(count, encoded_keyword):
    print("CAPTCHA detected. Please solve it manually.")
    if count % 7 == 0:
        time.sleep(100)
    if count >= 2:
        driver.get(f"https://www.google.com/search?q={encoded_keyword}")        
        # pyautogui.click(1373, 10)
        time.sleep(1)

    time.sleep(0.5)
    pyautogui.click(51, 194)
    time.sleep(1)
    pyautogui.click(253, 651)
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

def get_website(company_name, driver):
    query = f"{company_name}"
    try:
        driver.get(f'https://www.google.com/search?q={query}')
        # WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'h3')))
        soup = BeautifulSoup(driver.page_source, "html.parser")
        count = 1

        while detect_recaptcha(soup):
            captchaSolve(count, query)
            soup = BeautifulSoup(driver.page_source, "html.parser")
            count += 1

        url = ""
        matchpercent = ""
        phone = ""
        address = ""
        
        try:
            phone_element = driver.find_element(By.XPATH, '//span[contains(@aria-label, "Call phone number")]')
            phone = phone_element.text
        except:
            pass
        try:
            address_element = driver.find_element(By.XPATH, '//span[@class="LrzXr"]')
            address = address_element.text
        except:
            pass

        try:
            url_elem = soup.find_all('a', class_='ab_button')
            for url in url_elem:
                if url.text == "Website" or url.text == "ওয়েবসাইট":
                    url = url.get('href')
                    matchpercent = "From map"
                    return {"url": url, "match": matchpercent, "end": False, "address": address, "phone": phone}
            url_elem = soup.find_all('a', class_='n1obkb')
            for url in url_elem:
                if url.text == "Website" or url.text == "ওয়েবসাইট":
                    url = url.get('href')
                    matchpercent = "From - map"
                    return {"url": url, "match": matchpercent, "end": False, "address": address, "phone": phone}

            urls = soup.find_all('a', attrs={'jsname': 'UWckNb'})
            texts = [url.find('span', class_='VuuXrf').text for url in urls if url.find('span', class_='VuuXrf')]
            match = process.extractOne(company_name, texts, score_cutoff=70)
            if match:
                for url in urls:
                    if match[0] == url.find('span', class_='VuuXrf').text:
                        url = url.get('href')
                        matchpercent = match[1]
                        break
        except Exception as e:
            url = ""

        return {"url": url, "match": matchpercent, "end": False, "address": address, "phone": phone}
            
    except Exception as e:
        print(f"Error searching for {company_name}: {str(e)}")
    return {"end": True}


print("ready")
options = webdriver.ChromeOptions()
options.debugger_address = "127.0.0.1:9222"
driver = webdriver.Chrome(options=options)

# "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="C:\Users\absab\AppData\Local\Google\Chrome\User Data\Profile 2"
# %LOCALAPPDATA%
# chrome://version/
# https://chatgpt.com/c/dcbf62ec-e118-4299-a10c-4c182966cd8c

# Specify your Excel file path
excel_file_path = 'companies.xlsx'

# Read Excel file into a Pandas DataFrame
df = pd.read_excel(excel_file_path, engine='openpyxl')

# Convert DataFrame to a list of dictionaries
companies = df.to_dict(orient='records')

# Iterate over each company name in the Excel sheet
count = 1
for row in companies:
    # if count >= 20:
    #     break
    if count % 18 == 0:
        time.sleep(22)
    website = get_website(row['COMPANY name'], driver)
    time.sleep(1.5)
    if website['end']:
        break
    if website['url']:
        print(f"{count}) Website found for {row['COMPANY name']}\n")
        row['Website'] = website['url']
        row['match'] = website['match']
    if website['address']:
        row['address'] = website['address']
    if website['phone']:
        row['phone'] = website['phone']
    else:
        print(f"{count}) Website not found for {row['COMPANY name']}\n")
    count += 1

# Save the updated DataFrame to a new Excel file
df = pd.DataFrame(companies)
output_excel_path = 'output_companies_with_websites12.xlsx'
df.to_excel(output_excel_path, index=False)

# Close the WebDriver session
driver.quit()


print(f"Updated data saved to {output_excel_path}")

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import re
from fuzzywuzzy import process
import pandas as pd

# Function to get website using Selenium



def get_website(company_name, driver):
    query = f"{company_name}"
    try:
        driver.get(f'https://www.google.com/search?q="{query}"')
        # WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'h3')))
        soup = BeautifulSoup(driver.page_source, 'html.parser')


        # Check for common reCAPTCHA elements
        is_recaptcha_present = False

        # Check for v2 reCAPTCHA elements
        recaptcha_v2 = soup.find_all(class_='g-recaptcha')
        if recaptcha_v2:
            is_recaptcha_present = True

        # Check for v3 reCAPTCHA elements (usually involves an API script)
        recaptcha_v3 = soup.find_all('script', src=lambda src: src and 'recaptcha' in src)
        if recaptcha_v3:
            is_recaptcha_present = True

        # Check for the reCAPTCHA checkbox
        recaptcha_checkbox = soup.find_all(class_='recaptcha-checkbox-border')
        if recaptcha_checkbox:
            is_recaptcha_present = True

        # Check for other common reCAPTCHA elements
        recaptcha_elements = soup.find_all(class_='recaptcha')
        if recaptcha_elements:
            is_recaptcha_present = True

        val = ""
        if is_recaptcha_present:
            print("=================================================")
            val = input(f"Press Enter for next (e): ")

        if val  == "e":
            return {"end": True}

        url = ""
        matchpercent = ""

        # try:
        #     url = driver.find_element(By.XPATH, '//a[@class="ab_button" and text()="Website"]')
        # except:
        #     try:
        #         urls = driver.find_elements(By.XPATH, '//a[@jsname="UWckNb"]')
        #         texts = []
        #         for url in urls:
        #             try:
        #                 text = url.find_element(By.XPATH, './/span[@class="VuuXrf"]').text
        #                 texts.append(text)
        #             except:
        #                 continue
        #         match = process.extractOne(company_name, texts, score_cutoff=60)
        #         if match:
        #             for url in urls:
        #                 if match[0] in url.text:
        #                     url = url.get_attribute('href')
        #                     match = f"{match[1]}"
        #                     break
        #     except:
        #         url = ""


        try:
            url_elem = soup.find_all('a', class_='ab_button')
            for url in url_elem:
                if url.text == "Website" or url.text == "ওয়েবসাইট":
                    url = url.get('href')
                    matchpercent = "From map"
                    return {"url": url, "match": matchpercent, "end": False}
            url_elem = soup.find_all('a', class_='n1obkb')
            for url in url_elem:
                if url.text == "Website" or url.text == "ওয়েবসাইট":
                    url = url.get('href')
                    matchpercent = "From - map"
                    return {"url": url, "match": matchpercent, "end": False}

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

        return {"url": url, "match": matchpercent, "end": False}
            
    except Exception as e:
        print(f"Error searching for {company_name}: {str(e)}")
    return {"end": True}

# Initialize Selenium WebDriver (Chrome in this example)

# options = webdriver.ChromeOptions()
# options.debugger_address = "127.0.0.1:9222"
# driver = webdriver.Chrome(options=options)

driver = webdriver.Chrome()

# "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="C:\Users\absab\AppData\Local\Google\Chrome\User Data\Profile 1"

# Specify your Excel file path
excel_file_path = 'companies.xlsx'

# Read Excel file into a Pandas DataFrame
df = pd.read_excel(excel_file_path, engine='openpyxl')

# Convert DataFrame to a list of dictionaries
companies = df.to_dict(orient='records')

# Iterate over each company name in the Excel sheet
count = 1
for row in companies:
    website = get_website(row['company'], driver)
    if website['end']:
        break
    if website['url']:
        print(f"{count}) Website found for {row['company']}\n")
        row['Website'] = website['url']  # Assuming the website is in the second colum
        row['match'] = website['match']  # Assuming the website is in the second colum
    else:
        print(f"{count}) Website not found for {row['company']}\n")
    count += 1

# Save the updated DataFrame to a new Excel file
df = pd.DataFrame(companies)
output_excel_path = 'output_companies_with_websites12.xlsx'
df.to_excel(output_excel_path, index=False)

# Close the WebDriver session
driver.quit()


print(f"Updated data saved to {output_excel_path}")

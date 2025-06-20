from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import re, time, pyautogui
from fuzzywuzzy import process
import pandas as pd

# Function to get website using Selenium

def get_website(url, driver):
    try:
        driver.get(f'{url}')
        soup = BeautifulSoup(driver.page_source, "html.parser")

        data = {}
        data["url"] = url
        
        # Company name
        try:
            company_name = soup.find("h1", class_="exhibitor-name")
            if company_name:
                data["company_name"] = company_name.get_text(strip=True)
        except Exception as e:
            print("Company name extraction error:", e)

        # Company address
        try:
            company_address = soup.find("address", class_="address")
            if company_address:
                data["company_address"] = company_address.get_text(strip=True)
        except Exception as e:
            print("Company address extraction error:", e)

        # Emails from page + script
        try:
            page_text = soup.get_text()
            script_texts = " ".join(script.get_text() for script in soup.find_all("script"))
            full_text = page_text + " " + script_texts
            emails = re.findall(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', full_text)
            
            # Store each email in a separate key
            for idx, email in enumerate(emails, 1):
                data[f"email_{idx}"] = email
        except Exception as e:
            print("Email extraction error:", e)

        # Contact info (website and phone)
        try:
            contact_div = soup.find("div", class_="contact-info")
            if contact_div:
                list_items = contact_div.find_all("li")
                if len(list_items) >= 2:
                    data["website"] = list_items[0].get_text(strip=True)
                    data["phone"] = list_items[1].get_text(strip=True)
        except Exception as e:
            print("Contact info extraction error:", e)

        # LinkedIn company link
        try:
            linkedin_tag = soup.find("a", href=lambda href: href and href.startswith("https://www.linkedin.com/company"))
            if linkedin_tag:
                data["linkedin_company"] = linkedin_tag["href"]
        except Exception as e:
            print("LinkedIn (company) extraction error:", e)
            
            
        try:
            articles = soup.find_all("article", class_="card-v2")
            persons = []
            for article in articles:
                person_data = {}
                # LinkedIn person URL
                try:
                    linkedin_tag = article.find("a", href=lambda href: href and href.startswith("https://www.linkedin.com/"))
                    if linkedin_tag:
                        person_data["linkedin_person"] = linkedin_tag["href"]
                except Exception as e:
                    print("LinkedIn (person) extraction error:", e)

                # Person name
                try:
                    name_tag = article.find("p", class_="name")
                    if name_tag:
                        person_data["person_name"] = name_tag.get_text(strip=True)
                except Exception as e:
                    print("Name extraction error:", e)

                # Job title
                try:
                    title_tag = article.find("p", class_="job-title")
                    if title_tag:
                        person_data["job_title"] = title_tag.get_text(strip=True)
                except Exception as e:
                    print("Job title extraction error:", e)
                if person_data:
                    persons.append(person_data)
            data["persons"] = persons

        except Exception as e:
            print(f"Error processing articles: {e}")



        # Print final results
        # print(data)

        return data

    except Exception as e:
        print(f"Error searching for {url}: {str(e)}")


print("ready")
options = webdriver.ChromeOptions()
options.debugger_address = "127.0.0.1:9222"
driver = webdriver.Chrome(options=options)

# "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="C:\Users\absab\AppData\Local\Google\Chrome\User Data\Profile 2"
# %LOCALAPPDATA%
# chrome://version/
# https://chatgpt.com/c/dcbf62ec-e118-4299-a10c-4c182966cd8c

# Specify your Excel file path
excel_file_path = 'data.xlsx'

# Read Excel file into a Pandas DataFrame
df = pd.read_excel(excel_file_path, engine='openpyxl')

# Convert DataFrame to a list of dictionaries
companies = df.to_dict(orient='records')

# Iterate over each company name in the Excel sheet
count = 1
allData = []
for row in companies:
    # if count >= 15:
    #     break

    website = get_website(row['URLS'], driver)

    for person in website.get("persons", []):
        print(person)
        copy_website = website.copy()
        copy_website.pop("persons", None)
        copy_website.update(person)
        allData.append(copy_website)
    count += 1

# Save to Excel
df = pd.DataFrame(allData)
output_excel_path = 'lasvegas2025.xlsx'
df.to_excel(output_excel_path, index=False)

# Close the WebDriver session
driver.quit()


print(f"Updated data saved to {output_excel_path}")

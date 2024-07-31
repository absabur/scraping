from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.service import Service
service_obj=Service(r"c:\chromedriver.exe")
driver=webdriver.Chrome(service=service_obj)
# from selenium.webdriver.common.by import By
import time
import pandas as pd
import random

excel_file_path = 'person.xlsx'

df = pd.read_excel(excel_file_path)

employees = df.to_dict(orient='records')

linkedin_urls = []
count = 1

for employee in employees:
    queries = [
        f"{employee['Name']} Baseball {employee['Location']} linkedin",
    ]
    val = ""
    for query in queries:
        driver.get(f"https://www.google.com/search?q={query}")
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


        


        if is_recaptcha_present:
            print("=================================================")
            val = input(f"current: {count}, Press Enter for next, exit for stop: ")
        else:
            print(f"current: {count}.")

        if val  == "exit":
            break
        time.sleep(random.uniform(0.3, 0.7))
        try:
            a_tags = soup.find_all('a')
            
            for a_tag in a_tags:
                link = a_tag.get('href', '')
                if 'linkedin.com/in/' in link:
                    employee['LinkedInUrl'] = link
                    break

        except Exception as e:
            print(f"An error occurred: {e}")
        

    if val  == "exit":
        break

    count += 1


driver.quit()


df = pd.DataFrame(employees)

excel_file_path = f'output-linkedin.xlsx'

df.to_excel(excel_file_path, index=False)

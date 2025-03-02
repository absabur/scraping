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
import openpyxl
import time

# "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="C:\Users\absab\AppData\Local\Google\Chrome\User Data\Profile 1"
# %LOCALAPPDATA%
# chrome://version/
# https://chatgpt.com/c/dcbf62ec-e118-4299-a10c-4c182966cd8c


def scrape_current_page(driver, table_data):
    try:
        # Get the page source
        page_source = driver.page_source
        
        # Parse the page source with BeautifulSoup
        soup = BeautifulSoup(page_source, 'html.parser')
        
        # Locate the table body and rows
        tbody = soup.find('tbody')  # Finds the first <tbody> tag
        rows = tbody.find_all('tr') if tbody else []  # Finds all <tr> tags within <tbody>
        
        # Extract data from rows
        for row in rows:
            row_data = []
            cells = row.find_all('td')  # Finds all <td> tags within the row
            for cell in cells:
                # Extract text while handling <br> tags
                content_parts = [line.strip() for line in cell.decode_contents().split('<br>')]
                row_data.extend(content_parts)
            table_data.append(row_data)
    except Exception as e:
        print("Failed to scrape the page:", e)


# Open the target website
driver.get("https://saras.cbse.gov.in/saras/AffiliatedList/ListOfSchdirReport")

input("Wait for state selection and press Enter: ")

# Initialize storage for table data
table_data = []

# Locate the last <a> tag inside the pagination span
last_a_tag = driver.find_element(By.XPATH, '//div[@id="myTable_paginate"]//span//a[last()]')
last_page_number = int(last_a_tag.text)

# Iterate through pages and scrape data
for i in range(1, last_page_number):
    print(f"Scraping page {i}...")
    
    # Scrape data from the current page
    scrape_current_page(driver, table_data)

    next_button = driver.find_element(By.XPATH, f'//a[@data-dt-idx="{int(i)+1}"]')
    next_button.click()
    time.sleep(0.5)  # Add delay for page transition (adjust as needed)
    

print(f"Scraping page {last_page_number}...")
scrape_current_page(driver, table_data)

# Write scraped data to an Excel file
workbook = openpyxl.Workbook()
sheet = workbook.active
sheet.title = "Dynamic Data"

for i, row_data in enumerate(table_data, start=1):
    for j, value in enumerate(row_data, start=1):
        sheet.cell(row=i, column=j, value=value)

workbook.save("dynamic_output.xlsx")
print("Data saved to dynamic_output.xlsx")

# Close the WebDriver
driver.quit()
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
import json
import logging
from bs4 import BeautifulSoup
import json
import pandas as pd
from pandas import json_normalize

# Set up logging

# Service and Driver Setup
service_obj = Service(r"c:\chromedriver.exe")
driver = webdriver.Chrome(service=service_obj)

# Function to scrape data from a given URL
def scrap(url, driver,city,zip,county,type):
    object_data = dict()

    try:
        logging.info(f"Scraping URL: {url}")

        # Open the target URL
        driver.get(f"https://www.gastronaut.hr{url}")

        # Wait for the main content section to be present
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//section[@class="main-content"]'))
        )
        
        element = driver.find_element(By.XPATH, '//section[@class="main-content"]')

        
        object_data['url'] = f"https://www.gastronaut.hr{url}"
        object_data['city'] = city
        object_data['zip'] = zip
        object_data['county'] = county
        object_data['type'] = type

        # Wait for list items and scrape them
        lists = WebDriverWait(element, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, '//div[@class="details-left"]//li'))
        )
        
        init = 1
        for list_item in lists:
            keyValue = list_item.text.split(":")
            
            # If keyValue has more than one part (i.e., key-value pair)
            if len(keyValue) > 1:
                if keyValue[1]:
                    object_data[keyValue[0]] = keyValue[1]
                
                # Extract <a> tag's href if present
                try:
                    a_tag = list_item.find_element(By.XPATH, './/a')  # Relative XPath
                    if a_tag:
                        object_data[f"{keyValue[0]}-url"] = a_tag.get_attribute('href')
                except:
                    pass
                
                # Extract <img> tags' src attributes if present
                try:
                    img_tags = list_item.find_elements(By.XPATH, './/img')  # Relative XPath
                    if img_tags:
                        for idx, img in enumerate(img_tags, start=1):
                            object_data[f"{keyValue[0]}-pay-{idx}"] = img.get_attribute('alt')
                except:
                    pass
            
            # If keyValue has only one part (i.e., just a value in the list item)
            elif len(keyValue) == 1:
                if list_item.text:
                    object_data[f'column-{init}'] = list_item.text
                
                # Extract <a> tags' href if present
                try:
                    a_tags = list_item.find_elements(By.XPATH, './/a')  # Relative XPath
                    if a_tags:
                        for idx, a in enumerate(a_tags, start=1):
                            object_data[f'column-{init}-link-{idx}'] = a.get_attribute('href')

                except:
                    pass
                
                # Increment column counter for the next item
                init += 1

        logging.info(f"Successfully scraped data from {url}")
    
    except Exception as e:
        logging.error(f"Error scraping {url}: {e}")
    
    return object_data

# Main function to read URLs from JSON and scrape datadef main():
def main():
    try:
        with open('data.json', 'r', encoding='utf-8') as file:
            json_data = json.load(file)

        initial = 1
        scraped_data = []

        # Loop through the JSON data
        for item in json_data:
            # if initial == 4:  # Stop after scraping the first 3 URLs
            #     break

            # Safely access nested dictionary values using get() method
            url = item.get('get_absolute_url')
            city = item.get('city', {}).get('name', "")  # Safely access 'name' key in 'city'
            zip_code = item.get('city', {}).get('zip', "")  # Safely access 'zip' key in 'city'
            county = item.get('city', {}).get('county', "")  # Safely access 'county' key in 'city'
            type_ = item.get('type', {}).get('name', "")  # Renamed 'type' to 'type_' to avoid conflict with Python keyword

            if url:
                data = scrap(url, driver, city, zip_code, county, type_)
                scraped_data.append(data)

            initial += 1  # Increment the counter
        
        with open('all-datas.json', "w") as json_file:
            json.dump(scraped_data, json_file, indent=4)

    except FileNotFoundError:
        logging.error("Error: data.json file not found.")
    except json.JSONDecodeError:
        logging.error("Error: Invalid JSON format.")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
    finally:
        driver.quit()

# Run the script
if __name__ == "__main__":
    main()




with open('all-datas.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Normalize JSON data (this works well with nested structures)
df = json_normalize(data)

# Save the dataframe to an Excel file
output_file = 'all-mobile.xlsx'
df.to_excel(output_file, index=False)

print(f"Data has been successfully converted to {output_file}")
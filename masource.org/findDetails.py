from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
import pandas as pd
import time

# Initialize WebDriver options
options = webdriver.ChromeOptions()
options.debugger_address = "127.0.0.1:9222"
driver = webdriver.Chrome(options=options)

# Load the Excel file
excel_file_path = 'companies2.xlsx'
df = pd.read_excel(excel_file_path, engine='openpyxl')
companies = df.to_dict(orient='records')

data = []

def get_element(driver, xpath, retries=3):
    for _ in range(retries):
        try:
            return WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, xpath)))
        except StaleElementReferenceException:
            time.sleep(1)
        except TimeoutException:
            return None
    return None

def get_element_text(driver, xpath, retries=3):
    element = get_element(driver, xpath, retries)
    return element.text if element else None

def get_element_attribute(driver, xpath, attribute, retries=3):
    element = get_element(driver, xpath, retries)
    return element.get_attribute(attribute) if element else None
count = 1
for row in companies:
    try:
        driver.get(row["url"])
        all_urls = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//h4//a')))
        urls = []
        for i in range(len(all_urls)):
            urls.append(all_urls[i].get_attribute("href"))
        
        for url in urls:
            dictionary = {
                "URL": url,
                "State": row['state']
            }

            driver.get(url)

            dictionary["FullName"] = get_element_text(driver, "//h1")
            left_elements = driver.find_elements(By.XPATH, '//div[@class="content__page--box-left"]//div[@class="brokers__profile--data"]')

            if left_elements:
                dictionary["Phone"] = get_element_text(driver, '//div[@class="content__page--box-left"]//div[@class="brokers__profile--data"][1]//a')
                dictionary["Email"] = get_element_text(driver, '//div[@class="content__page--box-left"]//div[@class="brokers__profile--data"][2]//a')
                dictionary["Company"] = get_element_text(driver, '//div[@class="content__page--box-left"]//div[@class="brokers__profile--data"][3]//p')

            dictionary["Address"] = get_element_text(driver, '//div[@class="brokers__profile--data address"]')
            dictionary["Website"] = get_element_attribute(driver, '//div[@class="content__page--box-right"]//div[@class="brokers__profile--data"]//a', 'href')

            data.append(dictionary)
            print(count)
            count += 1
    
    except Exception as e:
        print(f"Error processing {row['url']}: {e}")

# Save the updated DataFrame to a new Excel file
output_excel_path = 'data2.xlsx'
df_output = pd.DataFrame(data)
df_output.to_excel(output_excel_path, index=False)

# Close the WebDriver session
driver.quit()

print(f"Updated data saved to {output_excel_path}")

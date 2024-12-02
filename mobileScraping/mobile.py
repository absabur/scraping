from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
import logging
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

# Set up logging
logging.basicConfig(level=logging.INFO)

# Automatically download the correct ChromeDriver version
service_obj = Service(ChromeDriverManager().install())
options = webdriver.ChromeOptions()

options.add_argument("--start-maximized")
# Alternative option to start in full-screen mode (not just maximized, but fully in full screen)
# options.add_argument("--kiosk")


# Uncomment the next line to run in headless mode
# options.add_argument("--headless")
options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
)
driver = webdriver.Chrome(service=service_obj, options=options)

linksList = []


def getLinks(p):

    driver.get(f"https://www.mobiledokan.com/mobile-price-list?fromprice=0&toprice=550000&page={p}")

    # Wait for the elements to load
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, '//span[contains(text(),"View Details")]/ancestor::a'))
    )
    
    # Find all matching <a> tags
    links = driver.find_elements(By.XPATH, '//span[contains(text(),"View Details")]/ancestor::a')

    # Extract the href attribute from each link
    for link in links:
        href = link.get_attribute('href')
        linksList.append(href)


# Loop through the pages and collect links
for i in range(1, 190):
    getLinks(i)

df = pd.DataFrame(linksList, columns=["Links"])

# Save the DataFrame to an Excel file
df.to_excel("links.xlsx", index=False)
driver.quit()
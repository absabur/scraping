from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

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
    try:
        driver.get(f"https://www.mobiledokan.co/filter/page/{p}")

        # Wait for the elements to load
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located(
                (By.XPATH, '//h2[@class="aps-product-title"]//a')
            )
        )

        # Find all matching <a> tags
        links = driver.find_elements(By.XPATH, '//h2[@class="aps-product-title"]//a')

        # Extract the href attribute from each link
        for link in links:
            href = link.get_attribute("href")
            linksList.append(href)
    except Exception as e:
        print(f"error {e}")


# Loop through the pages and collect links
for i in range(1, 288):
    getLinks(i)
    # if i == 1:
    #     break

df = pd.DataFrame(linksList, columns=["Links"])

# Save the DataFrame to an Excel file
df.to_excel("data/all-links.xlsx", index=False)
driver.quit()

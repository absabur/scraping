# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.chrome.service import Service
# import logging
# from webdriver_manager.chrome import ChromeDriverManager
# import pandas as pd

# # Set up logging
# # logging.basicConfig(level=logging.INFO)

# # Automatically download the correct ChromeDriver version
# service_obj = Service(ChromeDriverManager().install())
# options = webdriver.ChromeOptions()

# options.add_argument("--start-maximized")
# # Alternative option to start in full-screen mode (not just maximized, but fully in full screen)
# # options.add_argument("--kiosk")


# # Uncomment the next line to run in headless mode
# # options.add_argument("--headless")
# options.add_argument(
#     "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
# )
# driver = webdriver.Chrome(service=service_obj, options=options)

# def save_to_excell(mobiles, pathname):
#     flattened_data = []

#     # Loop through each mobile
#     for mobile in mobiles:
#         name = mobile['name']
        
#         # Add specifications to the flattened data
#         for spec in mobile['specs']:
#             category = spec['category']
#             for specification in spec['specification']:
#                 spec_key = list(specification.keys())[0]
#                 spec_value = list(specification.values())[0]
#                 flattened_data.append({
#                     'Mobile Name': name,
#                     'Category': category,
#                     'Specification': spec_key,
#                     'Value': spec_value,
#                     'Price': None,  # No price here for specifications
#                 })
        
#         # Add prices to the flattened data
#         for price in mobile['prices']:
#             variant = price['varient']
#             price_value = price['price']
#             status = price.get('status', 'N/A')
#             flattened_data.append({
#                 'Mobile Name': name,
#                 'Category': 'Price',
#                 'Varient': variant,
#                 'Price': price_value,
#                 'Status': status
#             })
            
#     df = pd.DataFrame(flattened_data)
#     df.to_excel(pathname, index=False)

# df = pd.read_excel("phone-links.xlsx")

# mobiles = []


# def getLinks(link):
#     try:
#         driver.get(link)
#         WebDriverWait(driver, 20).until(
#             EC.presence_of_element_located((By.XPATH, '//h1[@itemprop="name"]'))
#         )
#         mobileSpec = dict()
        
#         name = driver.find_element(By.XPATH, '//h1[@itemprop="name"]')
#         print(f"Scrapint {name.text}")
#         mobileSpec["name"] = name.text

#         varients = driver.find_elements(By.XPATH, '//li[@class="col-4 col-md-3 p-0"]')
#         status = driver.find_elements(By.XPATH, '//span[@class="tag"]')
#         prices = []
#         for varient in range(0, len(varients)):
#             priceDict = dict()
#             priceDict[f"varient"] = varients[varient].find_element(By.XPATH, './/span[@class="d-block fw-bold vtst"]').text
#             priceDict[f"price"] = varients[varient].find_element(By.XPATH, './/span[@class="ptst"]').text
#             if varient == 0:
#                 priceDict[f"status"] = status[0].text
#             prices.append(priceDict)
            
                
#         if len(status) > 1:
#             priceDict = dict()
#             priceDict[f"varient"] = varients[0].find_element(By.XPATH, './/span[@class="d-block fw-bold vtst"]').text
#             priceDict[f"price"] = varients[0].find_element(By.XPATH, './/span[@class="ptst"]').text
#             priceDict[f"status"] = status[1].text
#             prices.append(priceDict)
                
        
#         mobileSpec["prices"] = prices
        
#         spec_elements = driver.find_elements(By.XPATH, '//div[@class="row mb-2 pb-2 border-bottom"]')
#         specs = []
#         for spec in spec_elements:
#             spceDict = dict()
#             table = spec.find_elements(By.XPATH, './/table')  
#             for tab in table:
#                 if len(table) == 1:
#                     category = spec.find_element(By.XPATH, './/h3').text
#                 else:
#                     category = spec.find_element(By.XPATH, './/div[@class="subgroup my-2 pb-1"]').text
#                 spceDict['category'] = category  
#                 rows = tab.find_elements(By.XPATH, './/tr') 
#                 specificationList = []               
#                 for row in rows:
#                     specification = dict()              
#                     column = row.find_elements(By.XPATH, './/td')
#                     specification[column[0].text] = column[1].text
#                     specificationList.append(specification)
#                 spceDict['specification'] = specificationList
#             specs.append(spceDict)
#         mobileSpec["specs"] = specs
                    
                    
        
        

#         mobiles.append(mobileSpec)
#     except Exception as e:
#         print(f"{e}")
    


# # Loop through the pages and collect links

# count = 1
# for link in df['Links']:
#     print(f"scraping phone number: {count}")
#     getLinks(link)
#     print("\n===============================\n")
#     count += 1
#     if count % 5 == 0:
#         save_to_excell(mobiles, f'upto-{count}.xlsx')
#     # if count == 2:
#     #     break
    


# # print(mobiles)


# save_to_excell(mobiles, "all-mobile.xlsx")


# driver.quit()












from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
import logging
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
from bs4 import BeautifulSoup
import os
import requests

# Set up logging
# logging.basicConfig(level=logging.INFO)

# Automatically download the correct ChromeDriver version
service_obj = Service(ChromeDriverManager().install())
options = webdriver.ChromeOptions()

options.add_argument("--start-maximized")
# Uncomment the next line to run in headless mode
# options.add_argument("--headless")
options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
)
driver = webdriver.Chrome(service=service_obj, options=options)

def download_images(image_div, folder):
    os.makedirs(folder, exist_ok=True)
    saved_image_paths = []  # List to store saved image paths
    for img in image_div.find_elements(By.TAG_NAME, 'img'):
        img_url = img.get_attribute('src')
        img_name = img_url.split("/")[-1]
        img_path = os.path.join(folder, img_name)

        # Download the image using requests with SSL verification disabled
        try:
            response = requests.get(img_url, stream=True, verify=False)  # Disable SSL verification
            if response.status_code == 200:
                with open(img_path, 'wb') as file:
                    for chunk in response.iter_content(1024):
                        file.write(chunk)
                # print(f"Saved {folder} image: {img_path}")
                saved_image_paths.append(img_path)
        except Exception as e:
            print(f"Error downloading {img_url}: {e}")
    return saved_image_paths


def save_to_excel(mobiles, pathname):
    flattened_data = []

    # Loop through each mobile
    for mobile in mobiles:
        name = mobile['name']
        
        # Add specifications to the flattened data
        for spec in mobile['specs']:
            category = spec['category']
            for specification in spec['specification']:
                spec_key = list(specification.keys())[0]
                spec_value = list(specification.values())[0]
                flattened_data.append({
                    'Mobile Name': name,
                    'URL': mobile['url'],  # Add URL here
                    'Category': category,
                    'Specification': spec_key,
                    'Value': spec_value,
                    'Variant': '',
                    'Price': '',
                    'Status': '',
                })
        
        # Add prices to the flattened data
        for price in mobile['prices']:
            variant = price['varient']
            price_value = price['price']
            status = price.get('status', 'N/A')
            flattened_data.append({
                'Mobile Name': name,
                'URL': mobile['url'],  # Add URL here
                'Category': '',
                'Specification': '',
                'Value': '',
                'Variant': variant,
                'Price': price_value,
                'Status': status,
            })

        # Add View Images URLs
        for view_image in mobile.get('ViewImage', []):
            flattened_data.append({
                'Mobile Name': name,
                'URL': mobile['url'],  # Add URL here
                'Category': '',
                'Specification': '',
                'Value': '',  # Image URL
                'Variant': '',
                'Price': '',
                'Status': '',
                'ImageType': 'View Image',
                'ImagePath': view_image,  # Image URL
            })

        # Add Color Images URLs
        for color_image in mobile.get('ColorImage', []):
            flattened_data.append({
                'Mobile Name': name,
                'URL': mobile['url'],  # Add URL here
                'Category': '',
                'Specification': '',
                'Value': '',  # Image URL
                'Variant': '',
                'Price': '',
                'Status': '',
                'ImageType': 'Color Image',
                'ImagePath': color_image,  # Image URL
            })
    
    # Convert the flattened data into a DataFrame
    df = pd.DataFrame(flattened_data)
    
    # Save the DataFrame to Excel
    df.to_excel(pathname, index=False)
    
    
df = pd.read_excel("phone-links.xlsx")

mobiles = []
all_mobiles = []

def getLinks(link):
    try:
        driver.get(link)
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//h1[@itemprop="name"]'))
        )
        
        # Use BeautifulSoup to parse the page source
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        mobileSpec = dict()
        
        name = soup.find('h1', itemprop="name").text.strip()
        print(f"Scraping {name}")
        mobileSpec["name"] = name
        mobileSpec["url"] = link  # Store the URL

        varients = soup.find_all('li', class_='col-4 col-md-3 p-0')
        status = soup.find_all('span', class_='tag')
        prices = []
        for varient in varients:
            priceDict = dict()
            priceDict["varient"] = varient.find('span', class_='d-block fw-bold vtst').text.strip()
            priceDict["price"] = varient.find('span', class_='ptst').text.strip()
            priceDict["status"] = status[0].text.strip() if varient == varients[0] else "N/A"
            prices.append(priceDict)
        
        # Handle additional price statuses
        if len(status) > 1:
            priceDict = dict()
            priceDict["varient"] = varients[0].find('span', class_='d-block fw-bold vtst').text.strip()
            priceDict["price"] = varients[0].find('span', class_='ptst').text.strip()
            priceDict["status"] = status[1].text.strip()
            prices.append(priceDict)

        mobileSpec["prices"] = prices
        
        spec_elements = soup.find_all('div', class_='row mb-2 pb-2 border-bottom')
        specs = []
        for spec in spec_elements:
            tables = spec.find_all('table')
            category = spec.find_all('div', class_='subgroup my-2 pb-1')
            i = 0
            for table in tables:
                specificationList = []
                spceDict = dict()
                if len(category) == 0:
                    spceDict['category'] = spec.find('h3').text.strip()
                else:
                    spceDict['category'] = category[i].text.strip()
                rows = table.find_all('tr')
                for row in rows:
                    columns = row.find_all('td')
                    if len(columns) >= 2:  # Ensure there are at least two columns
                        specification = {columns[0].text.strip(): columns[1].text.strip()}
                        specificationList.append(specification)
                spceDict['specification'] = specificationList
                specs.append(spceDict)
                i += 1
            
            
        driver.get(f"{link}/gallery")  # Replace with actual URL

        image_divs = driver.find_elements(By.XPATH, '//div[@class="small-images"]')
        
        mobileSpec["specs"] = specs
        if len(image_divs) >= 2:
            
            mobileSpec['ViewImage'] = download_images(image_divs[0], 'view')
            mobileSpec['ColorImage'] = download_images(image_divs[1], 'colors')
        elif len(image_divs) == 1:
            
            mobileSpec['ViewImage'] = download_images(image_divs[0], 'view')
        else:
            print("Not enough divs found.")
        
        if (len(mobileSpec['ViewImage']) == 0):
            image_divs = driver.find_element(By.XPATH, '//div[@class="col-12 col-xl-8"]')
            mobileSpec['ViewImage'] = download_images(image_divs, 'view')
            
            

        mobiles.append(mobileSpec)
        all_mobiles.append(mobileSpec)
    except Exception as e:
        print(f"Error: {e}")

# Loop through the pages and collect links
count = 1
for link in df['Links']:
    print(f"Scraping phone number: {count}")
    getLinks(link)
    print("\n===============================\n")
    # if count == 2:
    #     break
    count += 1
    if count % 100 == 0:
        save_to_excel(mobiles, f'upto-{count}.xlsx')
        mobiles = []


save_to_excel(mobiles, f'upto-{count}.xlsx')
save_to_excel(all_mobiles, "all-mobile.xlsx")

driver.quit()


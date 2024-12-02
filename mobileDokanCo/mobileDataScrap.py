# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager
# import pandas as pd
# from bs4 import BeautifulSoup
# import os
# import requests

# # Set up logging
# # logging.basicConfig(level=logging.INFO)

# # Automatically download the correct ChromeDriver version
# service_obj = Service(ChromeDriverManager().install())
# options = webdriver.ChromeOptions()

# options.add_argument("--start-maximized")
# # Uncomment the next line to run in headless mode
# # options.add_argument("--headless")
# options.add_argument(
#     "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
# )
# driver = webdriver.Chrome(service=service_obj, options=options)

# def download_images(images, folder):
#     os.makedirs(folder, exist_ok=True)
#     saved_image_paths = []  # List to store saved image paths
#     downloaded_urls = set()  # Track unique URLs to avoid duplicates
    
#     for img in images:
#         img_url = img.get_attribute('src')
#         img_url = img_url.replace("-120x120", "")
#         if img_url and img_url not in downloaded_urls:
#             downloaded_urls.add(img_url)
#             img_name = img_url.split("/")[-1]
#             img_path = os.path.join(folder, img_name)

#             # Download the image
#             try:
#                 response = requests.get(img_url, stream=True, verify=False)
#                 if response.status_code == 200:
#                     with open(img_path, 'wb') as file:
#                         for chunk in response.iter_content(1024):
#                             file.write(chunk)
#                     saved_image_paths.append(img_path)
#             except Exception as e:
#                 print(f"Error downloading {img_url}: {e}")
#     return saved_image_paths
    
    
# df = pd.read_excel("datas/all-links.xlsx")

# mobiles = []
# allMobiles = []

# def getLinks(link):
#     try:
#         driver.get(link)
#         WebDriverWait(driver, 20).until(
#             EC.presence_of_element_located((By.XPATH, '//h1[@class="aps-main-title"]'))
#         )        
#         mobileSpec = dict()
#         mobileSpec['name'] = driver.find_element(By.XPATH, '//h1[@class="aps-main-title"]').text
#         mobileSpec['url'] = link
#         mobileSpec['price'] = driver.find_element(By.XPATH, '//span[@class="aps-price-value"]').text
#         try:
#             mobileSpec['prevPrice'] = driver.find_element(By.XPATH, '//span[@class="aps-price-value"]//del').text
#         except:
#             mobileSpec['prevPrice'] = ''
#         mobileSpec['brand'] = driver.find_element(By.XPATH, '//a[@itemprop="brand"]').text
#         mobileSpec['deviceType'] = driver.find_element(By.XPATH, '//span[@class="aps-product-cat"]//a').text
        
#         pros = driver.find_elements(By.XPATH, '//ul[@class="wp-block-list"]//li')
#         prosList = [pro.text for pro in pros]
#         mobileSpec['pros'] = prosList
        
#         cons = driver.find_elements(By.XPATH, '//div[@class="cons tie-list-shortcode"]//li')
#         consList = [con.text for con in cons]
#         mobileSpec['cons'] = consList
        
#         keyFeatures = driver.find_elements(By.XPATH, '//ul[@class="aps-features-iconic"]//li')
        
#         featDict = dict()
#         for feature in keyFeatures:
#             name = feature.find_element(By.XPATH, './/span[@class="aps-feature-nm"]').text
#             featDict[name] = feature.find_element(By.XPATH, './/strong').text
        
#         mobileSpec['keyFeatures'] = featDict     
         
        
#         specs = driver.find_elements(By.XPATH, '//div[@class="aps-group"]')
        
#         catedict = dict()
#         for spec in specs:
#             category = spec.find_element(By.XPATH, './/h3').text
#             rows = spec.find_elements(By.XPATH, './/tr')
#             specDict = dict()
#             for row in rows:
#                 name = row.find_element(By.XPATH, './/td[1]//strong').text
#                 specDict[name] = row.find_element(By.XPATH, './/td[2]').text
                
#             catedict[category] = specDict
            
#         mobileSpec['specification'] = catedict
        
#         desc = driver.find_element(By.XPATH, '//div[@itemprop="description"]')
#         html_content = desc.get_attribute('innerHTML')
#         mobileSpec['description'] = html_content 
        
#         images = driver.find_elements(By.XPATH, '//div[@class="owl-stage"]//img')
#         mobileSpec['images'] = download_images(images, 'images')

#         # If no images were downloaded, try the fallback
#         if len(mobileSpec['images']) == 0:
#             try:
#                 single_image_div = driver.find_elements(By.XPATH, '//div[@class="aps-main-image aps-main-img-zoom"]//img')
#                 mobileSpec['images'] = download_images(single_image_div, 'images')
#             except Exception as e:
#                 print(f"Error finding the fallback image div: {e}")
        
#         mobiles.append(mobileSpec)
#         allMobiles.append(mobileSpec)
#     except Exception as e:
#         print(f"Error: {e}")


# import json

# # Loop through the pages and collect links
# count = 1
# for link in df['Links']:
#     print(f"Scraping phone number: {count}")
#     getLinks(link)
#     print("\n===============================\n")
#     # if count == 5:
#     #     break
#     count += 1
#     if count % 50 == 0:
#         with open(f'separated/upto-{count}.json', "w") as json_file:
#             json.dump(mobiles, json_file, indent=4)
#         mobiles = []

# with open('datas/all-mobiles.json', "w") as json_file:
#     json.dump(allMobiles, json_file, indent=4)

# driver.quit()



















from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
import requests
import os
import json
from concurrent.futures import ThreadPoolExecutor

service_obj = Service(ChromeDriverManager().install())
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")
driver = webdriver.Chrome(service=service_obj, options=options)

# Image Downloading with ThreadPoolExecutor
def download_image(img_url, folder):
    os.makedirs(folder, exist_ok=True)
    img_url = img_url.replace("-120x120", "")
    img_name = img_url.split("/")[-1]
    img_path = os.path.join(folder, img_name)
    try:
        response = requests.get(img_url, stream=True, verify=False)
        if response.status_code == 200:
            with open(img_path, 'wb') as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)
            return img_path
    except Exception as e:
        print(f"Error downloading {img_url}: {e}")
    return None

def download_images(images, folder):
    with ThreadPoolExecutor() as executor:
        image_paths = list(filter(None, executor.map(lambda img: download_image(img.get_attribute('src'), folder), images)))
    return image_paths

# Load Links from Excel
df = pd.read_excel("datas/all-links.xlsx")
mobiles = []
allMobiles = []

def get_links(link):
    try:
        driver.get(link)
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")

        mobileSpec = {
            "name": soup.select_one('h1.aps-main-title').text,
            "url": link,
            "price": soup.select_one('span.aps-price-value').text,
            "prevPrice": soup.select_one('span.aps-price-value del').text if soup.select_one('span.aps-price-value del') else '',
            "brand": soup.select_one('a[itemprop="brand"]').text,
            "deviceType": soup.select_one('span.aps-product-cat a').text,
            "pros": [pro.text for pro in soup.select('ul.wp-block-list li')],
            "cons": [con.text for con in soup.select('div.cons.tie-list-shortcode li')],
        }

        # Key Features
        featDict = {feature.select_one('.aps-feature-nm').text.strip(): feature.select_one('strong').text for feature in soup.select('ul.aps-features-iconic li')}
        mobileSpec['keyFeatures'] = featDict

        # Specifications
        specs = {}
        for spec_group in soup.select('div.aps-group'):
            category = spec_group.select_one('h3').text
            specs[category.strip()] = {row.select_one('td strong').text.strip(): row.select_one('td:nth-of-type(2)').text for row in spec_group.select('tr')}
        mobileSpec['specification'] = specs

        # Description
        description = soup.select_one('div[itemprop="description"]')
        mobileSpec['description'] = description.decode_contents() if description else ""

        # Images
        images = driver.find_elements(By.XPATH, '//div[@class="owl-stage"]//img')
        mobileSpec['images'] = download_images(images, 'images')

        if len(mobileSpec['images']) == 0:  # Fallback if no images in owl-stage
            single_image_div = driver.find_elements(By.XPATH, '//div[@class="aps-main-image aps-main-img-zoom"]//img')
            mobileSpec['images'] = download_images(single_image_div, 'images')

        mobiles.append(mobileSpec)
        allMobiles.append(mobileSpec)
    except:
        with open(f'missed-{count}.json', "w") as json_file:
            json.dump({"link": f"{link}"}, json_file, indent=4)


# Loop through the pages and collect links
count = 1
for link in df['Links']:
    print(f"Scraping phone number: {count}")
    get_links(link)
    print("\n===============================\n")
    # if count == 5:
    #     break
    count += 1
    if count % 50 == 0:
        with open(f'separated/upto-{count}.json', "w") as json_file:
            json.dump(mobiles, json_file, indent=4)
        mobiles = []
 
# Save all mobiles data
with open('datas/all-mobiles.json', "w") as json_file:
    json.dump(allMobiles, json_file, indent=4)

driver.quit()
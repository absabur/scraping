from selenium import webdriver
options = webdriver.ChromeOptions()
options.debugger_address = "127.0.0.1:9222"
driver = webdriver.Chrome(options=options)
from selenium.webdriver.common.by import By
import pandas as pd

# "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="C:\Users\absab\AppData\Local\Google\Chrome\User Data\Profile 1"
# %LOCALAPPDATA%
# chrome://version/
# https://chatgpt.com/c/dcbf62ec-e118-4299-a10c-4c182966cd8c

driver.get("https://instacoach.com/listings?sports=Baseball&distance=30")
input(":")
data = []
sections = driver.find_elements(By.XPATH, '//div[@class="listings_feature_body_card__kK_wB"]')
for section in sections:
    single = {}
    single["URL"] = section.find_element(By.XPATH, './/a').get_attribute('href')
    single["Location"] = section.find_element(By.XPATH, './/div[@class="maincard_maincard_body_mode__9gepQ"]//span').text
    try:
        single["Ratings"] = section.find_element(By.XPATH, './/div[@class="maincard_maincard_body_rating__zTbK0 maincard_new__W8V0Z"]//span').text
    except:
        single["Ratings"] = section.find_element(By.XPATH, './/div[@class="maincard_maincard_body_rating__zTbK0"]//span').text
    single["Name"] = section.find_element(By.XPATH, './/h3').text
    single["Role"] = section.find_element(By.XPATH, './/div[@class="maincard_maincard_body_box2__ujRsC"]//div//span[2]').text
    single["Description"] = section.find_element(By.XPATH, './/div[@class="maincard_maincard_body_box3__hxiM8"]').text
    srcset = section.find_element(By.XPATH, './/div[@class="maincard_maincard_img_box__YrHQK"]//img').get_attribute('srcset')
    image_urls = [f"https://instacoach.com{url.split()[0]}" for url in srcset.split(',')]
    single["images"] = image_urls[-1]
    data.append(single)
        
  

driver.quit()

df = pd.DataFrame(data)

person_path = f'baseball.xlsx'

df.to_excel(person_path, index=False)

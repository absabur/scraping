from selenium import webdriver
from selenium.webdriver.chrome.service import Service
service_obj=Service(r"c:\chromedriver.exe")
driver=webdriver.Chrome(service=service_obj)
from selenium.webdriver.common.by import By
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

excel_file_path = 'linkinsta.xlsx'

df = pd.read_excel(excel_file_path)

employees = df.to_dict(orient='records')

count = 1

driver.get(f"https://www.google.com/search?q=instagram")
input(f"current: {count}, login insta: ")


for employee in employees:
    for i in [25, 50, 75, 100, 125, 150, 175, 200]:
        if count == i:
            time.sleep(2)
    try:
        driver.get(employee["InstagramUrl"])
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//main//header'))
        )
        usernameelement = driver.find_elements(By.XPATH, '//a//h2//span')
        followerselement = driver.find_elements(By.XPATH, '//li//div//a[contains(text(), "followers")]//span//span')
        if len(followerselement) == 0:
            followerselement = driver.find_elements(By.XPATH, '//li//div[contains(text(), "followers")]//span//span')
        if len(usernameelement) > 0:
            username = usernameelement[0].text
        if len(followerselement) > 0:
            followers = followerselement[0].text        
        private_message = driver.find_elements(By.XPATH, '//span[contains(text(), "This account is private")]')
        employee["Username"] = username
        employee["Followers"] = followers
        if private_message:
            employee["Status"] = "private"
        else:
            employee['Status'] = "public"
    except Exception as e:
        print(f"{e}")

    count += 1


driver.quit()




df = pd.DataFrame(employees)

excel_file_path = f'output-insta.xlsx'

df.to_excel(excel_file_path, index=False)

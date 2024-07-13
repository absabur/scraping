from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# service_obj=Service(r"c:\chromedriver.exe")
# driver=webdriver.Chrome(service=service_obj)

# "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="C:\Users\absab\AppData\Local\Google\Chrome\User Data\Profile 9"


options = webdriver.ChromeOptions()
options.debugger_address = "127.0.0.1:9222"
driver = webdriver.Chrome(options=options)



from selenium.webdriver.common.by import By
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pyautogui, pyperclip, re

excel_file_path = 'insta.xlsx'

df = pd.read_excel(excel_file_path)

employees = df.to_dict(orient='records')

count = 1


for employee in employees:
    for i in [25, 50, 75, 100, 125, 150, 175, 200, 225, 250, 275, 300, 325, 350, 375, 400]:
        if count == i:
            time.sleep(2)
    try:
        pyautogui.click(626, 863, duration=0.3)
        clean_url = re.sub(r'\?hl=.*$', '', f"{employee['InstagramUrl']}")
        clean_url = re.sub(r'\?locale=.*$', '', f"{clean_url}")
        if clean_url == 'nan':
            continue
        employee['clean_url'] = clean_url
        pyperclip.copy(clean_url)
        pyautogui.hotkey('ctrl', 'l')
        pyautogui.hotkey('ctrl', 'v')
        pyautogui.press('enter')
        print(f"Current {count}")
        # driver.get(employee["InstagramUrl"])
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
        val = input("s for stop: ")
        if val  == "s":
            break
    count += 1


driver.quit()




df = pd.DataFrame(employees)

excel_file_path = f'output-insta.xlsx'

df.to_excel(excel_file_path, index=False)

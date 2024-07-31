from selenium import webdriver
options = webdriver.ChromeOptions()
options.debugger_address = "127.0.0.1:9222"
driver = webdriver.Chrome(options=options)
from selenium.webdriver.common.by import By
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time, random
import pyperclip, pyautogui


# "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="C:\Users\absab\AppData\Local\Google\Chrome\User Data\Profile 1"
# %LOCALAPPDATA%
# chrome://version/
# https://chatgpt.com/c/dcbf62ec-e118-4299-a10c-4c182966cd8c

more = driver.find_elements(By.XPATH, '//div[@aria-label="More"]')


profile = 1
for p in more:
    try:
        p.click()
        time.sleep(0.01)
        unf = driver.find_element(By.XPATH, '//div[@role="menuitem"][4]')
        unf.click()
        time.sleep(0.01)
        con = driver.find_element(By.XPATH, '//div[@aria-label="Confirm"]')
        con.click()
        time.sleep(0.01)
        profile += 1

    except:
        print("No profile found.")
        # val = input("SType (e) for end:  ")
        # if val == "e":
        #     break

print(f"{profile} unfriend")
driver.quit()


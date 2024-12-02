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


# print(pyautogui.position())

for i in range(100):
    # time.sleep(0.5)
    # pyautogui.click(407, 484)

    # time.sleep(0.5)
    # pyautogui.click(402, 523)

    # time.sleep(0.5)
    # pyautogui.click(1047, 483)

    # time.sleep(0.5)
    # pyautogui.click(1050, 525)
    
    # time.sleep(2)
    # pyautogui.click(716, 305)
    # pyautogui.click(716, 355)
    # pyautogui.click(716, 390)

    # pyautogui.click(626, 986)
    # time.sleep(4)
    
    time.sleep(0.5)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//div[@data-input="checkbox"]'))
    )
    time.sleep(0.5)
    checkbox = driver.find_element(By.XPATH, '//div[@data-input="checkbox"]')
    checkbox.click()

    # 2. Click on "Select this page"
    select_page = driver.find_element(By.XPATH, '//a[contains(text(), "Select this page")]')
    select_page.click()

    # 3. Click on "Enrich"
    enrich = driver.find_element(By.XPATH, '//div[contains(text(), "Enrich")]')
    enrich.click()

    # 4. Click on "Enrich emails" link
    enrich_emails_link = driver.find_element(By.XPATH, '//a[contains(text(), "Enrich emails")]')
    enrich_emails_link.click()
    time.sleep(2)
    pyautogui.click(716, 305)
    pyautogui.click(716, 320)
    pyautogui.click(716, 345)
    pyautogui.click(716, 360)
    pyautogui.click(716, 375)
    pyautogui.click(716, 390)
    pyautogui.click(716, 405)



    # # 6. Click on the button with aria-label="right-arrow"
    right_arrow_button = driver.find_element(By.XPATH, '//button[@aria-label="right-arrow"]')
    right_arrow_button.click()





# checkbox = driver.find_element(By.XPATH, '//div[@data-input="checkbox"]')
# checkbox.click()

# # 2. Click on "Select this page"
# select_page = driver.find_element(By.XPATH, '//a[contains(text(), "Select this page")]')
# select_page.click()

# # 3. Click on "Enrich"
# enrich = driver.find_element(By.XPATH, '//div[contains(text(), "Enrich")]')
# enrich.click()

# # 4. Click on "Enrich emails" link
# enrich_emails_link = driver.find_element(By.XPATH, '//a[contains(text(), "Enrich emails")]')
# enrich_emails_link.click()


# time.sleep(3)
# # 5. Click on "Enrich emails" div
# enrich_emails_div = driver.find_element(By.XPATH, '//div[contains(text(), "Enrich emails")]')
# enrich_emails_div.click()

# time.sleep(3)
# # 6. Click on the button with aria-label="right-arrow"
# right_arrow_button = driver.find_element(By.XPATH, '//button[@aria-label="right-arrow"]')
# right_arrow_button.click()
# time.sleep(3)



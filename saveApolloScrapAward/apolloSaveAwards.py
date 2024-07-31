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


def remove_duplicate_lines(input_string):
    lines = input_string.split('\n')
    unique_lines = []
    seen = set()
    
    for line in lines:
        if line not in seen:
            unique_lines.append(line)
            seen.add(line)
    
    return '\n'.join(unique_lines)

# "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="C:\Users\absab\AppData\Local\Google\Chrome\User Data\Profile 1"
# %LOCALAPPDATA%
# chrome://version/
# https://chatgpt.com/c/dcbf62ec-e118-4299-a10c-4c182966cd8c

excel_file_path = 'awards.xlsx'

df = pd.read_excel(excel_file_path)

persons = df.to_dict(orient='records')
profile = 1
input("Focus:====================")
time.sleep(2)
for p in persons:
    try:
        pyautogui.click(626, 863, duration=0.3)
        time.sleep(1)
        pyperclip.copy(f"{p['all_href']}")
        time.sleep(0.3)
        pyautogui.hotkey('ctrl', 'l')
        time.sleep(0.3)
        pyautogui.hotkey('ctrl', 'a')
        time.sleep(0.3)
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(0.3)
        pyautogui.press('enter')
        print("\n=====================================\n")
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//main'))
        )

        # p["linkedin"] = driver.current_url
        # time.sleep(random.randint(4,6))
        time.sleep(1)
        pyautogui.scroll(5000)
        time.sleep(1)
        pyautogui.scroll(-4000)
        time.sleep(1)
        pyautogui.scroll(3000)
        
        pyautogui.moveTo(593, 177, duration=1)
        pyautogui.click(572, 187, duration=0.4)
        # time.sleep(random.randint(4,6))
        time.sleep(1)
        pyautogui.scroll(4000)
        time.sleep(1)
        pyautogui.scroll(-3000)
        time.sleep(1)
        pyautogui.scroll(2500)
        pyautogui.click(581, 325, duration=1)
        
        time.sleep(1)
        pyautogui.click(800, 863, duration=0.3)
        
        val = input("Save to apollo,\n Press Enter for next, Type (e) for end:  ")
        
        if val == "e":
            break
        
        pyautogui.click(626, 863, duration=0.3)
        time.sleep(1)
        pyperclip.copy(f"{driver.current_url}details/honors")
        time.sleep(0.3)
        pyautogui.hotkey('ctrl', 'l')
        time.sleep(0.3)
        pyautogui.hotkey('ctrl', 'a')
        time.sleep(0.3)
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(0.3)
        pyautogui.press('enter')
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//main'))
        )
        lists = driver.find_elements(By.XPATH, "//main//li[@class='pvs-list__paged-list-item artdeco-list__item pvs-list__item--line-separated pvs-list__item--one-column']")
        
        count = 1
        for li in lists:
            award = remove_duplicate_lines(li.text)
            p[f"HonorsAndAwards{count}"] = award
            count += 1
        time.sleep(random.uniform(0.5, 1.0))
        
    except:
        print("No profile found.")
        val = input("Save to apollo,\n Press Enter for next, Type (e) for end:  ")
        if val == "e":
            break
    print(f"{profile}| {p['all']}")
    profile += 1

driver.quit()
df = pd.DataFrame(persons)
person_path = f'awardsoutput10.xlsx'
df.to_excel(person_path, index=False)

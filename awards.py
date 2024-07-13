from selenium import webdriver


# from selenium.webdriver.chrome.service import Service
# service_obj=Service(r"c:\chromedriver.exe")
# driver=webdriver.Chrome(service=service_obj)




# from selenium.webdriver.firefox.service import Service
# gecko_path = r'c:\geckodriver.exe'
# # Create a service object
# service = Service(gecko_path)
# driver = webdriver.Firefox(service=service)




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
    
    # return '\n'.join(unique_lines)
    return unique_lines[0]

excel_file_path = 'awards.xlsx'

df = pd.read_excel(excel_file_path)

persons = df.to_dict(orient='records')
profile = 1
input("Focus:====================")
time.sleep(2)
for p in persons:
    try:        
                
        pyautogui.click(626, 863, duration=0.3)
        pyperclip.copy(f"{p['linkedin']}/details/honors")
        pyautogui.hotkey('ctrl', 'l')
        time.sleep(0.3)
        pyautogui.hotkey('ctrl', 'a')
        time.sleep(0.3)
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(0.3)
        pyautogui.press('enter')
        pyautogui.click(726, 863, duration=0.3)
        time.sleep(2)
        pyautogui.press('enter')
        val = input("Press Enter for next, Type (e) for end:  ")
        if val == "e":
            break
        
        
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//main'))
        )
        lists = driver.find_elements(By.XPATH, "//main//li[@class='pvs-list__paged-list-item artdeco-list__item pvs-list__item--line-separated pvs-list__item--one-column']")
        
        count = 1
        for li in lists:
            award = remove_duplicate_lines(li.text)
            if "Nothing to see for now" not in award:
                p[f"HonorsAndAwards{count}"] = award
            count += 1
        time.sleep(random.uniform(2.5, 5.5))
        
    except:
        print("No profile found.")
        val = input("Save to apollo,\n Press Enter for next, Type (e) for end:  ")
        if val == "e":
            break
    print(f"{profile}| {p['name']}")
    profile += 1

driver.quit()
df = pd.DataFrame(persons)
person_path = f'awardsout2.xlsx'
df.to_excel(person_path, index=False)

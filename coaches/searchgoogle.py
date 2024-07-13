# from selenium import webdriver
# options = webdriver.ChromeOptions()
# options.debugger_address = "127.0.0.1:9222"
# driver = webdriver.Chrome(options=options)

# "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="C:\Users\absab\AppData\Local\Google\Chrome\User Data\Profile 9"

import pandas as pd
import pyperclip, pyautogui, time

excel_file_path = 'coaches.xlsx'
df = pd.read_excel(excel_file_path)
coaches = df.to_dict(orient='records')

count = 1
for coach in coaches:
    queries = [
        f"{coach['name_search']} {coach['title_search']} baseball linkedin",
        f"{coach['name_search']} {coach['title_search']} {coach['Institute_search']} baseball linkedin",
    ]
    searchcount = ""
    print("\n=================================================\n")
    print(f"Current: {count}, Coach: {coach['name_search']} | {coach['title_search']} | {coach['Institute_search']}")
    
    pyautogui.click(50, 20, duration=0.1)
    pyperclip.copy(coach['Website'])
    time.sleep(0.1)
    pyautogui.hotkey('ctrl', 'l')
    pyautogui.hotkey('ctrl', 'v')
    pyautogui.press('enter')
    for query in queries:
        # pyautogui.click(50, 20, duration=0.1)
        pyperclip.copy(query)
        time.sleep(0.1)
        pyautogui.hotkey('ctrl', 't')
        pyautogui.hotkey('ctrl', 'l')
        pyautogui.hotkey('ctrl', 'v')
        pyautogui.press('enter')
    searchcount = input(f"(stop) for end, Enter for next coach: ")
    if searchcount  == "stop":
        break

    count += 1


# driver.quit()

# df = pd.DataFrame(coaches)

# excel_file_path = f'output-coaches.xlsx'

# df.to_excel(excel_file_path, index=False)

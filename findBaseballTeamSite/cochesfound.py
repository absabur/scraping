from selenium import webdriver
from selenium.webdriver.chrome.service import Service
service_obj=Service(r"c:\chromedriver.exe")
driver=webdriver.Chrome(service=service_obj)

import pandas as pd

excel_file_path = 'website.xlsx'
df = pd.read_excel(excel_file_path)
employees = df.to_dict(orient='records')

count = 1

for employee in employees:
    print("\n=====================================\n")
    try:
        print(f"current: {count}.")
        driver.get(employee['website'])
        print("------------------------")
        print(employee['institute'])
        print("------------------------")
        val = input("(e) for exit, (no) for remove website, Number of Coaches: ")
        if val  == "e":
            break
        if val == "no":
            employee['website'] = ""
            continue
        employee['number'] = val
    except:
        print("No website found.")
    count += 1

driver.quit()

df = pd.DataFrame(employees)
excel_file_path = f'website4.xlsx'
df.to_excel(excel_file_path, index=False)

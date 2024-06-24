from selenium import webdriver
from selenium.webdriver.chrome.service import Service
service_obj=Service(r"c:\chromedriver.exe")
driver=webdriver.Chrome(service=service_obj)
from selenium.webdriver.common.by import By
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

excel_file_path = 'edu.xlsx'

df = pd.read_excel(excel_file_path)

persons = df.to_dict(orient='records')

count = 1

driver.get('https://www.linkedin.com/home')
# mail="mdsabbirhossain6565@gmail.com"
# password="#######$%234ERfgh"
# driver.find_element(By.XPATH, "//input[@type='text']").send_keys(mail)
# driver.find_element(By.XPATH, "//input[@type='password']").send_keys(password)
# driver.find_element(By.XPATH, "//button[@type='submit']").click()

for employee in persons:
    val = input(f"current: {count}, Press Enter for next (exit): ")
    if val  == "exit":
        break
    try:
        driver.get(f"{employee['linkedin']}/details/education/")

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//main//ul'))
        )

        section = driver.find_elements(By.XPATH, '//main//section//ul//li//a//span[@aria-hidden="true"]')
        
        for i in range(0, len(section), 3):
            if i >= 12:
                break
            employee[f"Institute{i//3 + 1}"] = section[i].text if i < len(section) else ""
            employee[f"Education{i//3 + 1}"] = section[i + 1].text if i + 1 < len(section) else ""
            employee[f"Duration{i//3 + 1}"] = section[i + 2].text if i + 2 < len(section) else ""
           
    except Exception as e:
        print(f"An error occurred for {employee['linkedin']}: {e}")
    count += 1


driver.quit()

df = pd.DataFrame(persons)

person_path = f'edupersons.xlsx'

df.to_excel(person_path, index=False)

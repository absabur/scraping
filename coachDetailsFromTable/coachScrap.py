from selenium import webdriver


# options = webdriver.ChromeOptions()
# options.debugger_address = "127.0.0.1:9222"
# driver = webdriver.Chrome(options=options)



from selenium.webdriver.chrome.service import Service
service_obj=Service(r"c:\chromedriver.exe")
driver=webdriver.Chrome(service=service_obj)



from selenium.webdriver.common.by import By
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

# "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="C:\Users\absab\AppData\Local\Google\Chrome\User Data\Profile 1"
# %LOCALAPPDATA%
# chrome://version/
# https://chatgpt.com/c/dcbf62ec-e118-4299-a10c-4c182966cd8c

excel_file_path = 'website.xlsx'

df = pd.read_excel(excel_file_path)

coaches = df.to_dict(orient='records')

count = 529
collegeCount = 101

data = []
for coach in coaches:
    collegeCount += 1
    if collegeCount == 100:
        df = pd.DataFrame(data)
        person_path = f'Coaches1.xlsx'
        df.to_excel(person_path, index=False)
    if collegeCount == 200:
        df = pd.DataFrame(data)
        person_path = f'Coaches2.xlsx'
        df.to_excel(person_path, index=False)
    if collegeCount == 300:
        df = pd.DataFrame(data)
        person_path = f'Coaches3.xlsx'
        df.to_excel(person_path, index=False)

    print("\n================================\n")
    print(f"Current college: {collegeCount}) {coach['college']}")

    try:
        driver.get(coach['website'])
    except:
        count += 1
        print(f"Current coach: {count}")
        single = {}
        single['Institute'] = coach['college']
        data.append(single)
        continue
    try:
        WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.XPATH, '//table//th[@id="col-coaches-fullname"]'))
        )
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        tbodies = soup.find_all('tbody')
        for tbody in tbodies:
            rows = tbody.find_all('tr')
            for row in rows:
                count += 1
                print(f"Current: {count}")
                single = {}
                single['Institute'] = coach['college']
                single['Website'] = coach['website']
                try:
                    single["Name"] = row.find('th').text
                    title = row.find('th').find_next_sibling('td')
                    if title:
                        single["Title"] = title.text.strip()
                except:
                    pass

                try:
                    single["Email"] = row.find('a', href=lambda x: x and 'mailto:' in x).text
                except:
                    pass

                try:
                    single["Phone"] = row.find('a', href=lambda x: x and 'tel:' in x).text
                except:
                    pass
                data.append(single)
    except:
        for i in range(0, int(coach['number'])):
            count += 1
            print(f"Current: {count}")
            single = {}
            single['Institute'] = coach['college']
            single['Website'] = coach['website']
            data.append(single)
        print("Table not found.")
        

driver.quit()
df = pd.DataFrame(data)
person_path = f'allCoaches.xlsx'
df.to_excel(person_path, index=False)

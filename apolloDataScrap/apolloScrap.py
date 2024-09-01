from selenium import webdriver
options = webdriver.ChromeOptions()
options.debugger_address = "127.0.0.1:9222"
driver = webdriver.Chrome(options=options)
from selenium.webdriver.common.by import By
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import math
import time

# "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="C:\Users\absab\AppData\Local\Google\Chrome\User Data\Profile 1"
# %LOCALAPPDATA%
# chrome://version/
# https://chatgpt.com/c/dcbf62ec-e118-4299-a10c-4c182966cd8c


data = []
fileName = input("Enter file name: ")
lead = int(input("How many lead do you have: "))
page = math.ceil(lead/25)
print("====================")
print("Number of Pages: ",page)
print("====================")
for p in range(1, page+1):
    if p == 25 or p == 50 or p == 75:
        driver.refresh()
        time.sleep(4)
    driver.get(f"https://app.apollo.io/#/people?finderViewId=6674b20eecfedd000184539f&prospectImportIds[]=66c9a99b1aaa11019bb84abf&page={p}&prospectedByCurrentTeam[]=yes&sortByField=person_name.raw&sortAscending=true")
    time.sleep(1)
    print(f"Current Page: {p} | {page}")
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, './/table//tr[@data-cy="SelectableTableRow"]//a'))
    )
    if p == 1:
        time.sleep(5)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    rows = soup.find_all('tr')
    # print(f"{len(rows)-1} person")
    for row in rows:
        single = {}

        try:
            single["Name"] = row.find('div', class_="zp_xVJ20").find('a').text
        except:
            pass

        try:
            single["Email"] = row.find('a', class_="zp-link zp_OotKe zp_Iu6Pf").text
        except:
            pass

        try:
            single["PersonLinkedIn"] = row.find('a', href=lambda x: x and 'linkedin.com/in' in x)['href']
        except:
            pass
        
        try:
            single["Phone"] = row.find('a', class_="zp-link zp_OotKe zp_vc37T").text
        except:
            pass

        try:
            single["Apollo"] = f"https://app.apollo.io/{row.find('div', class_="zp_xVJ20").find('a')['href']}"
        except:
            pass

        try:
            single["CompanyName"] = row.find('div', class_="zp_J1j17").find('a').text
        except:
            pass

        try:
            single["CompanyApollo"] = f"https://app.apollo.io/{row.find('div', class_="zp_J1j17").find('a')['href']}"
        except:
            pass

        try:
            single["CompanyLinkedIn"] = row.find('a', href=lambda x: x and 'linkedin.com/company' in x)['href']
        except:
            pass
        
        try:
            single["Twitter"] = row.find('a', href=lambda x: x and 'twitter.com' in x)['href']
        except:
            pass
        
        try:
            single["Facebook"] = row.find('a', href=lambda x: x and 'facebook.com' in x)['href']
        except:
            pass
            
        try:
            single["Website"] = row.find('a', href=lambda x: x and 'linkedin.com' not in x and 'facebook.com' not in x and 'twitter.com' not in x and '#/contacts/' not in x and '#/accounts/' not in x)['href']
        except:
            pass
        

        cells = row.find_all('span', class_='zp_Y6y8d')
        for idx, cell in enumerate(cells):
            single[f"key{idx + 1}"] = cell.text

        # Extracting keywords
        try:
            keyword_div = row.find('div', class_='zp_HlgrG zp_y8Gpn zp_uuO3B')
            keywords = " ".join([item.text for item in keyword_div.find_all('span')])
            single["Keywords"] = keywords
        except:
            pass

        # Extracting industries
        try:
            industry_div = row.find('div', class_='zp_paOF8')
            industries = " ".join([item.text for item in industry_div.find_all('span')])
            single["Industries"] = industries
        except:
            pass

        if len(single) == 0:
            pass
        else:
            data.append(single)
        
driver.quit()

df = pd.DataFrame(data)

person_path = f'{fileName}({lead}).xlsx'

df.to_excel(person_path, index=False)

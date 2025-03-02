from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

# Connect to an existing Chrome instance with debugging enabled
options = webdriver.ChromeOptions()
options.debugger_address = "127.0.0.1:9222"
driver = webdriver.Chrome(options=options)

# Message content to send
message = """
Welcome to our platform, offering a vast library of 21,000 films and TV shows for streaming and AI.

. We use AI technologies to enhance the cinematic experience. Our key offerings include dubbing in 60 languages, upscaling SD content to HD, colorization and upscaling packages, $299  each., documentary creation, white label sites from $5000, 
AI advisory services, and investment opportunities in AI for film. For more information, contact Smuel Kleinman at Doctorofdance@gmail.com or +13108958315. 
We buy/license library films. 

Full doc : https://docs.google.com/file/d/1rvLc7rd2RZRU6bz_vS1N_J1GMZUfPhhZ/edit?usp=docslist_api&filetype=msword 
"""

# Find all the card elements on the page
results = driver.find_elements(By.XPATH, '//div[@class="card"]')
# sheets = []

count = 1
try:
    for result in results:
        # content = dict()
        if count in range(691):
            count += 1
            continue
        if count == 1325:
            break

        name = result.find_element(By.XPATH, './/div[@class="profiledetails"]//h4')
        messageIcon = result.find_element(By.XPATH, './/div[@class="btn-chat"]//img')
        try:
            messageIcon.click()
        except:
            print("Failed to click message icon")
        modal = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, '//div[@class="modal-content"]'))
        )
        textArea = WebDriverWait(modal, 20).until(
            EC.visibility_of_element_located((By.XPATH, './/textarea[@class="form-control"]'))
        )
        textArea.send_keys(message)
        sendButton = WebDriverWait(modal, 10).until(
            EC.element_to_be_clickable((By.XPATH, './/button[@id="send"]'))
        )
        sendButton.click()
        WebDriverWait(driver, 20).until(
            EC.invisibility_of_element((By.XPATH, './/div[@class="modal-content"]'))
        )
        

        # try:
        #     # Wait until the toast element is present in the DOM
        #     toast_element = WebDriverWait(driver, 10).until(
        #         EC.presence_of_element_located((By.XPATH, './/div[@id="toast"]'))
        #     )

        #     # Get the computed style of the display property
        #     display_value = driver.execute_script("return window.getComputedStyle(arguments[0]).display;", toast_element)
            
        #     if display_value == "block":
        #         content['name'] = name.text
        #         content['status'] = "sent"
        #     else:
        #         content['name'] = name.text
        #         content['status'] = "failed"
        #     toast_element.find_element(By.XPATH, './/a[@class="close"]').click()
        # except Exception as e:
        #     content['name'] = name.text
        #     content['status'] = "failed"
            
        # sheets.append(content)
        
        print(f"({count}): {name.text}")
        count += 1
        time.sleep(2)
except Exception as e:
    print(e)


# df = pd.DataFrame(sheets)

# # Save to an Excel file
# df.to_excel(f"status{count}.xlsx", index=False)

# print("Excel file created successfully!")
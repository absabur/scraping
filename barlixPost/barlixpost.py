from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
import time
import random
import logging
from webdriver_manager.chrome import ChromeDriverManager

# Set up logging
logging.basicConfig(level=logging.INFO)

# Automatically download the correct ChromeDriver version
service_obj = Service(ChromeDriverManager().install())
options = webdriver.ChromeOptions()
# Uncomment the next line to run in headless mode
# options.add_argument("--headless")
options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
)

driver = webdriver.Chrome(service=service_obj, options=options)


def postToBarlix(username, password, text, path, page, pageText, pagePath):
    try:
        logging.info(f"Attempting to post for user: {username}")
        driver.get("https://www.barlix.com/logout/")
        driver.get("https://www.barlix.com/welcome/")

        # Log in to the website
        email_input = driver.find_element(By.XPATH, '//input[@id="username"]')
        password_input = driver.find_element(By.XPATH, '//input[@id="password"]')

        email_input.send_keys(username)
        password_input.send_keys(password)

        driver.find_element(
            By.XPATH, '//button[@type="submit"][text()="Login"]'
        ).click()

        if text != "" or path != "":
            # Wait for the post box to be visible
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//textarea[@name="postText"]')
                )
            )

            # Enter text into the "What's on your mind?" box
            textarea = driver.find_element(By.XPATH, '//textarea[@name="postText"]')
            textarea.click()
            driver.execute_script("arguments[0].value = arguments[1];", textarea, text)

            if path == "":
                driver.find_element(
                    By.XPATH, '//div[@onclick="Wo_ShowColors()"]'
                ).click()
                colors = driver.find_elements(
                    By.XPATH, '//div[@class="all_colors_style"]'
                )
                randomNumber = random.randint(0, len(colors) - 1)
                colors[randomNumber].click()

            # Find the file input and upload an image
            if path:
                file_input = driver.find_element(
                    By.XPATH, '//input[@type="file" and @id="publisher-photos"]'
                )
                file_input.send_keys(path)

                # Wait until the image is uploaded
                WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located(
                        (By.XPATH, '//span[@id="image_to_0"]//img')
                    )
                )
                logging.info("Image uploaded successfully")

            # Click the Post button
            time.sleep(0.7)
            post_button = driver.find_element(
                By.XPATH, '//button[@id="publisher-button"]'
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", post_button)
            post_button.click()

            logging.info(f"Post successful for user: {username}")

        if pageText != "" or pagePath != "":
            if text != "" or path != "":
                # input("next=============================")
                time.sleep(150)
            # Wait for the post box to be visible
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//textarea[@name="postText"]')
                )
            )
            driver.get(page)
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//textarea[@name="postText"]')
                )
            )

            # Enter text into the "What's on your mind?" box
            textarea = driver.find_element(By.XPATH, '//textarea[@name="postText"]')
            textarea.click()
            driver.execute_script(
                "arguments[0].value = arguments[1];", textarea, pageText
            )

            if pagePath == "":
                driver.find_element(
                    By.XPATH, '//div[@onclick="Wo_ShowColors()"]'
                ).click()
                colors = driver.find_elements(
                    By.XPATH, '//div[@class="all_colors_style"]'
                )
                randomNumber = random.randint(0, len(colors) - 1)
                colors[randomNumber].click()

            # Find the file input and upload an image
            if pagePath:
                file_input = driver.find_element(
                    By.XPATH, '//input[@type="file" and @id="publisher-photos"]'
                )
                file_input.send_keys(pagePath)

                # Wait until the image is uploaded
                WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located(
                        (By.XPATH, '//span[@id="image_to_0"]//img')
                    )
                )
                logging.info("Image uploaded successfully")

            # Click the Post button
            time.sleep(0.7)
            post_button = driver.find_element(
                By.XPATH, '//button[@id="publisher-button"]'
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", post_button)
            post_button.click()

            logging.info(f"Post successful for user: {username}")

    except Exception as e:
        logging.error(f"An error occurred for user: {username} - {e}")
        driver.save_screenshot(f"error_screenshot_{username}.png")

    # input("next=============================")
    time.sleep(150)


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import logging


usernamePasswords = [
    {
        "username": "tahmidAhmed",
        "password": "q1w2e3r4",
        "text": "",
        "image": "",
        "page": "https://www.barlix.com/InternationalAffairs",
        "pageText": "",
        "pagePath": "",
    },
    {
        "username": "SajidIslam",
        "password": "q1w2e3r4",
        "text": "",
        "image": "",
        "page": "https://www.barlix.com/UnknownFacts",
        "pageText": "",
        "pagePath": "",
    },
    {
        "username": "MehediHasan",
        "password": "q1w2e3r4",
        "text": "",
        "image": "",
        "page": "https://www.barlix.com/ScienceAndTechnology",
        "pageText": "",
        "pagePath": "",
    },
    {
        "username": "FarhanIslam",
        "password": "q1w2e3r4",
        "text": "",
        "image": "",
        "page": "https://www.barlix.com/BangladeshAffairs",
        "pageText": "",
        "pagePath": "",
    },
    {
        "username": "RafsanMahmud",
        "password": "q1w2e3r4",
        "text": "",
        "image": "",
        "page": "https://www.barlix.com/AstronomyAdventures",
        "pageText": "",
        "pagePath": "",
    },
    {
        "username": "TanvirAlam",
        "password": "q1w2e3r4",
        "text": "",
        "image": "",
        "page": "",
        "pageText": "",
        "pagePath": "",
    },
    {
        "username": "ZareenFarhana",
        "password": "q1w2e3r4",
        "text": "",
        "image": "",
        "page": "",
        "pageText": "",
        "pagePath": "",
    },
    {
        "username": "AyanChowdhury",
        "password": "q1w2e3r4",
        "text": "",
        "image": "",
        "page": "",
        "pageText": "",
        "pagePath": "",
    },
]

# Open the website and post for each account
for account in usernamePasswords:
    if (
        account["text"] != ""
        or account["image"] != ""
        or account["pageText"] != ""
        or account["pagePath"]
    ):
        postToBarlix(
            account["username"],
            account["password"],
            account["text"],
            account["image"],
            account["page"],
            account["pageText"],
            account["pagePath"],
        )


# Wait for user input before closing
input("Press Enter to exit...")

driver.get("https://www.barlix.com/logout/")
driver.quit()

logging.info("All posts completed and browser closed.")


reset = [
    {
        "username": "tahmidAhmed",
        "password": "q1w2e3r4",
        "text": "",
        "image": "",
        "page": "https://www.barlix.com/InternationalAffairs",
        "pageText": "",
        "pagePath": "",
    },
    {
        "username": "SajidIslam",
        "password": "q1w2e3r4",
        "text": "",
        "image": "",
        "page": "https://www.barlix.com/UnknownFacts",
        "pageText": "",
        "pagePath": "",
    },
    {
        "username": "MehediHasan",
        "password": "q1w2e3r4",
        "text": "",
        "image": "",
        "page": "https://www.barlix.com/ScienceAndTechnology",
        "pageText": "",
        "pagePath": "",
    },
    {
        "username": "FarhanIslam",
        "password": "q1w2e3r4",
        "text": "",
        "image": "",
        "page": "https://www.barlix.com/BangladeshAffairs",
        "pageText": "",
        "pagePath": "",
    },
    {
        "username": "RafsanMahmud",
        "password": "q1w2e3r4",
        "text": "",
        "image": "",
        "page": "https://www.barlix.com/AstronomyAdventures",
        "pageText": "",
        "pagePath": "",
    },
    {
        "username": "TanvirAlam",
        "password": "q1w2e3r4",
        "text": "",
        "image": "",
        "page": "",
        "pageText": "",
        "pagePath": "",
    },
    {
        "username": "ZareenFarhana",
        "password": "q1w2e3r4",
        "text": "",
        "image": "",
        "page": "",
        "pageText": "",
        "pagePath": "",
    },
    {
        "username": "AyanChowdhury",
        "password": "q1w2e3r4",
        "text": "",
        "image": "",
        "page": "",
        "pageText": "",
        "pagePath": "",
    },
]

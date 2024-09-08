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

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import logging


def auto_like(username, password, gender):
    logging.info(f"Attempting to create user {username}")

    try:
        driver.get("https://www.barlix.com/register/")

        username_input = driver.find_element(By.XPATH, '//input[@id="username"]')
        email_input = driver.find_element(By.XPATH, '//input[@id="email"]')
        password_input = driver.find_element(By.XPATH, '//input[@id="password"]')
        cpassword_input = driver.find_element(
            By.XPATH, '//input[@id="confirm_password"]'
        )
        gender_input = driver.find_element(By.XPATH, '//select[@id="gender"]')
        accept_terms = driver.find_element(By.XPATH, '//input[@id="accept_terms"]')

        username_input.send_keys(username)
        email_input.send_keys(f"{username}@gmail.com")
        password_input.send_keys(password)
        cpassword_input.send_keys(password)
        gender_input.send_keys(gender)
        driver.execute_script("arguments[0].click();", accept_terms)

        driver.find_element(
            By.XPATH, '//button[@type="submit"][@id="sign_submit"]'
        ).click()
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//textarea[@name="postText"]'))
        )
        print("user created successfully")
        driver.get("https://www.barlix.com/logout/")
    except Exception as e:
        logging.error(f"Failed to create user {username}: {e}")


usernamePasswords = [
    {"username": "Abdullah", "password": "q1w2e3r4", "gender": "male"},
]

# Open the website and post for each account
for account in usernamePasswords:
    auto_like(account["username"], account["password"], account["gender"])

# Wait for user input before closing
input("Press Enter to exit...")

driver.get("https://www.barlix.com/logout/")
driver.quit()

logging.info("All posts completed and browser closed.")

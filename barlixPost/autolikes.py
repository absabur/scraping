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


last_post = 483


def auto_like(username, password, last_post):
    logging.info(f"Attempting to post for user: {username}")

    driver.get("https://www.barlix.com/logout/")
    driver.get("https://www.barlix.com/welcome/")

    email_input = driver.find_element(By.XPATH, '//input[@id="username"]')
    password_input = driver.find_element(By.XPATH, '//input[@id="password"]')

    email_input.send_keys(username)
    password_input.send_keys(password)

    driver.find_element(By.XPATH, '//button[@type="submit"][text()="Login"]').click()

    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, '//textarea[@name="postText"]'))
    )

    #================ page like code ===============
    
    # driver.get("https://www.barlix.com/suggested-pages")
    # time.sleep(1)
    # likes = driver.find_elements(By.XPATH, '//button[@id="wo_useract_btn"]')
    # time.sleep(1)
    # for like in likes:
    #     like.click()
    # driver.get("https://www.barlix.com/suggested-pages")
    # return
    
    # =============== end ==================

    SCROLL_PAUSE_TIME = 5

    last_height = driver.execute_script("return document.body.scrollHeight")

    processed_posts = []
    stop = False
    while True:
        if stop:
            break

        elements = driver.find_elements(By.XPATH, '//ul[@style=" right: auto; "]')
        for element in elements:
            driver.execute_script("arguments[0].style.display = 'block';", element)

        for box in elements:
            post_id = box.get_attribute("data-id")
            ignore = [
                f"{last_post+3}",
                f"{last_post+7}",
                f"{last_post+9}",
                f"{last_post+13}",
                f"{last_post+16}",
                f"{last_post+20}",
                f"{last_post+22}",
                f"{last_post+25}",
                f"{last_post+29}",
                f"{last_post+32}",
                f"{last_post+34}",
                f"{last_post+37}",
                f"{last_post+40}",
            ]
            if random.randint(0, 4) == 2 and post_id not in ignore:
                print(f"{post_id} -> Post is not liked.")
                continue

            try:
                reacts = box.find_elements(By.XPATH, ".//li")
                index = [0, 1, 0, 1, 3, 0, 1, 3, 0, 1, 3, 4]
                rand = random.randint(0, 11)
                element = reacts[index[rand]]
                driver.execute_script("arguments[0].scrollIntoView(true);", box)
                driver.execute_script("arguments[0].style.display = 'block';", box)
                # time.sleep(0.2)
                driver.execute_script("arguments[0].click();", element)
                processed_posts.append(post_id)
                print(f"{post_id} -> Post liked successfully.")
            except Exception as e:
                print(f"Failed to like post: =====")

            if int(post_id) <= last_post:
                stop = True
                break
            if post_id in processed_posts:
                continue

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # if len(processed_posts) != 0:
        #     try:
        #         last_element_str = processed_posts[-1]
        #         last_element_int = int(last_element_str)
        #         result = last_element_int - 1
        #         WebDriverWait(driver, 20).until(
        #             EC.presence_of_element_located(
        #                 (By.XPATH, f'//span[@data-id="{result}"]')
        #             )
        #         )
        #     except Exception as e:
        #         print(f"Failed to find the last post: =====")
        # else:
        #     time.sleep(SCROLL_PAUSE_TIME)

        time.sleep(SCROLL_PAUSE_TIME)

        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    logging.info("Auto-like process completed.")


usernamePasswords = [
    {
        "username": "tahmidAhmed",
        "password": "q1w2e3r4",
    },
    {
        "username": "SajidIslam",
        "password": "q1w2e3r4",
    },
    {
        "username": "MehediHasan",
        "password": "q1w2e3r4",
    },
    {
        "username": "FarhanIslam",
        "password": "q1w2e3r4",
    },
    {
        "username": "RafsanMahmud",
        "password": "q1w2e3r4",
    },
    {
        "username": "TanvirAlam",
        "password": "q1w2e3r4",
    },
    {
        "username": "ZareenFarhana",
        "password": "q1w2e3r4",
    },
    {
        "username": "AyanChowdhury",
        "password": "q1w2e3r4",
    },
    {
        "username": "aaaaa",
        "password": "aaaaaa",
    },
    {
        "username": "bbbbb",
        "password": "bbbbbb",
    },
    {
        "username": "ccccc",
        "password": "cccccc",
    },
    {
        "username": "ddddd",
        "password": "dddddd",
    },
    {
        "username": "eeeee",
        "password": "eeeeee",
    },
    {
        "username": "fffff",
        "password": "ffffff",
    },
    {
        "username": "ggggg",
        "password": "gggggg",
    },
    {
        "username": "hhhhh",
        "password": "hhhhhh",
    },
    {
        "username": "iiiii",
        "password": "iiiiii",
    },
    {
        "username": "jjjjj",
        "password": "jjjjjj",
    },
    {"username": "AyeshaRahman", "password": "q1w2e3r4"},
    {"username": "ImranHossain", "password": "q1w2e3r4"},
    {"username": "ZaraAhmed", "password": "q1w2e3r4"},
    {"username": "TariqAnwar", "password": "q1w2e3r4"},
    {"username": "NadiaKarim", "password": "q1w2e3r4"},
    {"username": "ArifChowdhury", "password": "q1w2e3r4"},
    {"username": "SabinaSultana", "password": "q1w2e3r4"},
    {"username": "FarhanMahmud", "password": "q1w2e3r4"},
    {"username": "MehnazIslam", "password": "q1w2e3r4"},
    {"username": "RinaBegum", "password": "q1w2e3r4", "gender": "female"},
    {"username": "AnisurRahman", "password": "q1w2e3r4", "gender": "male"},
    {"username": "ShakilAhmed", "password": "q1w2e3r4", "gender": "male"},
    {"username": "RahulChowdhury", "password": "q1w2e3r4", "gender": "male"},
    {"username": "SaraKhan", "password": "q1w2e3r4", "gender": "female"},
    {"username": "AmitSingh", "password": "q1w2e3r4", "gender": "male"},
    {"username": "NinaJain", "password": "q1w2e3r4", "gender": "female"},
    {
        "username": "ShafiqRahman",
        "password": "q1w2e3r4",
    },
    {
        "username": "RaheelSiddiqui",
        "password": "q1w2e3r4",
    },
    {
        "username": "NusratJahan",
        "password": "q1w2e3r4",
    },
    {
        "username": "OmarFaruq",
        "password": "q1w2e3r4",
    },
    {
        "username": "TamannaAkter",
        "password": "q1w2e3r4",
    },
    {
        "username": "FahimHasan",
        "password": "q1w2e3r4",
    },
    {
        "username": "LailaNoor",
        "password": "q1w2e3r4",
    },
    {
        "username": "JamilKhan",
        "password": "q1w2e3r4",
    },
    {"username": "RaviPatel", "password": "q1w2e3r4", "gender": "male"},
    {"username": "PoojaVerma", "password": "q1w2e3r4", "gender": "female"},
    {"username": "VikramSharma", "password": "q1w2e3r4", "gender": "male"},
    {"username": "AnitaDesai", "password": "q1w2e3r4", "gender": "female"},
    {"username": "MahmudHassan", "password": "q1w2e3r4", "gender": "male"},
    {"username": "ShabnamAkter", "password": "q1w2e3r4", "gender": "female"},
    {"username": "NafisAhmed", "password": "q1w2e3r4", "gender": "male"},
    {"username": "TaslimaBegum", "password": "q1w2e3r4", "gender": "female"},
    {"username": "RakibulIslam", "password": "q1w2e3r4", "gender": "male"},
    {"username": "SumaiyaJahan", "password": "q1w2e3r4", "gender": "female"},
    {"username": "FahimRahman", "password": "q1w2e3r4", "gender": "male"},
    {"username": "MalihaIslam", "password": "q1w2e3r4", "gender": "female"},
    {"username": "RashedKhan", "password": "q1w2e3r4", "gender": "male"},
    {"username": "SadiaRahman", "password": "q1w2e3r4", "gender": "female"},
    {"username": "AlaminMiah", "password": "q1w2e3r4", "gender": "male"},
    {"username": "FarzanaAkter", "password": "q1w2e3r4", "gender": "female"},
    {"username": "ShahinAlam", "password": "q1w2e3r4", "gender": "male"},
    {"username": "RubinaSultana", "password": "q1w2e3r4", "gender": "female"},
    {"username": "FerdousAhmed", "password": "q1w2e3r4", "gender": "male"},
    {"username": "MarufaIslam", "password": "q1w2e3r4", "gender": "female"},
    {"username": "AsifIqbal", "password": "q1w2e3r4", "gender": "male"},
    {"username": "LamiaKhanum", "password": "q1w2e3r4", "gender": "female"},
    {"username": "TamimKhan", "password": "q1w2e3r4", "gender": "male"},
    {"username": "MasudRahman", "password": "q1w2e3r4", "gender": "male"},
    {"username": "Hasanuzzaman", "password": "q1w2e3r4", "gender": "male"},
    {"username": "HamzaChowdhory", "password": "q1w2e3r4", "gender": "male"},
    {"username": "TowhidHridoy", "password": "q1w2e3r4", "gender": "male"},
]

# Open the website and post for each account
for account in usernamePasswords:
    auto_like(account["username"], account["password"], last_post)

# Wait for user input before closing
input("Press Enter to exit...")

driver.get("https://www.barlix.com/logout/")
driver.quit()

logging.info("All posts completed and browser closed.")

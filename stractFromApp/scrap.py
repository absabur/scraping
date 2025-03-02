import pyautogui, time, pyperclip
import mss, os, re
import base64
from io import BytesIO
from PIL import Image
import pandas as pd

all_data = []

def sanitize_filename(filename):
    # Replace invalid characters with an underscore and remove spaces
    filename = re.sub(r'[\\/*?:"<>|]', "_", filename)  # Replace invalid characters with an underscore
    filename = filename.replace(" ", "_")  # Replace spaces with underscores
    filename = filename.replace("\r", "")  # Remove carriage return characters
    filename = filename.replace("\n", "")  # Remove newline characters
    return filename

def copyText():
    data = dict()
    time.sleep(2)
    pyautogui.hotkey('ctrl', '.')
    time.sleep(0.5)

    start_x, start_y = 2022, 280
    end_x, end_y = 2450, 421

    pyautogui.moveTo(start_x, start_y)
    pyautogui.mouseDown()
    pyautogui.moveTo(end_x, end_y)
    pyautogui.mouseUp()
    time.sleep(0.5)

    clipboard_value = pyperclip.paste()
    
    key_to_find = "namePostCompany"
    value_to_find = clipboard_value

    # Find the dictionary with the matching value
    result = next((item for item in all_data if item.get(key_to_find) == value_to_find), None)

    if result:
        print(f"Person number: {len(all_data)}")
        print(all_data[-1]['namePostCompany'])
        input("scrolled to top: ")
    else:
        data['namePostCompany'] = clipboard_value
        data['Category'] = "Attendee Recommendations"

        all_data.append(data)
        
        pyautogui.click(2174, 959)
        time.sleep(0.5)

i = 1
while i < 350:
    pyautogui.click(2222, 175)
    copyText()
    pyautogui.click(2222, 250)
    copyText()
    pyautogui.click(2222, 325)
    copyText()
    pyautogui.click(2222, 400)
    copyText()
    pyautogui.click(2222, 480)
    copyText()
    pyautogui.click(2222, 560)
    copyText()
    pyautogui.click(2222, 630)
    copyText()
    pyautogui.click(2222, 710)
    copyText()
    pyautogui.click(2222, 790)
    copyText()
    pyautogui.click(2222, 870)
    copyText()
    print(i*10, "finished")

    pyautogui.moveTo(2222, 870)
    pyautogui.mouseDown()
    pyautogui.moveTo(2222, 91)
    pyautogui.mouseUp()
    
    
    df = pd.DataFrame(all_data)
    df.to_excel(f"file-{i*10}.xlsx", index=False)
    
    time.sleep(2)
    
    if i % 10 == 0:
        if (input("enter (e) for exit: ")) == "e":
            break
        
    i += 1
    
df = pd.DataFrame(all_data)
df.to_excel("all_data.xlsx", index=False)



# for i in range(1,105):
#     pyautogui.moveTo(2222, 870)
#     pyautogui.mouseDown()
#     pyautogui.moveTo(2222, 88)
#     pyautogui.mouseUp()








    
# image_folder = "images"
# os.makedirs(image_folder, exist_ok=True)

# region = {"top": 100, "left": 2156, "width": 180, "height": 190}

# with mss.mss() as sct:
#     screenshot = sct.grab(region)

# image = Image.frombytes("RGB", screenshot.size, screenshot.rgb)

# sanitized_clipboard_value = sanitize_filename(clipboard_value)
# image_filename = os.path.join(image_folder, f"{sanitized_clipboard_value}.png")

# image.save(image_filename, "PNG")

# data['Image_Path'] = image_filename

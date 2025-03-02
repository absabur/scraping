from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import re
from fuzzywuzzy import process
import pandas as pd

# Function to get website using Selenium



def get_website(company_name, driver):
    query = f"{company_name}"
    try:
        driver.get(f'https://www.google.com/search?q={query}')
        # WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'h3')))
        soup = BeautifulSoup(driver.page_source, 'html.parser')


        # Check for common reCAPTCHA elements
        is_recaptcha_present = False

        # Check for v2 reCAPTCHA elements
        recaptcha_v2 = soup.find_all(class_='g-recaptcha')
        if recaptcha_v2:
            is_recaptcha_present = True

        # Check for v3 reCAPTCHA elements (usually involves an API script)
        recaptcha_v3 = soup.find_all('script', src=lambda src: src and 'recaptcha' in src)
        if recaptcha_v3:
            is_recaptcha_present = True

        # Check for the reCAPTCHA checkbox
        recaptcha_checkbox = soup.find_all(class_='recaptcha-checkbox-border')
        if recaptcha_checkbox:
            is_recaptcha_present = True

        # Check for other common reCAPTCHA elements
        recaptcha_elements = soup.find_all(class_='recaptcha')
        if recaptcha_elements:
            is_recaptcha_present = True

        val = ""
        if is_recaptcha_present:
            print("=================================================")
            val = input(f"Press Enter for next (e): ")

        if val  == "e":
            return {"end": True}

        website_url = ""
        matchpercent = ""
        phone = ""
        address= ""
        justDial = ""
        facebook_page= ""
        facebook_url = ""
        linkedin_url = ""
        twitter_url = ""
        instagram_url = ""
        youtube_url = ""


        try:
            url_elem = soup.find_all('a', class_='ab_button')
            for url in url_elem:
                if url.text == "Website" or url.text == "ওয়েবসাইট":
                    website_url = url.get('href')
                    matchpercent = "From map"
                    break
            url_elem = soup.find_all('a', class_='n1obkb')
            for url in url_elem:
                if url.text == "Website" or url.text == "ওয়েবসাইট":
                    website_url = url.get('href')
                    matchpercent = "From - map"
                    break

            urls = soup.find_all('a', attrs={'jsname': 'UWckNb'})
            texts = [url.find('span', class_='VuuXrf').text for url in urls if url.find('span', class_='VuuXrf')]
            match = process.extractOne(company_name, texts, score_cutoff=70)
            if match and matchpercent == "":
                for url in urls:
                    if match[0] == url.find('span', class_='VuuXrf').text:
                        website_url = url.get('href')
                        matchpercent = match[1]
                        break
                    
            try:
                justdial_urls = [link['href'] for link in urls if 'justdial.com' in link.get('href', '')]
                justDial = justdial_urls[0]
            except:
                justDial = ""
                
        except Exception as e:
            website_url = ""
            
        try:
            a_tag = soup.find('a', {'data-dtype': 'd3ph'})
            if a_tag:
                text = a_tag.get_text(strip=True)
                phone = text.replace('+', '')  # Remove the '+' symbol
        except:
            phone = ""
            
        try:
            divs = soup.find_all('div', attrs={'jsname': 'xQjRM'})
            for div in divs:
                span = div.find('span', class_='z3HNkc')
                if span:
                    url = div.find('a', attrs={'jsname': 'UWckNb'}).get('href')
                    if "facebook.com" in url:
                        facebook_page = url
                        break
        except:
            pass
            
            
        try:
            address_tag = soup.find('span', class_="LrzXr")
            if address_tag:
                text = address_tag.get_text(strip=True)
                address = text
        except:
            address = ""
            
        try:
            div = soup.find_all('div', class_='OOijTb P6Tjc gDQYEd Dy8CGd')

            for d in div:
                links = d.find_all('a')
                for link in links:
                    href = link.get('href', '')
                    if href:
                        # Step 4: Check if the URL belongs to one of the specified domains
                        if 'facebook.com' in href:
                            facebook_url = href
                        elif 'linkedin.com' in href:
                            linkedin_url = href
                        elif 'twitter.com' in href:
                            twitter_url = href
                        elif 'instagram.com' in href:
                            instagram_url = href
                        elif 'youtube.com' in href:
                            youtube_url = href
        except:
            pass

        return {
            "url": website_url,
            "phone": phone,
            "address": address,
            "facebook_page": facebook_page,
            "justDial": justDial,
            "facebook_url": facebook_url,
            "linkedin_url": linkedin_url,
            "twitter_url": twitter_url,
            "instagram_url": instagram_url,
            "youtube_url": youtube_url,
            "match": matchpercent,
            "end": False
        }
            
    except Exception as e:
        print(f"Error searching for {company_name}: {str(e)}")
    return {"end": True}

# Initialize Selenium WebDriver (Chrome in this example)

options = webdriver.ChromeOptions()
options.debugger_address = "127.0.0.1:9222"
driver = webdriver.Chrome(options=options)
print("ready")

# Specify your Excel file path
excel_file_path = 'dynamic_output.xlsx'

# Read Excel file into a Pandas DataFrame
df = pd.read_excel(excel_file_path, engine='openpyxl')

# Convert DataFrame to a list of dictionaries
companies = df.to_dict(orient='records')

# Iterate over each company name in the Excel sheet
count = 1
for row in companies:
    print(f"searching: {count}")
    # if count >= 20:
    #     break
    if row['school'] and row['address']:
        website = get_website(f"{row['school']} {row['address']}", driver)
        row['web_from_map'] = website['url']
        row['match_from_map'] = website['match']
        row['phone_from_map'] = website['phone']
        row['address_from_map'] = website['address']
        row['facebook_profile_map'] = website['facebook_url']
        row['justDial'] = website['justDial']
        row['facebook_page'] = website['facebook_page']
        # row['linkedin_url_map'] = website['linkedin_url']
        # row['twitter_url_map'] = website['twitter_url']
        # row['instagram_url_map'] = website['instagram_url']
        # row['youtube_url_map'] = website['youtube_url']
    elif row['school']:
        website = get_website(f"{row['school']}", driver)
        row['web_from_map'] = website['url']
        row['match_from_map'] = website['match']
        row['phone_from_map'] = website['phone']
        row['address_from_map'] = website['address']
        row['facebook_profile_map'] = website['facebook_url']
        row['justDial'] = website['justDial']
        row['facebook_page'] = website['facebook_page']
        # row['linkedin_url_map'] = website['linkedin_url']
        # row['twitter_url_map'] = website['twitter_url']
        # row['instagram_url_map'] = website['instagram_url']
        # row['youtube_url_map'] = website['youtube_url']
        
    count += 1

# Save the updated DataFrame to a new Excel file
df = pd.DataFrame(companies)
output_excel_path = 'output_companies_with_websites12.xlsx'
df.to_excel(output_excel_path, index=False)

# Close the WebDriver session
driver.quit()


print(f"Updated data saved to {output_excel_path}")

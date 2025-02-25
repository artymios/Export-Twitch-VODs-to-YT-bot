import time, os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = webdriver.ChromeOptions()
# options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument("--log-level=3")

#### MODIFY THE VALUES BELOW ####

# In Chrome, open Chrome://version and copy the Profile Path (remove "Default" from the end) and the Executable Path, and paste them below and double all backslashes
options.add_argument("user-data-dir=C:\\Users\\User\\AppData\\Local\\Google\\Chrome for Testing\\User Data")
options.binary_location = "D:\\Other code\\chrome-win64\\chrome.exe"
# type your twitch username below, without the @
twitch_username = "imsoarty"

#### END OF MODIFY SECTION ####

# Function to save the last uploaded VOD title, page number, and preferences
def save_last_uploaded_vod(title, page, sort_from_oldest, skip_unpublished):
    with open("last_uploaded_vod.txt", "w", encoding="utf-8") as file:
        file.write(f"{title}\n{page}\n{sort_from_oldest}\n{skip_unpublished}")

# Function to read the last uploaded VOD title, page number, and preferences
def read_last_uploaded_vod():
    if os.path.exists("last_uploaded_vod.txt"):
        with open("last_uploaded_vod.txt", "r", encoding="utf-8") as file:
            lines = file.readlines()
            if len(lines) == 4:
                return lines[0].strip(), int(lines[1].strip()), lines[2].strip() == "True", lines[3].strip() == "True"
    return None, 1, None, None

# Ask the user if they would like to continue from the last time
continue_from_last_time = input("Would you like to continue from where you left off last time? (y/n, n if starting for the first time) ").lower() in ["y", "yes"]

if continue_from_last_time:
    # Read the last uploaded VOD title, page number, and preferences
    last_uploaded_vod, last_uploaded_page, sort_from_oldest, skip_unpublished = read_last_uploaded_vod()
    start_uploading = False if last_uploaded_vod else True
else:
    # Prompt the user for options if not continuing from the last time
    sort_from_oldest = True if input("Sort from oldest? (y/n) ").lower() in ["y", "yes"] else False
    skip_unpublished = True if input("Skip unpublished highlights? (y/n) ").lower() in ["y", "yes"] else False
    start_vod_title = input("Enter the full title of the VOD to start uploading from (leave empty to start from the beginning): ").strip()
    if start_vod_title:
        last_uploaded_vod = start_vod_title
        start_uploading = False
    else:
        last_uploaded_vod = None
        start_uploading = True
    last_uploaded_page = 1

service = Service(executable_path="chromedriver.exe")
bot = webdriver.Chrome(service=service, options=options)
wait = WebDriverWait(bot, 10)

bot.get(f"https://dashboard.twitch.tv/u/{twitch_username}/content/video-producer")
wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[6]/div/div/div[2]/div/div[3]/div[1]/button'))).click()

# Show only highlights
wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div[3]/div/div/div[2]/div/main/div/div[3]/div/div/div/div[2]/div[2]/div[3]/div/div/div/div/div/div[1]/div[1]/div[1]/div/div[2]/button'))).click()
wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[last()]/div/div/div/div/div[1]/div/div/div[4]/button'))).click()

# - Apply the saved sorting preference
if sort_from_oldest:
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div[3]/div/div/div[2]/div/main/div/div[3]/div/div/div/div[2]/div[2]/div[3]/div/div/div/div/div/div[1]/div[1]/div[3]/div/button'))).click()
    time.sleep(0.5)
    bot.find_element(By.XPATH, '/html/body/div[5]/div/div/div/div/div[1]/div/div/div[2]/button').click()

time.sleep(1) # give it a sec, let him cook

# - Navigate to the last uploaded page
current_page = 1
while current_page < last_uploaded_page:
    next_page_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div[3]/div/div/div[2]/div/main/div/div[3]/div/div/div/div[2]/div[2]/div[3]/div/div/div/div/div/div[1]/div[2]/div/button[2]')))
    next_page_button.click()
    current_page += 1
    time.sleep(2)

# - Export to youtube
vods_uploaded = 0
vod_upload_limit = 100
while vods_uploaded < vod_upload_limit:
    all_vods_on_page = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="root"]/div[3]/div/div/div[2]/div/main/div/div[3]/div/div/div/div[2]/div[2]/div[3]/div/div/div/div/div/div[2]/div[2]/*')))

    for i, vod in enumerate(all_vods_on_page):
        # Get the title of the current VOD
        vod_title = vod.find_element(By.XPATH, './/div/a/div/div[2]/div[1]/div/div/div[2]/div/div[2]/h5').text

        if not start_uploading:
            if vod_title == last_uploaded_vod:
                start_uploading = True
            continue

        if skip_unpublished:
            publication_status = vod.find_element(By.XPATH, './/div/a/div/div[2]/div[1]/div/div/div[1]')
            if len(publication_status.find_elements(By.XPATH, './*')) > 1:
                continue

        video = vod.find_element(By.XPATH, './/div/a/div/div[4]/div/div/div/button')
        video.click()
        
        try:
            wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[last()]/div/div/div/div/div[1]/div/div/div/div/div/div/div[5]/button'))).click()
        except:
            if not skip_unpublished:
                wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[last()]/div/div/div/div/div[1]/div/div/div/div/div/div/div[4]/button'))).click()
        
        time.sleep(0.5)
        bot.find_element(By.XPATH, '/html/body/div[4]/div/div/div/div/div/div[last()-1]/div[2]/button').click()
        
        vods_uploaded += 1

        # Save the title of the last uploaded VOD, the current page number, and preferences
        save_last_uploaded_vod(vod_title, current_page, sort_from_oldest, skip_unpublished)

        if vods_uploaded >= vod_upload_limit:
            print("VOD upload limit reached, run this script again in 12h to upload more.")
            break

    time.sleep(1)

    # Check if both the "Next Page" and "Previous Page" buttons are not clickable
    if current_page > 1:
        try:
            previous_page_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div[3]/div/div/div[2]/div/main/div/div[3]/div/div/div/div[2]/div[2]/div[3]/div/div/div/div/div/div[1]/div[2]/div/button[1]')))
        except:
            print("All VODs have been uploaded.")
            bot.quit()
            exit()

    # Go to the next page
    next_page_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div[3]/div/div/div[2]/div/main/div/div[3]/div/div/div/div[2]/div[2]/div[3]/div/div/div/div/div/div[3]/div/button[2]')))
    next_page_button.click()
    time.sleep(2)
    current_page += 1

bot.quit()
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import requests
import os
# Path to your Chrome WebDriver
CHROMEDRIVER_PATH = "bin/chromedriver"  # Update this path

# Setup Selenium with headless Chrome
options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")

service = Service(CHROMEDRIVER_PATH)
driver = webdriver.Chrome(service=service, options=options)

# Load the local HTML file
file_path = "https://updates.jenkins.io/download/plugins/"  # Update with correct file path
# print('here')
driver.get(file_path)
# driver.get('https://updates.jenkins.io/download/plugins/42crunch-security-audit/')
# print('here')

# Find all links
initial_links = driver.find_elements(By.TAG_NAME, "a")
# print(links)
# print(links)

# print(links[5].get_attribute('href'))
# driver.get(links[5].get_attribute('href'))
# print(driver.find_elements(By.TAG_NAME, "a")[0].get_attribute('href'))

# Click each link
plugins = []
for link in initial_links[4:]:
    try:
        if not link.get_attribute("href") == file_path:
            plugins.append(link.get_attribute("href"))

            # print(driver.find_elements(By.TAG_NAME, "a")[0].get_attribute('href'))
            # link.click()
            # time.sleep(1)  # Give time for navigation
            # driver.back()  # Go back after clicking
    except Exception as e:
        print(f"Could not click {href}: {e}")

def get_latest_version_link(plugin_link):
    driver.get(plugin_link)
    return(driver.find_elements(By.TAG_NAME, "a")[0].get_attribute('href'))

for link in plugins:
    # driver.get(link)
    current_links = driver.find_elements(By.TAG_NAME, "a")
    # print(driver.find_elements(By.TAG_NAME, "a")[0].get_attribute('href'))
    plugin_file = get_latest_version_link(link)
    response = requests.get(plugin_file)
    os.makedirs('plugins', exist_ok=True)
    if response.status_code == 200:
        with open(os.path.join('plugins', os.path.basename(plugin_file)), "wb") as file:
            file.write(response.content)
        print("File downloaded successfully!")
    else:
        print("Failed to download the file. Status code:", response.status_code)
    print(get_latest_version_link(link))

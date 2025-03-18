import requests
from bs4 import BeautifulSoup
import os
from tqdm import tqdm
import time

url = "https://updates.jenkins.io/download/plugins/"
response = requests.get(url)

# Check if request was successful
if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")

    # Example: Find all links
    links = [a['href'] for a in soup.find_all('a', href=True)[4:]]
    links = [os.path.join(url, link) for link in links]
    for link in links:
        print(link)
else:
    print("Failed to retrieve the page")

def get_latest_plugins_links(initial_links):
    latest_links = []
    for plugin_url in initial_links:
        print('here1')
        response = requests.get(plugin_url)
        print('here2')
        new_soup = BeautifulSoup(response.text, "html.parser")
        current_links = [a['href'] for a in new_soup.find_all('a', href=True)]
        
        # print(current_links[0])
        latest_links.append(os.path.join(plugin_url, current_links[0]))
    for link in latest_links:
        print(link)
        # for link in current_links:
        #     print(link)
        # return current_links
get_latest_plugins_links(links)
# def download_latest_plugins():
    
    # for link in plugins:
    #     # driver.get(link)
    #     current_links = driver.find_elements(By.TAG_NAME, "a")
    #     # print(driver.find_elements(By.TAG_NAME, "a")[0].get_attribute('href'))
    #     plugin_file = get_latest_version_link(link)
    #     response = requests.get(plugin_file)
    #     os.makedirs('plugins', exist_ok=True)
    #     if response.status_code == 200:
    #         with open(os.path.join('plugins', os.path.basename(plugin_file)), "wb") as file:
    #             file.write(response.content)
    #         print("File downloaded successfully!")
    #     else:
    #         print("Failed to download the file. Status code:", response.status_code)
    #     print(get_latest_version_link(link))

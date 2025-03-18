import requests
from bs4 import BeautifulSoup
import os
from tqdm import tqdm
from utils import download_file

url = "https://updates.jenkins.io/download/plugins/"
def get_plugins_list():
    print('Retrieving plugins list:')
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        links = [a['href'] for a in soup.find_all('a', href=True)[4:]]
        links = [os.path.join(url, link) for link in links]
        for link in links:
            print(link)
        return links

def get_latest_plugins_links(initial_links):
    print('retrieving all latest plugin links(shortened for now)')
    latest_links = []
    with tqdm(initial_links[:20], desc="Processing") as pbar:
        for plugin_url in pbar:
            response = requests.get(plugin_url)
            new_soup = BeautifulSoup(response.text, "html.parser")
            current_links = [a['href'] for a in new_soup.find_all('a', href=True)]
            latest_links.append(os.path.join(plugin_url, current_links[0][1:]))
            pbar.set_postfix({"Current": plugin_url})
    for link in latest_links:
        print(link)

    return latest_links

def download_plugins(download_links):
    with tqdm(download_links[:20], desc="Processing") as pbar:
        for plugin_link in pbar:
            pbar.set_postfix({"Current": os.path.basename(plugin_link)})
            download_file(plugin_link, 'plugins/latest')


links = get_plugins_list()
plugins_download_links = get_latest_plugins_links(links)
download_plugins(plugins_download_links)

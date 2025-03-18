import requests
from bs4 import BeautifulSoup
import os
from tqdm import tqdm
from utils import download_file
from concurrent.futures import ThreadPoolExecutor, as_completed

url = "https://updates.jenkins.io/download/plugins/"
max_workers = 200

def get_plugins_list():
    print('Retrieving plugins list:')
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        links = [a['href'] for a in soup.find_all('a', href=True)[4:]]
        links = [os.path.join(url, link) for link in links]
        # for link in links:
        #     print(link)
        return links

def get_latest_plugins_links(initial_links):
    print('Retrieving all latest plugin links (parallelized)')
    latest_links = []

    # Function to process each plugin URL
    def process_plugin(plugin_url):
        response = requests.get(plugin_url)
        new_soup = BeautifulSoup(response.text, "html.parser")
        current_links = [a['href'] for a in new_soup.find_all('a', href=True)]
        return os.path.join(plugin_url, current_links[0][1:])

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(process_plugin, url): url for url in initial_links}

        with tqdm(total=len(futures), desc="Processing") as pbar:
            for future in as_completed(futures):
                latest_link = future.result()
                latest_links.append(latest_link)
                pbar.set_postfix({"Current": latest_link})
                pbar.update(1)  # Update progress bar as tasks complete

    # for link in latest_links:
    #     print(link)
    return latest_links

def download_plugins(download_links):
    print('Downloading plugins:')
    def download_plugin(plugin_link):
        download_file(plugin_link, 'plugins/latest')

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(download_plugin, plugin_link): plugin_link for plugin_link in download_links}

        with tqdm(total=len(download_links), desc="Downloading") as pbar:
            for future in as_completed(futures):
                pbar.set_postfix({"Current": os.path.basename(futures[future])})
                pbar.update(1)  # Update progress bar as tasks complete

links = get_plugins_list()
plugins_download_links = get_latest_plugins_links(links)
download_plugins(plugins_download_links)

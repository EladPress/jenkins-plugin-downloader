from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests
from bs4 import BeautifulSoup
import os
from config import *


def get_plugins_list():
    print('Retrieving plugins list:')
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        links = [a['href'] for a in soup.find_all('a', href=True)[4:]]
        links = [os.path.join(url, link) for link in links]
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

    return latest_links

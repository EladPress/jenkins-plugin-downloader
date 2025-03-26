from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests
from bs4 import BeautifulSoup
import os
from config import *

def get_plugin_info(plugin_name, version='all'):
    response = requests.get(f'{url}{plugin_name}/')
    soup = BeautifulSoup(response.text, "html.parser")

    plugin = []
    if version == 'all':
        for a in soup.find_all("a", class_="version"):
            if a.text == 'permalink to the latest':
                plugin.append({
                    'name': plugin_name,
                    'version': 'latest',
                    'link': os.path.join(url, plugin_name, a["href"][1:])
                })
            else:
                plugin.append({
                    'name': plugin_name,
                    'version': a.text,
                    'link': a['href']
                })
    else: 
        a = soup.find_all("a", class_="version", string=version)
        plugin = [{
            "name": plugin_name,
            'version': version,
            'link': a[0]['href']
        }]
    return plugin

def get_all_plugins_info():
    plugin_names = get_plugins_names()
    print('Retrieving info for all plugins (parallelized)')
    latest_links = []

    plugins = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(get_plugin_info, plugin_name): plugin_name for plugin_name in plugin_names}

        with tqdm(total=len(futures), desc="Processing") as pbar:
            for future in as_completed(futures):
                plugins += future.result()
                plugin_name = future.result()[0]['name']
                pbar.set_postfix({"Current": plugin_name})
                pbar.update(1)  # Update progress bar as tasks complete

    return plugins

def get_plugins_names():
    print('Retrieving plugins list:')
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        names = [a.text for a in soup.find_all('a', href=True)[4:]]
        return names

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

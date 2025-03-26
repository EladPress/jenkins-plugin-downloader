import os
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
from config import max_workers, destination

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

def download_plugins_updated(plugins, max_workers=max_workers):
    print('Downloading plugins:')
    def download_plugin(plugin_link, plugin_name, version):
        download_file(plugin_link, f'jenkins-plugins/{plugin_name}/{version}')
    print(f'max_workers: {max_workers}')
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(download_plugin, plugin['link'], plugin['name'], plugin['version']): plugin['link'] for plugin in plugins}
        with tqdm(total=len(plugins), desc="Downloading") as pbar:
            for future in as_completed(futures):
                pbar.set_postfix({"Current": os.path.basename(futures[future])})
                pbar.update(1)  # Update progress bar as tasks complete

def download_file(url, path):
    file_name = os.path.basename(url)
    response = requests.get(url)
    os.makedirs(os.path.join(destination, path), exist_ok=True)
    if response.status_code == 200:
        with open(os.path.join(destination, path, file_name), 'wb') as file:
            file.write(response.content)
    else:
        print(f'Failed to download {file_name}. Status code:', response.status_code)
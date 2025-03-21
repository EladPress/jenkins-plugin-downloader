import os
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
from env import max_workers

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


def download_file(url, path):
    file_name = os.path.basename(url)

    response = requests.get(url)
    os.makedirs(path, exist_ok=True)
    if response.status_code == 200:
        with open(os.path.join(path, file_name), 'wb') as file:
            file.write(response.content)
        # print(f'{file_name} downloaded successfully!')
    else:
        print(f'Failed to download {file_name}. Status code:', response.status_code)
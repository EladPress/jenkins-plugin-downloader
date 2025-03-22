import sys
import os
sys.path.append(os.path.abspath("./src"))

from process_plugins import *
from utils import *
import requests
from bs4 import BeautifulSoup

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

plugins = get_all_plugins_info()
download_plugins_updated(plugins, max_workers=300)
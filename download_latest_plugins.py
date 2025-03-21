import sys
import os
sys.path.append(os.path.abspath("./src"))

from utils import download_plugins
from process_plugins import get_plugins_list, get_latest_plugins_links

links = get_plugins_list()
plugins_download_links = get_latest_plugins_links(links)
download_plugins(plugins_download_links)
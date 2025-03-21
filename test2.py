import requests
from bs4 import BeautifulSoup
import os
from utils import download_file, download_plugins
from process_plugins import *

from env import *





links = get_plugins_list()
plugins_download_links = get_latest_plugins_links(links)
download_plugins(plugins_download_links)

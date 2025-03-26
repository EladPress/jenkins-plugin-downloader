import sys
import os
sys.path.append(os.path.abspath("./src"))

from process_plugins import *
from utils import *
import requests
from bs4 import BeautifulSoup

plugins = get_all_plugins_info()
download_plugins_updated(plugins, max_workers=300)
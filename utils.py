import os
import requests


def download_file(url, path):
    file_name = os.path.basename(url)

    response = requests.get(url)
    os.makedirs(path, exist_ok=True)
    if response.status_code == 200:
        with open(os.path.join(path, file_name), 'wb') as file:
            file.write(response.content)
        print(f'{file_name} downloaded successfully!')
    else:
        print(f'Failed to download {file_name}. Status code:', response.status_code)
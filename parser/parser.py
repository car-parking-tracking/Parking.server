import time
import os
import re
import zipfile

import requests
from bs4 import BeautifulSoup

from moscow_data_processing import process


URL = 'https://data.mos.ru/opendata/7704786030-platnye-parkovki-na-ulichno-dorojnoy-seti/passport?versionNumber=9&releaseNumber=17'


while True:
    request = requests.get(URL)

    soup = BeautifulSoup(request.text, 'html.parser')
    element = soup.select_one("#passport > article > table > tbody > tr:nth-child(16) > td:nth-child(2)")

    with open('previous_results', 'r', encoding='utf-8') as file:
        previous_content = file.read()

    if element.text.strip() == previous_content.strip():
        print('Данные не обновлялись, повторю запрос через 24 часа')
        time.sleep(86400)
    else:
        url_to_excel = 'https:' + str(element.find('a').get('href'))
        digits = re.findall(r'\d+', url_to_excel)
        digits = int(digits[0])-2
        modified_url = re.sub(r'\d+', str(digits), url_to_excel)

        with open('previous_results', 'w', encoding='utf-8') as file:
            file.write(element.text)

        custom_filename = 'raw_data.zip'
        download = requests.get(modified_url)
        if download.status_code == 200:
            with open(custom_filename, "wb") as file:
                file.write(download.content)
            with zipfile.ZipFile('raw_data.zip', 'r') as zip_ref:
                first_file = zip_ref.namelist()[0]
                with zip_ref.open(first_file) as source_file, open('raw_data.json', 'wb') as target_file:
                    target_file.write(source_file.read())
            process()
            os.remove('raw_data.zip')
            os.remove('raw_data.json')
            print('Повторный запрос через 24 часа')
            time.sleep(86400)
        else:
            print("Не удалось скачать файл. Код состояния:", download.status_code)

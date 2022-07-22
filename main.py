import requests
from bs4 import BeautifulSoup
import lxml
import json
import csv

# url = 'https://www.taxi-heute.de/de/adressen/kategorien/955'
#
headers = {
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
}
# req = requests.get(url, headers=headers)
# src = req.text
#
# with open('index.html', 'w') as file:
#     file.write(src)

# with open('index.html') as file:
#     src = file.read()
#
# soup = BeautifulSoup(src, 'lxml')
# all_taxi_href = soup.find_all('a', hreflang='de')
#
# all_taxi_dict = {}
# for item in all_taxi_href:
#     item_text = item.text
#     item_href = 'https://www.taxi-heute.de' + item.get('href')
#
#     all_taxi_dict[item_text] = item_href
#
# with open('all_taxi_dict.json', 'w') as file:
#     json.dump(all_taxi_dict, file, indent=4, ensure_ascii=False)





with open('all_taxi_dict.json') as file:
    all_taxi = json.load(file)

count = 0
taxi_list_result = []
for taxi_name, taxi_href in all_taxi.items():
    count += 1
    print(count)
    print(taxi_href)
    req = requests.get(url=taxi_href, headers=headers)
    src = req.text

    try:
        soup = BeautifulSoup(req.text, 'lxml')
        taxi_info = soup.find('div', class_='field field--name-node-title field--type-ds field--label-hidden field__item')
        taxi_fullname = taxi_info.find('h1').text.strip()

        taxi_info2 = soup.find('fieldset', class_='js-form-item form-item js-form-wrapper form-wrapper')
        taxi_adres_strasse = taxi_info2.find('div', class_='field field--name-field-adresse-strasse-nr field--type-string field--label-inline clearfix').text.strip()
        taxi_adres_PLZ = taxi_info2.find('div', class_='field field--name-field-adresse-plz-ort field--type-string field--label-inline clearfix').text.strip()
        taxi_adres_bundesland = taxi_info2.find('div', class_='field field--name-field-adressen-bundesland field--type-entity-reference field--label-inline clearfix').text.strip()

        taxi_info3 = soup.find('div', class_='field field--name-field-adresse-mail field--type-email field--label-above')
        taxi_mail = taxi_info3.find('div', class_='field__item').text

        taxi_list_result.append(
            {
                'Name': taxi_fullname,
                'Address': {
                    'Strasse': taxi_adres_strasse.split('\n')[1],
                    'PLZ, Ort': taxi_adres_PLZ.split('\n')[1],
                    'Bundesland': taxi_adres_bundesland.split('\n')[1],
                },
                'Mail': taxi_mail
            }
        )

    except Exception as ex:
        taxi_list_result.append('Object has no attribute')
        print(ex)

with open('taxi_list_result.json', 'a', encoding='utf-8') as file:
    json.dump(taxi_list_result, file, indent=4, ensure_ascii=False)


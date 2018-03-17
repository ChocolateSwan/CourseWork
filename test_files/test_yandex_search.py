# import yandex_search
# yandex = yandex_search.Yandex(api_user='olyasur1996', api_key='03.485805363:094651a13cca89bf31b600569879242c')
# print(yandex.search('"Interactive Saudi"').items)

import requests
url = 'https://yandex.ru/search/xml?'
key = '03.485805363:094651a13cca89bf31b600569879242c'
text = 'привет'
lang = 'kk-ru'
r = requests.post(url, data={'key': key, 'user': 'olyasur1996'})
# Выводим результат
print(r.text)
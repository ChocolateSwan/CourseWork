import requests
url = 'https://translate.yandex.net/api/v1.5/tr.json/translate?'
key = 'trnsl.1.1.20180310T190946Z.c9152ab571dfc5ab.e6af6d123c42b4461104f7db69832c720d9c63ec'
text = 'привет'
lang = 'kk-ru'
r = requests.post(url, data={'key': key, 'text': text, 'lang': lang})
# Выводим результат
print(r.text)
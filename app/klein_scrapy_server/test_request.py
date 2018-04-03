import requests
word = "qwerty"
r = requests.get('http://127.0.0.1:8900/?word={}'.format(word))
print (r.json())
from app import app
from flask import render_template, flash, jsonify, request
from app.forms import SearchForm
import requests
from test_files.lang_module import find_synonyms
from functools import reduce

MIN_COUNT = 5

@app.route('/', methods=['GET', 'POST'])
def search():
    form = SearchForm() # csrf_enabled=False
    print(form.data)
    if form.validate_on_submit():
        # TODO анализ несколько слов
        # TODO подсказки
        # TODO переписать иф покороче
        if form.data['another_site_flag']:
            url = form.data['another_site']
        else:
            url = form.data['select_url']
        response = requests.get('http://127.0.0.1:8900/?word={w}&url={u}'
                                .format(w=form.data['search'],
                                        u=url))
        print(response.json())
        flash('Поиск удался =)')
        return render_template("index.html",
                        form = form,
                        results = response.json())
    return render_template("index.html",
                           form=form,
                           results="не было поиска")




@app.route('/process_form/', methods=['post'])
def process_form():
    form = SearchForm()
    # Слова

    # TODO переписать иф покороче
    if form.data['another_site_flag']:
        url = form.data['another_site']
    else:
        url = form.data['select_url']

    word = form.data['search']
    word = word.replace("&", "*")

    unwanted_words = form.data['unwanted_words']

    print("Debug: Список слов: {w}".format(w=word))
    print("Debug: Url: {u}".format(u=url))
    print("Debug: Нежелательные слова: {u}".format(u=unwanted_words))

    try:
        response = requests.get('http://127.0.0.1:8900/?word={w}&url={url}'
                                .format(w=word,
                                        url=url))
        # TODO фильтровать по не пустому found arr !!!!!!!!!!!!!!!!!!!!!
        response = response.json()
    except Exception:
        print("Error: Сервис Scrapy недоступен или неправильный URL!")
        message = "Сайт недоступен или произошли непредвиденные обстоятельства :( "
        return jsonify(data={
            'results': [],
            'message': message,
        })

    words = word.split("*") if word.find("|") == -1 \
        else word.split("|")

    if response:
        sum_all_resp = reduce(lambda s, el: s + el,
                     list(map(lambda el: len(el['found_arr']), response)))

        print("Debug: Всего от Scrapy {sum} совпадений.".format(sum=sum_all_resp))

        if sum_all_resp < MIN_COUNT:
            synonyms = find_synonyms(words)
            if synonyms:

                message = "Найдено всего {} совпадений(я). Это очень мало, но найдены синонимы. Попробуйте: <br>".format(sum_all_resp) + \
                          "; ".join(list(map(lambda x: "{}: {}".format(x['word'], ", ".join(x["synonyms"])),synonyms)))
            else:
                message = "Слишком мало совпадений ({}), и к вашему слову не найдено ни одного синонима :(".format(sum_all_resp) +\
                          " Попробуйте ввести другое слово"
        else:
            message = "Отлично! Поиск успешно состоялся :)"

    else:

        try:
            requests.get(url)
        except:
            # TODO а если сайт уже написан???? сделать if, и наверное надо перенести это в начало
            message = "Поиск не удался! Вы уверены, что вы правильно написали адрес сайта?"
            return jsonify(data={
                'results': response,
                'message': message,
            })

        synonyms = find_synonyms(words)
        if synonyms:
            message = "Не найдено ни одного совпадения, но найдены синонимы. Попробуйте: <br> " \
                      + "; ".join(list(map(lambda x: "{}: {}".format(x['word'], ", ".join(x["synonyms"])),synonyms)))
        else:
            message = "Проверьте написание вашего слова! Возможно оно написано неверно" \
                      " или у него нет синонимов :("


    return jsonify(data={
        'results': response,
        'message': message,
    })

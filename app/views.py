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
    # TODO переписать иф покороче
    if form.data['another_site_flag']:
        url = form.data['another_site']
    else:
        url = form.data['select_url']

    try:
        response = requests.get('http://127.0.0.1:8900/?word={w}&url={u}'
                                .format(w=form.data['search'],
                                        u=url))
        response = response.json()
    except Exception:
        print("Error: Сервис Scrapy недоступен или неправильный URL!")
        response = []
        synonyms = []
        message = "Сайт недоступен или произошли непредвиденные обстоятельства :( "
        return jsonify(data={
            'results': response,
            'message': message,
        })

    if response:
        sum_resp = reduce(lambda s,el: s + el,
                     list(map(lambda el: len(el['found_arr']), response)))
        print("Debug: Всего от Scrapy {sum} совпадений.".format(sum=sum_resp))
        synonyms = []
        if sum_resp < MIN_COUNT:
            synonyms = find_synonyms(form.data['search'])
            if synonyms:
                message = "Слишком мало совпадений! Попробуйте: " + ", ".join(synonyms)
            else:
                message = "Слишком мало совпадений, но к вашему слову не найдено ни одного синонима :(" \
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

        synonyms = find_synonyms(form.data['search'])
        if synonyms:
            message = "Не найдено ни одного совпадения! Попробуйте: " + ", ".join(synonyms)
        else:
            message = "Проверьте написание вашего слова! Возможно оно написано неверно" \
                      " или у него нет синонимов :("


    return jsonify(data={
        'results': response,
        'message': message,
    })

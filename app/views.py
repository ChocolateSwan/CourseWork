from app import app
from flask import render_template, flash, jsonify, request
from app.forms import SearchForm
import requests
from test_files.lang_module import find_synonyms, find_antonyms, find_synonyms_from_db
from functools import reduce
from test_files.utils import cut_found_arr
from .program_dict import PROGRAMS
from flask_mysqldb import MySQL
import _mysql
import MySQLdb
import os



MIN_COUNT = 20
conn = MySQLdb.connect(host="localhost",user="graduate_work",
                  passwd="graduate_work",db="GraduateWork")


@app.route('/', methods=['GET',"POST"])
def search():
    return render_template("index.html",
                           form=SearchForm(),)


@app.route('/process_form/', methods=['post'])
def process_form():
    form = SearchForm()

    urls = form.data['select_url']
    programs = list(filter(lambda x: x["url"] in urls, PROGRAMS))

    try:
        urls = list(map(lambda x: x["программы"], programs))
    except:
        urls = []

    word = form.data['search']
    word = word.replace("&", "*")

    unwanted_words = form.data['unwanted_words']

    print("Debug: Список слов: {w}".format(w=word))
    print("Debug: Url: {u}".format(u=urls))
    print("Debug: Нежелательные слова: {u}".format(u=unwanted_words))

    try:
        response=[]
        for url in urls:
            print(url)

            resp_json = requests.get('http://127.0.0.1:8900/?&word={w}&url={url}&unwanted={uw}'
                                .format(w=word,
                                        url=url,
                                        uw=unwanted_words))
            response += resp_json.json()
        response = list(filter(lambda x: x["found_arr"], response))
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
                     list(map(lambda el: el['count'], response)))

        print("Debug: Всего от Scrapy {sum} совпадений.".format(sum=sum_all_resp))

        if sum_all_resp < MIN_COUNT:
            synonyms = find_synonyms_from_db(conn,words)
            if synonyms:

                message = "Найдено всего {} совпадений(я). Это очень мало, но найдены синонимы. Попробуйте: <br>".format(sum_all_resp) + \
                          "; ".join(list(map(lambda x: "{}: {}".format(x['word'], ", ".join(x["synonyms"])),synonyms)))
            else:
                message = "Слишком мало совпадений ({}), и к вашему слову не найдено ни одного синонима :(".format(sum_all_resp)

        else:
            response = list(map(lambda x: cut_found_arr(x), response))

            message = "Отлично! Поиск успешно состоялся - найдено {} совпадений!".format(sum_all_resp)

    else:

        try:
            for url in urls:
                requests.get(url)
        except:
            message = "Поиск не удался! Адрес сайта(ов) неверный!"
            return jsonify(data={
                'results': response,
                'message': message,
            })

        synonyms = find_synonyms_from_db(conn,words)
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


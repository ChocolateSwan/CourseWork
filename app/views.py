from app import app
from flask import render_template, flash, jsonify, request
from app.forms import SearchForm
import requests
from test_files.lang_module import find_synonyms, find_antonyms
from functools import reduce
from test_files.utils import cut_found_arr
from .program_dict import PROGRAMS
from flask_mysqldb import MySQL
import _mysql
import MySQLdb
import os


MIN_COUNT = 20


def connection():
    conn = MySQLdb.connect(host="localhost",user="graduate_work",
                  passwd="graduate_work",db="GraduateWork")
    c = conn.cursor()

    return c, conn

# @app.before_request
# def before_request():
#     print("hdsbdhb")
#     # g.db.connect()  #note the connection to the database here
#
# @app.after_request
# def after_request(response):
#     print("hjsvvvvv")
#     # g.db.close()
#     return response


@app.route('/', methods=['GET',"POST"])
def search():
    # try:
    #     c, conn = connection()
    #     c.execute("""SELECT * FROM synonym where synonym_id = 1 or synonym_id = 2""")
    #     print("sdv", c.fetchall())
    #     # c.close()
    # except Exception as e:
    #     print(str(e))

    form = SearchForm() # csrf_enabled=False
    return render_template("index.html",
                           form=form,)


@app.route('/static/')
def static_file():
    print("jdnv")
    return app.send_static_file("static/css/test.html")

@app.route('/js/<path:path>')
def serve_static(path):
    root_dir = os.path.dirname(os.getcwd())
    print(os.path.join(root_dir, 'static', 'js', path))
    return app.send_static_file(os.path.join(root_dir, 'static', 'js', path))


@app.route('/process_form/', methods=['post'])
def process_form():
    form = SearchForm()

    url = form.data['select_url']
    program = list(filter(lambda x: x["url"] == url,PROGRAMS))
    print(program)
    try:
        url = program[0]['программы']
    except:
        url = ""

    word = form.data['search']
    word = word.replace("&", "*")

    unwanted_words = form.data['unwanted_words']

    print("Debug: Список слов: {w}".format(w=word))
    print("Debug: Url: {u}".format(u=url))
    print("Debug: Нежелательные слова: {u}".format(u=unwanted_words))

    try:
        response = requests.get('http://127.0.0.1:8900/?&word={w}&url={url}&unwanted={uw}'
                                .format(w=word,
                                        url=url,
                                        uw=unwanted_words))
        response = response.json()
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
            synonyms = find_synonyms(words)
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


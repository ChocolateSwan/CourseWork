from flask import render_template, jsonify
import MySQLdb
import requests

from app import app
from app.forms import SearchForm
from .program_dict import PROGRAMS
from utils.lang_module import find_synonyms_from_db
from utils.utils import cut_found_arr


MIN_COUNT = 20
conn = MySQLdb.connect(host="localhost",user="graduate_work",
                  passwd="graduate_work",db="GraduateWork")


@app.route("/", methods=["GET", "POST"])
def search():
    """Стартовая страница"""
    return render_template("index.html",
                           form=SearchForm(),)


@app.route('/process_form/', methods=['post'])
def process_form():
    """Обработка поискового запроса"""

    form = SearchForm()

    urls = form.data['select_url']

    # Необходимая информация из списка всех программ
    programs = list(filter(lambda x: x["url"] in urls, PROGRAMS))

    try:
        urls = list(map(lambda x: x["программы"], programs))
    except:
        urls = []

    word = form.data['search']
    # Экранирование амперсандов
    word = word.replace("&", "*")

    unwanted_words = form.data['unwanted_words']
    # Отладочная информация
    print("Debug: Список слов: {w}".format(w=word))
    print("Debug: Url: {u}".format(u=urls))
    print("Debug: Нежелательные слова: {u}".format(u=unwanted_words))

    try:
        # Запросы в скрапи
        response=[]
        for url in urls:
            resp_json = requests.get('http://127.0.0.1:8900/?&word={w}&url={url}&unwanted={uw}'
                                     .format(w=word,
                                             url=url,
                                             uw=unwanted_words))
            response += resp_json.json()
        # На всякий случай оставляем только непустые результаты поиска
        response = list(filter(lambda x: x["found_arr"], response))

    # Если скрапи недоступен или все плохо
    except Exception:
        message = "Сайт недоступен или произошли непредвиденные обстоятельства!"
        return jsonify(data={
            'results': [],
            'message': message,
        })

    words = word.split("*") if word.find("|") == -1 \
        else word.split("|")

    # Если были результаты поиска
    if response:
        sum_all_resp = sum(list(map(lambda el: el['count'], response)))

        print("Debug: Всего от Scrapy {sum} совпадений.".format(sum=sum_all_resp))

        # Если слишком мало результатов
        if sum_all_resp < MIN_COUNT:
            synonyms = find_synonyms_from_db(conn, words)
            # Если есть синонимы и результаты поиска
            if synonyms:
                message = "Найдено всего {} совпадений(я). " \
                          "Это очень мало, но найдены похожие слова. " \
                          "Попробуйте: <br>".format(sum_all_resp) + \
                          "; ".join(list(map(lambda x: "{}: {}".format(x['word'], ", ".join(x["synonyms"])),
                                             synonyms)))
            else:
                message = "Слишком мало совпадений ({}), и не найдено ни одного похожего слова!" \
                          "Попробуйте другой поисковый запрос"\
                    .format(sum_all_resp)

        else:
            response = list(map(lambda x: cut_found_arr(x), response))

            message = "Отлично! Поиск успешно состоялся - найдено {} совпадений."\
                .format(sum_all_resp)

    # Если нет результатов поиска
    else:
        # Если есть какой то неправильный урл
        try:
            for url in urls:
                requests.get(url)
        except:
            message = "Поиск не удался! Адрес сайта(ов) неверный!"
            return jsonify(data={
                'results': [],
                'message': message,
            })
        # Если нет результатов поиска но есть синонимы
        synonyms = find_synonyms_from_db(conn, words)
        if synonyms:
            message = "Не найдено ни одного совпадения, но найдены похожие слова. " \
                      "Попробуйте: <br> " \
                      + "; ".join(list(map(lambda x: "{}: {}".format(x['word'], ", ".join(x["synonyms"])),
                                           synonyms)))
        # Если нет результатов поиска и нет синонимов
        else:
            message = "Проверьте написание слов(а)! Возможно есть ошибки в написании" \
                      " или у слов(а) нет похожих слов!"

    return jsonify(data={
        'results': response,
        'message': message,
    })


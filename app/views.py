from flask import render_template, jsonify
import MySQLdb
import requests

from app import app
from app.forms import SearchForm
from .program_dict import PROGRAMS
from utils.lang_module import find_synonyms_from_db
from utils.utils import cut_found_arr


MIN_COUNT_OF_WORDS = 20
MIN_COUNT_OF_PAGES = 5
MAX_COUNT_OF_PAGES = 20

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
        message = "Сервис недоступен или произошли непредвиденные обстоятельства!"
        return jsonify(data={
            'results': [],
            'message': message,
        })

    words = word.split("*") if word.find("|") == -1 \
        else word.split("|")

    # Если были результаты поиска
    if response:
        sum_all_resp = sum(list(map(lambda el: el['count'], response)))
        sum_all_pages = len(response)

        print("Debug: Всего от Scrapy {sum} совпадений на {pages} страницах."
              .format(sum=sum_all_resp, pages=sum_all_pages))

        response = list(map(lambda x: cut_found_arr(x), response))
        # Если слишком мало результатов
        if sum_all_pages < MIN_COUNT_OF_PAGES:
            synonyms = find_synonyms_from_db(conn, words)
            # Если есть синонимы и результаты поиска
            if synonyms:
                message = "Найдено {} совпадений(я) на {} веб-страницах. " \
                          "Объем результатов слишком мал, но найдены связанные с вашим запросом дескрипторы. " \
                          "Вам стоит попробовать: <br>".format(sum_all_resp, sum_all_pages) + \
                          "; ".join(list(map(lambda x: "{}: {}".format(x['word'], ", ".join(x["synonyms"])),
                                             synonyms)))
            else:
                message = "Найдено {} совпадений(я) на {} веб-страницах. " \
                          "Объем результатов мал и не найдено ни одного связанного с вашим запросом дескриптора." \
                          " Возможно вам следует ввести другой поисковый запрос{}. "\
                    .format(sum_all_resp, sum_all_pages,
                            ' или отредактировать поле "исключаемые дескрипторы"' if len(unwanted_words) else "")

        elif sum_all_pages > MAX_COUNT_OF_PAGES:
            message = "Отлично! Поиск успешно состоялся - найдено {} совпадений(я) на {} веб-страницах. Объем " \
                      "результатов слишком велик. Возможно вам следует сузить область поиска " \
                      '(например добавить дескрипторов в поле "исключаемые дескрипторы").' \
                .format(sum_all_resp, sum_all_pages)
        else:

            message = "Отлично! Поиск успешно состоялся - найдено {} совпадений(я) на {} веб-страницах."\
                .format(sum_all_resp,sum_all_pages)

    # Если нет результатов поиска
    else:
        # Если есть какой то неправильный урл
        try:
            for url in urls:
                requests.get(url)
        except:
            message = "Поиск не удался! Адреса сайтов возможно ошибочны!"
            return jsonify(data={
                'results': [],
                'message': message,
            })
        # Если нет результатов поиска но есть синонимы
        synonyms = find_synonyms_from_db(conn, words)
        if synonyms:
            message = "Не найдено ни одного совпадения, но найдены связанные с вашим запросом дескрипторы. " \
                      "Вам стоит попробовать: <br> " \
                      + "; ".join(list(map(lambda x: "{}: {}".format(x['word'], ", ".join(x["synonyms"])),
                                           synonyms)))
        # Если нет результатов поиска и нет синонимов
        else:
            message = "Проверьте написание дескрипторов! Возможно есть ошибки в написании" \
                      " или связанных с вашим запросом дескрипторов не существует!"

    return jsonify(data={
        'results': response,
        'message': message,
    })


from app import app
from flask import render_template, flash, redirect, url_for
from app.forms import SearchForm
from .start_crawler import run_spider
import subprocess
import requests
word = "qwerty"


@app.route('/', methods=['GET', 'POST'])
def search():

    r = requests.get('http://127.0.0.1:8900/?word={}'.format(word))
    print(r.json())


    print("hello")
    url = "http://test.ru"
    form = SearchForm() # csrf_enabled=False
    print(form.data)
    if form.validate_on_submit():
        results = []
        if form.data['search'] == "qq":

            # results = run_spider()
            print("rrr", subprocess.check_output(['python3', './app/spider.py']))

        # print ("rrr", subprocess.check_output(['python3', './app/spider.py']))
        print(results)
        print("поиск удался")
        flash('Поиск удался =)')
        return render_template("index.html", url=url,
                        form = form,
                        results = results)
    return render_template("index.html",
                           url=url,
                           form=form,
                           results = "не было поиска")








# Кастомная страница защиты от CSRF
# from flask_wtf.csrf import CSRFError
#
# @app.errorhandler(CSRFError)
# def handle_csrf_error(e):
#     return render_template('csrf_error.html', reason=e.description), 400

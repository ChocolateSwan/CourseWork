from app import app
from flask import render_template, flash
from app.forms import SearchForm
import requests

word = "qwerty"

@app.route('/', methods=['GET', 'POST'])
def search():
    form = SearchForm() # csrf_enabled=False
    print(form.data)
    if form.validate_on_submit():
        # TODO анализ несколько слов
        # TODO подсказки
        response = requests.get('http://127.0.0.1:8900/?word={}'.format(form.data['search']))
        print(response.json())
        print("поиск удался")
        flash('Поиск удался =)')
        return render_template("index.html",
                        form = form,
                        results = response.json())
    return render_template("index.html",
                           form=form,
                           results="не было поиска")








# Кастомная страница защиты от CSRF
# from flask_wtf.csrf import CSRFError
#
# @app.errorhandler(CSRFError)
# def handle_csrf_error(e):
#     return render_template('csrf_error.html', reason=e.description), 400

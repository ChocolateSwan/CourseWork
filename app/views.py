from app import app
from flask import render_template, flash, jsonify, request
from app.forms import SearchForm
import requests

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
    # print(form.data)
    # TODO переписать иф покороче
    if form.data['another_site_flag']:
        url = form.data['another_site']
    else:
        url = form.data['select_url']
    response = requests.get('http://127.0.0.1:8900/?word={w}&url={u}'
                            .format(w=form.data['search'],
                                    u=url))
    print(response.json())


    return jsonify(data=response.json())

#     form = OurForm()
#     if form.validate_on_submit():
#         return jsonify(data={'message': 'hello {}'.format(form.foo.data)})
# return jsonify(data=form.errors)

# Кастомная страница защиты от CSRF
# from flask_wtf.csrf import CSRFError
#
# @app.errorhandler(CSRFError)
# def handle_csrf_error(e):
#     return render_template('csrf_error.html', reason=e.description), 400

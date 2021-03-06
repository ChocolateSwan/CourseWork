from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectMultipleField
from .program_dict import PROGRAMS


class SearchForm(FlaskForm):
    """Форма для поиска"""
    search = StringField('слова для поиска',
                         render_kw={"class": "form-input form-input-width-90",
                                    "placeholder": "искомые дескрипторы (через & или |)"})

    unwanted_words = StringField('нежелательные слова',
                        render_kw={"class": "form-input form-input-width-100",
                                    "placeholder": "исключаемые дескрипторы"})

    select_url = SelectMultipleField('университеты и программы',
                                     render_kw={"class": "selectDemo sel"},
                                     choices=list(map(lambda p: (p['url'], p['название']), PROGRAMS)),)

    search_btn = SubmitField('Искать', render_kw={"class": "form-btn"})

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from .program_dict import PROGRAMS

class SearchForm(FlaskForm):
    search = StringField('слова для поиска',
                         render_kw={"class": "form-input form-input-width-100",
                                    "placeholder": "слова через & или |"})

    unwanted_words = StringField('нежелательные слова',
                         render_kw={"class": "form-input form-input-width-100",
                                    "placeholder": "нежелательные термины"})

    select_url = SelectField('выбрать сайт для поиска',
                             choices=[('не выбрано', 'сайт не выбран')] +
                                     list(map(lambda p: (p['url'], p['название']), PROGRAMS)),)

    search_btn = SubmitField('Искать', render_kw={"class": "form-btn"})

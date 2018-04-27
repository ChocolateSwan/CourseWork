from flask_wtf import FlaskForm
from wtforms import StringField,BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired
from .program_dict import PROGRAMS


# squared = list(map(lambda p: (p['название'], p['url']), PROGRAMS))

class SearchForm(FlaskForm):
    search = StringField('слова для поиска', validators=[DataRequired("Не пустое")],
                         render_kw={"class": "form-input form-input-width-100", "placeholder": "слова через & или |"})

    unwanted_words = StringField('нежелательные слова',
                         render_kw={"class": "form-input form-input-width-100","placeholder": "нежелательные термины"})

    # TODO choices as list
    select_url = SelectField(u'выбрать сайт для поиска',
                             # TODO тестовый сайт убрать
                             choices=[('не выбрано', 'сайт не выбран')] + list(map(lambda p: (p['url'], p['название']), PROGRAMS)) + [('http://htmlbook.ru/html/table', 'test rus'),('https://www.python.org', 'test eng') ]
                             ,)
    another_site_flag = BooleanField('другой сайт',render_kw={"class": "checkbox-hidden"})
    another_site = StringField('сайт не из списка',
                               render_kw={"class": "form-input form-input-width-50", "placeholder": "адрес сайта не из списка"})#, render_kw={'disabled':''},
    search_btn = SubmitField('Искать', render_kw={"class": "form-btn"})

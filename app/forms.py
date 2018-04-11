from flask_wtf import FlaskForm
from wtforms import StringField,BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired
from .program_dict import PROGRAMS


# squared = list(map(lambda p: (p['название'], p['url']), PROGRAMS))

class SearchForm(FlaskForm):
    search = StringField('слова для поиска', validators=[DataRequired("Не пустое")],
                         render_kw={"class": "form-input form-input-width-100"})
    # TODO choices as list
    select_url = SelectField(u'выбрать сайт для поиска',
                             # TODO тестовый сайт убрать
                             choices=[('не выбрано', 'не выбрано')] + list(map(lambda p: (p['url'], p['название']), PROGRAMS)) + [('http://htmlbook.ru/html/table', 'test')]
                             ,)
    another_site_flag = BooleanField('другой сайт',render_kw={"class": "checkbox-hidden"})
    another_site = StringField('сайт не из списка',
                               render_kw={"class": "form-input form-input-width-50"})#, render_kw={'disabled':''},
    search_btn = SubmitField('Искать', render_kw={"class": "form-btn"})

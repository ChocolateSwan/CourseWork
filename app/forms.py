from flask_wtf import FlaskForm
from wtforms import StringField,BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired


class SearchForm(FlaskForm):
    search = StringField('слова для поиска', validators=[DataRequired("Не пустое")],
                         render_kw={"class": "form-input form-input-width-100"})
    # TODO choices as list
    select_url = SelectField(u'выбрать сайт для поиска',
                             choices=[('yandex', 'yandex.ru'), ('google', 'google.com'), ('rambler', 'rambler.ru')],
                             validators=[DataRequired("Не пустое")])
    another_site_flag = BooleanField('другой сайт',render_kw={"class": "checkbox-hidden"}
                                     )
    another_site = StringField('сайт не из списка', validators=[DataRequired()],
                               render_kw={"class": "form-input form-input-width-50"})#, render_kw={'disabled':''},
    search_btn = SubmitField('Искать', render_kw={"class": "form-btn"})

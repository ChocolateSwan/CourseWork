from flask_wtf import FlaskForm, widgets
from wtforms import StringField, SubmitField, SelectField, SelectMultipleField,BooleanField
from .program_dict import PROGRAMS
from wtforms.widgets import ListWidget, CheckboxInput
# from flask.ext.wtf import Form, widgets

#
# class MultiCheckboxField(SelectMultipleField):
#     widget = ListWidget(prefix_label=False)
#     option_widget = CheckboxInput()

class SearchForm(FlaskForm):
    search = StringField('слова для поиска',
                         render_kw={"class": "form-input form-input-width-100",
                                    "placeholder": "слова через & или |"})

    unwanted_words = StringField('нежелательные слова',
                         render_kw={"class": "form-input form-input-width-100",
                                    "placeholder": "нежелательные термины"})

    select_url = SelectMultipleField('выбрать сайт для поиска', render_kw={"class": "selectDemo sel"},
                             choices=list(map(lambda p: (p['url'], p['название']), PROGRAMS)),)

    search_btn = SubmitField('Искать', render_kw={"class": "form-btn"})

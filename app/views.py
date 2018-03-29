from app import app
from flask import render_template, flash, redirect, url_for
from app.forms import SearchForm
# from .forms import SearchForm



# @app.before_request
# def before_request():
#     g.user = current_user
#     if g.user.is_authenticated():
#         g.user.last_seen = datetime.utcnow()
#         db.session.add(g.user)
#         db.session.commit()
#         g.search_form = SearchForm()

@app.route('/', methods=['GET', 'POST'])
def search():
    print("hello")
    url = "http://test.ru"
    form = SearchForm() # csrf_enabled=False
    if form.validate_on_submit():
        flash('Поиск удался =)')
        return redirect(url_for('search'))
    return render_template("index.html",
                           url=url,
                           form=form)








# Кастомная страница защиты от CSRF
# from flask_wtf.csrf import CSRFError
#
# @app.errorhandler(CSRFError)
# def handle_csrf_error(e):
#     return render_template('csrf_error.html', reason=e.description), 400

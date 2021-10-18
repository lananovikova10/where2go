from flask import render_template

from webapp import app
from webapp.country.forms import CounryChoose

@app.route("/")
def display():
    title = 'Куда поехать теперь?'
    country_choosed = CounryChoose()
    return render_template('index.html', page_title = title, form = country_choosed)

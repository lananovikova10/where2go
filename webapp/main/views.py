from flask import render_template, Blueprint, current_app

from webapp import app
from webapp.country.forms import CounryChoose

blueprint = Blueprint('main_page', __name__)

@blueprint.route("/")
def display():
    title = 'Куда поехать теперь?'
    country_choosed = CounryChoose()
    return render_template('index.html', page_title = title, form = country_choosed)

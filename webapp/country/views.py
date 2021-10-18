from flask import render_template, redirect, flash, url_for, request, Blueprint

from flask_login import LoginManager, current_user, login_required

from webapp import app

from webapp.country.forms import CounryChoose
from webapp import db
from webapp.country.models import UserRequest

blueprint = Blueprint('country_related', __name__, url_prefix='/countries')

@blueprint.route('/process_country', methods=['GET', 'POST'])
def check_signin():
    if current_user.is_authenticated:
        return process_country()
    else:
        flash('пожалуйста, авторизируйтесь')
        return redirect(url_for('user_related.login'))

def process_country():
    form = CounryChoose()
    if form.validate_on_submit():
        form.country_dep
        select_dep = request.form.get('country_dep')
        select_arr = request.form.get('country_arr')
    if select_dep != select_arr:
        choice = UserRequest(user_id=current_user.id, country_dep = select_dep, country_arr = select_arr)

        db.session.add(choice)
        db.session.commit()
        return redirect(url_for('country_related.country_request'))
    else: 
        flash('одинаковые страны, попробуйте еще')
        return redirect(url_for('display'))

@blueprint.route('/country_request')
@login_required
def country_request():
    title = f'Актуальная информация по странам'
    que = UserRequest.query.filter(UserRequest.user_id==current_user.id).order_by(UserRequest.id.desc()).limit(1)
    dep = que[0].country_dep
    arr = que[0].country_arr
    return render_template('country_request.html', page_title=title, country_dep=dep, country_arr=arr)

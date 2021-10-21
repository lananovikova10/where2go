from flask import render_template, redirect, flash, url_for, request, Blueprint


from flask_login import current_user, login_required


from webapp.country.forms import CounryChoose, UserRequest
from webapp import db

from webapp.countries_rosturizm import get_info_rosturizm
from webapp import log


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
        return redirect(url_for('main_page.display'))
        

@blueprint.route('/country_request')
@login_required
def country_request():
    title = f'Актуальная информация по странам'
    que = UserRequest.query.filter(UserRequest.user_id==current_user.id).order_by(UserRequest.id.desc()).limit(1)
    dep = que[0].country_dep
    arr = que[0].country_arr
    restrictions_by_country = get_info_rosturizm(arr)
    log.logging.info(arr)
    if restrictions_by_country == {}:
        no_data_by_country = "Сюда пока нельзя"
        log.logging.info(restrictions_by_country)
        return render_template('country/country_request.html', page_title=title, country_dep=dep, country_arr=arr, no_data_by_country = no_data_by_country)
    else:
        if 'transportation' in restrictions_by_country:
            transportation = restrictions_by_country['transportation']
        else:
            transportation = "У нас пока нет информации"
        if 'visa' in restrictions_by_country:
            visa = restrictions_by_country['visa']
        else:
            visa = "У нас пока нет информации"
        if 'vaccine' in restrictions_by_country:
            vaccine = restrictions_by_country['vaccine']
        else:
            vaccine = "У нас пока нет информации"
        if 'open_objects' in restrictions_by_country:
            open_objects = restrictions_by_country['open_objects']
        else:
            open_objects = "У нас пока нет информации"
        if 'conditions' in restrictions_by_country:
            conditions = restrictions_by_country['conditions']
        else:
            conditions = "У нас пока нет информации"    
        if 'restrictions' in restrictions_by_country:
            lockdown_restrictions = restrictions_by_country['restrictions']
        else:
            lockdown_restrictions = "У нас пока нет информации"
        return render_template('country/country_request.html', page_title=title, country_dep=dep, country_arr=arr, transportation = transportation, visa = visa, vaccine = vaccine, open_objects = open_objects, conditions = conditions, lockdown_restrictions = lockdown_restrictions)

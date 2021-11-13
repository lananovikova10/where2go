from flask import render_template, redirect, flash, url_for, request, Blueprint
from flask_login import current_user, login_required


from webapp.country.forms import CounryChoose, UserRequest, Country
from webapp import db, covid_api
from webapp.countries_rosturizm import get_info_rosturizm
from webapp.countries_rosturizm import get_countries_rosturizm, filter_set_of_headers
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
        choice = UserRequest(user_id=current_user.id, country_dep=select_dep, country_arr=select_arr)

        db.session.add(choice)
        db.session.commit()
        country = Country.query.filter_by(country_name=select_arr).first()
        log.logging.info(country.id)
        return redirect(url_for('country_related.country_request'))
    else:
        flash('одинаковые страны, попробуйте еще')
        return redirect(url_for('main_page.display'))


@blueprint.route('/process_country_from_list')
def process_country_from_list():
    id = int(request.args.get('identifier'))
    open_countries = get_open_countries()
    select_dep = 'Россия'
    for element in open_countries:
        if element['country_id'] == id:
            select_arr = element['country_name']
    choice = UserRequest(user_id=current_user.id, country_dep=select_dep, country_arr=select_arr)
    db.session.add(choice)
    db.session.commit()
    return redirect(url_for('country_related.country_request', identifier=id))


@blueprint.route('/country_request')
@login_required
def country_request():
    title = f'Актуальная информация по странам'
    que = UserRequest.query.filter(UserRequest.user_id==current_user.id).order_by(UserRequest.id.desc()).limit(1)
    dep = que[0].country_dep
    arr = que[0].country_arr
    restrictions_by_country = country_conditions_request(arr)
    covid_data = country_covid_request(arr)
    return render_template('country/country_request.html', page_title=title, 
                                country_dep=dep, country_arr=arr,
                                restrictions_by_country=restrictions_by_country,
                                covid_data=covid_data)


def country_conditions_request(arr):
    '''Возвращает кортеж из одного элемента при ошибке подключения,
    возвращает None при получении пустого словаря,
    возвращает кортеж из 6 элементов, если получен ожидаемый набор данных,
    возвращает кортеж из 7 элементов, если неожидаемый набор'''
    
    log.logging.info(arr)
    restrictions_by_country = get_info_rosturizm(arr)
    no_data_by_field = "Ошибка подключения. Обновите страницу"
    if restrictions_by_country is None:
        return no_data_by_field,
    elif restrictions_by_country == {}:
        return None
    else:
        restrictions_by_country = get_info_rosturizm(arr)[0]
        unusual_output_rosturizm = get_info_rosturizm(arr)[1]
        transportation = restrictions_by_country.get('transportation')
        visa = restrictions_by_country.get('visa')
        vaccine = restrictions_by_country.get('vaccine')
        conditions = restrictions_by_country.get('conditions')
        open_objects = restrictions_by_country.get('open_objects')
        restrictions = restrictions_by_country.get('restrictions')
        log.logging.info(restrictions_by_country)
        if not unusual_output_rosturizm:
            return transportation, visa, vaccine, conditions, open_objects, restrictions
        else:
            return transportation, visa, vaccine, conditions, open_objects, restrictions, 'unusual'


def get_open_countries():
    countries_list = get_countries_rosturizm()
    country_to_id_mapping = []
    for country in countries_list:
        log.logging.info(country)
        country_from_db = Country.query.filter_by(country_name=country).first()
        countries_data = {}
        if country_from_db:
            log.logging.info(country_from_db.country_name)
            countries_data['country_id'] = country_from_db.id
            countries_data['country_name'] = country_from_db.country_name
            log.logging.info(countries_data)
            country_to_id_mapping.append(countries_data)
    log.logging.info(country_to_id_mapping)

    return country_to_id_mapping


@blueprint.route('/country_list')
def display_countries_list():
    title = f"Какие страны открыты для россиян"
    countries_list = get_countries_rosturizm()
    country_to_id_mapping = get_open_countries()

    return render_template('country/country_list.html', page_title=title, countries_list=countries_list,
                            country_to_id_mapping=country_to_id_mapping)


# возвращает словарь из ответов по covid для страны
def country_covid_request(arr):
    country_query = Country.query.filter(Country.country_name==arr).first()
    country_code_resieved = country_query.country_code
    covid_data = covid_api.get_covid_data(country_code_resieved)
    return covid_data

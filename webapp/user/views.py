from flask import render_template, redirect, flash, url_for, Blueprint, request


from flask_login import login_user, logout_user, current_user, login_required

from webapp import db
from webapp.country.models import Country, UserRequest
from webapp.user.forms import LoginForm, RegistrationForm, User



blueprint = Blueprint('user_related', __name__, url_prefix='/users')


@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main_page.display'))
    form = LoginForm()
    return render_template('user/login.html', page_title='Страница логина', form=form)


@blueprint.route('/process-login', methods=['POST'])
def process_login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(login=form.username.data).first()
        if user and user.check_password(password=form.password.data):
            login_user(user)
            flash('Вы авторизированы')
            return redirect(url_for('main_page.display'))
    flash('Неправильное имя пользователя или пароль')
    return redirect(url_for('user_related.login'))


@blueprint.route('/logout')
def logout():
    logout_user()
    flash('Вы успешно разлогинились')
    return redirect(url_for('main_page.display'))


@blueprint.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main_page.display'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(login=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Поздравляем, вы зарегистрировались!')
        return redirect(url_for('user_related.login'))
    return render_template('user/register.html', page_title='Страница регистрации', form=form)


@blueprint.route('/requests')
@login_required
def show_user_requests():
    all_user_requests = UserRequest.query.filter(UserRequest.user_id==current_user.id).order_by(UserRequest.id.desc()).limit(25)
    country_to_id_mapping = get_country_id(all_user_requests)
    return render_template('user/user_requests.html', page_title='История ваших запросов',
                           all_user_requests=all_user_requests, user_name=current_user.login,
                           country_to_id_mapping=country_to_id_mapping)


def get_country_id(country_list):
    country_to_id_mapping = {}
    for country in country_list:
        country_from_db = Country.query.filter_by(country_name=country.country_arr).first()
        if country_from_db:
            country_to_id_mapping[country_from_db.country_name] = country_from_db.id
        country_from_db = Country.query.filter_by(country_name=country.country_dep).first()
        if country_from_db:
            country_to_id_mapping[country_from_db.country_name] = country_from_db.id
    return(country_to_id_mapping)


@blueprint.route('/process_country_from_user_request')
def process_country_from_user_request():
    select_dep = choose_select_by_id('dep')
    select_arr = choose_select_by_id('arr')
    choice = UserRequest(user_id=current_user.id, country_dep=select_dep, country_arr=select_arr)
    db.session.add(choice)
    db.session.commit()
    return redirect(url_for('country_related.country_request'))


def choose_select_by_id(template_id):
    id = int(request.args.get(template_id))
    country_from_db = Country.query.filter_by(id=id).first()
    return country_from_db.country_name

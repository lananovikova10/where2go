from flask import render_template, redirect, flash, url_for, request
from flask_admin.base import AdminIndexView

from flask_login import LoginManager, login_user, logout_user, current_user, login_required

from webapp import app

from webapp.forms import LoginForm, RegistrationForm, CounryChoose
from webapp.model import db, User, UserRequest, Country
from flask_admin.contrib.sqla import ModelView
from wtforms.validators import Email, DataRequired


@app.route("/")
def display():
    title = 'Куда поехать теперь?'
    country_choosed = CounryChoose()
    return render_template('index.html', page_title=title, form=country_choosed)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('display'))
    form = LoginForm()
    return render_template('login.html', page_title='Страница логина', form=form)


@app.route('/process-login', methods=['POST'])
def process_login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(login=form.username.data).first()
        if user and user.check_password(password=form.password.data):
            login_user(user)
            flash('Вы авторизированы')
            return redirect(url_for('display'))
    flash('Неправильное имя пользователя или пароль')
    return redirect(url_for('login'))


@app.route('/logout')
def logout():
    logout_user()
    flash('Вы успешно разлогинились')
    return redirect(url_for('display'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('display'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(login=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Поздравляем, вы зарегистрировались!')
        return redirect(url_for('login'))
    return render_template('register.html', page_title='Страница регистрации', form=form)


@app.route('/process_country', methods=['GET', 'POST'])
def check_signin():
    if current_user.is_authenticated:
        return process_country()
    else:
        flash('пожалуйста, авторизируйтесь')
        return redirect(url_for('login'))


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
        return redirect(url_for('country_request'))
    else:
        flash('одинаковые страны, попробуйте еще')
        return redirect(url_for('display'))


@app.route('/country_request')
@login_required
def country_request():
    title = f'Актуальная информация по странам'
    que = UserRequest.query.filter(UserRequest.user_id == current_user.id).order_by(UserRequest.id.desc()).limit(1)
    dep = que[0].country_dep
    arr = que[0].country_arr
    return render_template('country_request.html', page_title=title,
                           country_dep=dep, country_arr=arr)


# делает страницу админки доступной только для админов
class AdminView(AdminIndexView):

    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        flash('Вы не админ')
        return redirect(url_for('display', next=request.url))


# настройки для отображения таблицы в админке
class UserAdmin(ModelView):
    # хеширует пароль при создании юзера
    def on_model_change(self, form, User, is_created):
        if form.password.data:
            User.set_password(form.password.data)

    # проверка при создании
    form_args = {
        'login': {'validators': [DataRequired()]},
        'email': {'validators': [DataRequired(), Email()]},
        'password': {'validators': [DataRequired()]}
        }
    # скрывает поле user_requests на форме
    form_excluded_columns = ['user_requests', ]
    # добавляет поиск по email
    column_searchable_list = ['email', ]
    # добавляет фильтр по admin
    column_filters = ['admin']


class UserRequestAdmin(ModelView):
    form_args = {
        'country_arr': {'validators': [DataRequired()]},
        'country_dep': {'validators': [DataRequired()]},
        'User': {'validators': [DataRequired()]},
        }
    column_filters = ['user_id', ]


class CountryAdmin(ModelView):
    form_args = {
        'country_code': {'validators': [DataRequired()]},
        'country_name': {'validators': [DataRequired()]},
        }
    column_searchable_list = ['country_name', ]
    can_delete = False
    can_edit = False
    can_create = False

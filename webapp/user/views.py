from flask import render_template, redirect, flash, url_for, Blueprint


from flask_login import login_user, logout_user, current_user


blueprint = Blueprint('user_related', __name__, url_prefix='/users')

@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main_page.display'))
    form = LoginForm()
    return render_template('login.html', page_title='Страница логина', form=form)

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
    return render_template('register.html', page_title='Страница регистрации', form=form)


from webapp.user.forms import LoginForm, RegistrationForm
from webapp import db 
from webapp.user.models import User
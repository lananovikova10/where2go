from flask import render_template, redirect, flash, url_for

from flask_login import LoginManager, login_user, logout_user, current_user, login_required

from webapp import app

from webapp.forms import LoginForm, RegistrationForm
from webapp.model import db, User

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = "Войдите, чтобы просмотреть страницу"
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.route("/")
@login_required
def display():
    title = 'Куда поехать из России'
    return render_template('index.html', page_title = title)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('display'))
    form = LoginForm()
    return render_template('login.html', title='Sign In', form=form)

@app.route('/process-login', methods=['POST'])
def process_login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(login=form.username.data).first()
        if user and user.check_password(password=form.password.data):
            login_user(user)
            flash('Вы вошли на сайт')
            return redirect(url_for('display'))
    flash('Неправильное имя пользователя или пароль')
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    logout_user()
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
    return render_template('register.html', title='Register', form=form)
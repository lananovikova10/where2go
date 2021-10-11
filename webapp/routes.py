from flask import render_template, redirect, flash, url_for, request

from flask_login import LoginManager, login_user, logout_user, current_user, login_required

from webapp import app

from webapp.forms import LoginForm, RegistrationForm, CounryChoose
from webapp.model import db, User, UserRequest

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = "Войдите, чтобы просмотреть страницу"
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.route("/")
#@login_required
def display():
    title = 'Куда поехать теперь?'
    country_choosed = CounryChoose()
    return render_template('index.html', page_title = title, form = country_choosed)

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
    return render_template('register.html', title='Register', form=form)


@app.route('/process_country', methods=['GET', 'POST'])
def check_signin():
    if current_user.is_authenticated:
        return process_country()
    else:
        flash('пожалуйста, авторизируйтесь')
        return redirect(url_for('login'))
def process_country():
    #создаем элемент формы
    form = CounryChoose()
    if form.validate_on_submit():
        form.country_dep
        select_dep = request.form.get('country_dep')
        select_arr = request.form.get('country_arr')
    if select_dep != select_arr:
        choice = UserRequest(user_id=current_user.id, country_dep = select_dep, country_arr = select_arr)
        # если авторизирован - по проверке выше, брать user_id = current_user.id

        db.session.add(choice)
        db.session.commit()
        #flash(f'получилось, из {select_dep} в {select_arr}')
        return redirect(url_for('country_request'))
    else: 
        flash('одинаковые страны, попробуйте еще')
        return redirect(url_for('display'))

@app.route('/country_request')
def country_request():
    title = f'Актуальная информация по странам'
    #ожидается проверка на current user, чтобы делать фильтр по нему
    que = UserRequest.query.filter(UserRequest.user_id==current_user.id).order_by(UserRequest.id.desc()).limit(1)
    dep = que[0].country_dep
    arr = que[0].country_arr
    return render_template('country_request.html', title=title, country_dep=dep, country_arr=arr)

@app.route('/admin')
def admin():
    # добавить проверку на роль Админ
    title = f'Админка'
    users = User.query.all()
    for user in users:
        print(f'id {user.id}, login {user.login}')

    return render_template('admin.html', title=title, users = users)
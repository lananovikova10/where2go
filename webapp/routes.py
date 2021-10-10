from datetime import datetime
from flask import render_template, flash, redirect, url_for, request
from webapp import app, db
from webapp.forms import LoginForm, CounryChoose
from webapp.model import UserRequest, User
from flask_login import LoginManager, current_user, login_user, logout_user


@app.route('/')
def display():
    title = 'Куда поехать теперь?'
    country_choosed = CounryChoose()
    return render_template('index.html', page_title = title, form = country_choosed)

@app.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', title='Sign In', form=form)



@app.route('/process_country', methods=['GET', 'POST'])
# подготовлен блок для проверки авторизации
# def check_signin():
#     #if not current_user.is_authenticated:
#         return process_country()
#     else:
#         flash('пожалуйста, авторизуйтесь')
#         return redirect(url_for('login'))


def process_country():
    #создаем элемент формы
    form = CounryChoose()
    if form.validate_on_submit():
        form.country_dep
        select_dep = request.form.get('country_dep')
        select_arr = request.form.get('country_arr')
    if select_dep != select_arr:
        choice = UserRequest(user_id=1, country_dep = select_dep, country_arr = select_arr)
        # если авторизирован - по проверке выше, брать user_id = current_user.id

        db.session.add(choice)
        db.session.commit()
        return redirect(url_for('country_request'))
    else: 
        flash('одинаковые страны, попробуйте еще')
        return redirect(url_for('display'))

@app.route('/country_request')
def country_request():
    title = f'Актуальная информация по странам'
    #ожидается проверка на current user, чтобы делать фильтр по нему
    que = UserRequest.query.filter(UserRequest.user_id==1).order_by(UserRequest.id.desc()).limit(1)
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
from datetime import datetime
from flask import render_template, flash, redirect, url_for, request
from webapp import app, db
from webapp.forms import LoginForm, CounryChoose
from webapp.model import UserRequest, User
from flask_login import LoginManager, current_user, login_user, logout_user


@app.route('/')
def display():
    title = 'Куда поехать теперь?'
    # country_name = ['Австралия', 'Австрия', 'Азербайджан', 'Албания', 'Алжир', 'Ангола', 'Андорра', 'Антигуа и Барбуда']
    # country_code = ['AU', 'AU2', 'AZZ', 'ALD', 'ALZ', 'ANG', 'ANO', 'AAB']
    # quant = len(country_name)
    country_choosed = CounryChoose()
    return render_template('index.html', page_title = title, form = country_choosed)

@app.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', title='Sign In', form=form)



@app.route('/process_country', methods=['GET', 'POST'])
# def check_signin():
#     if 2 != 2:
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
        # создать новый экземпляр модели
        select_dep = request.form.get('country_dep')
        select_arr = request.form.get('country_arr')
    if select_dep != select_arr:
        choice = UserRequest(user_id=1, country_dep = select_dep, country_arr = select_arr)
        
        # # if current_user.is_authenticated:
        # #     choice.user_id = current_user.id
        db.session.add(choice)
        db.session.commit()
        flash(f'получилось, из {select_dep} в {select_arr}')
        return redirect(url_for('country_request'))
    else: 
        flash('одинаковые страны, попробуйте еще')
        return redirect(url_for('display'))

@app.route('/country_request')
def country_request():
    title = f'Актуальная информация по странам'
    dep = UserRequest.query.first().country_dep
    arr = UserRequest.query.first().country_arr
    return render_template('country_request.html', title=title, country_dep=dep, country_arr=arr)

@app.route('/admin')
def admin():
    title = f'Админка'
    users = User.query.all()
    for user in users:
        print(f'id {user.id}, login {user.login}')

    return render_template('admin.html', title=title, users = users)
from flask import render_template, flash, redirect, url_for, request
from webapp import app
from webapp.forms import LoginForm, CounryChoose


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
def process_country():
    #создаем элемент формы
    form = CounryChoose()
    if form.validate_on_submit():
        select_dep = request.form.get('country_dep')
        select_arr = request.form.get('country_arr')
    if select_dep != select_arr:
        flash(f'получилось, из {select_dep} в {select_arr}')
        return redirect(url_for('country_request'))
    else: 
        flash('одинаковые страны, попробуйте еще')
        return redirect(url_for('display'))

@app.route('/country_request')
def country_request():
    title = f'Актуальная информация по странам'
    return render_template('country_request.html', title=title)

@app.route('/admin')
def admin():
    title = f'Актуальная информация по странам'
    return render_template('country_request.html', title=title)
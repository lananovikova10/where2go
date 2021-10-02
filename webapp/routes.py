from flask import render_template, redirect, flash 
from webapp import app

from webapp.forms import LoginForm

@app.route("/")
def display():
    title = 'Куда поехать из России'
    return render_template('index.html', page_title = title)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect('/')
    return render_template('login.html', title='Sign In', form=form)
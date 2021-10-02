from flask import Flask, render_template
<<<<<<< HEAD
from config import Config
from forms import LoginForm
=======
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, migrate

from webapp.config import Config
from webapp.forms import LoginForm
>>>>>>> main

db = SQLAlchemy()  # creating db instance
app = Flask(__name__)
migrate = Migrate()
app.config.from_object(Config)

<<<<<<< HEAD

@app.route("/")

def display():
    title = 'Куда поехать из России'
    country_name = ['Австралия', 'Австрия', 'Азербайджан', 'Албания', 'Алжир', 'Ангола', 'Андорра', 'Антигуа и Барбуда']
    country_code = ['AU', 'AU2', 'AZZ', 'ALD', 'ALZ', 'ANG', 'ANO', 'AAB']
    quant = len(country_name)
    return render_template('index.html', page_title = title, quant = quant, country_name = country_name, country_code = country_code)

@app.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', title='Sign In', form=form)
=======
db.init_app(app)  #  bounding app and bd
migrate.init_app(app, db)  # bounfing app, bd and migration instance
>>>>>>> main

from webapp import routes, model

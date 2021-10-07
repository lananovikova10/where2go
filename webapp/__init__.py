from flask import Flask, render_template, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, migrate

from webapp.config import Config
from webapp.forms import LoginForm, CounryChoose


#запуск: 
# Linux и Mac: export FLASK_APP=webapp && export FLASK_ENV=development && flask run
# Windows: set FLASK_APP=webapp && set FLASK_ENV=development && set FLASK_DEBUG=1 && flask run

db = SQLAlchemy()  # creating db instance
app = Flask(__name__)
migrate = Migrate()
app.config.from_object(Config)

db.init_app(app)  #  bounding app and bd
migrate.init_app(app, db)  # bounfing app, bd and migration instance

from webapp import routes, model
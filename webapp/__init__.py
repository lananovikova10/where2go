from flask import Flask, render_template, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, migrate

from flask_login import LoginManager, login_user, logout_user, current_user, login_required

from webapp.config import Config
#from webapp.forms import LoginForm

db = SQLAlchemy()  # creating db instance
app = Flask(__name__)
migrate = Migrate()
app.config.from_object(Config)

db.init_app(app)  #  bounding app and bd
migrate.init_app(app, db)  # bounfing app, bd and migration instance

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

from webapp import routes, model

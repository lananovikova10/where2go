from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from webapp.config import Config
from webapp.forms import LoginForm


db = SQLAlchemy()  # creating db instance
app = Flask(__name__)
app.config.from_object(Config)

def create_app():
    db.init_app(app)  #  bounding app and bd
    migrate = Migrate(app, db)  # bounfing app, bd and migration instance

    return app

from webapp import routes, model

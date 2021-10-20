from flask import Flask, render_template, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, migrate
from flask_login import LoginManager
from flask_admin import Admin, AdminIndexView

from webapp.config import Config

db = SQLAlchemy()  # creating db instance
app = Flask(__name__)
migrate = Migrate(compare_type=True)
app.config.from_object(Config)

db.init_app(app)  #  bounding app and bd
migrate.init_app(app, db)  # bounding app, bd and migration instance

from webapp.user.views import blueprint as user_blueprint
from webapp.country.views import blueprint as country_blueprint
from webapp.main.views import blueprint as main_blueprint

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'user_related.login'
login_manager.login_message = "Войдите, чтобы просмотреть страницу"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

app.register_blueprint(country_blueprint)
app.register_blueprint(main_blueprint)
app.register_blueprint(user_blueprint)

from flask_login import current_user
from flask import redirect, flash, url_for, request

from webapp.country.models import UserRequest, Country
from webapp.user.models import User 
from webapp.admin.views import AdminView, ModelView, UserAdmin, UserRequestAdmin

from webapp import routes, model
from webapp.model import db, User, UserRequest, Country

admin = Admin(app, index_view=routes.AdminView())
admin.add_view(routes.CountryAdmin(Country, db.session))
admin.add_view(routes.UserAdmin(User, db.session))
admin.add_view(routes.UserRequestAdmin(UserRequest, db.session))

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, migrate
from flask_login import LoginManager
from flask_admin import Admin

from webapp.config import Config
from webapp.admin.views import AdminView, ModelView, UserAdmin, UserRequestAdmin, CountryAdmin


db = SQLAlchemy()  # creating db instance
app = Flask(__name__)
migrate = Migrate(compare_type=True)
app.config.from_object(Config)

db.init_app(app)  #  bounding app and bd
migrate.init_app(app, db)  # bounding app, bd and migration instance

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'user_related.login'
login_manager.login_message = "Войдите, чтобы просмотреть страницу"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

from webapp.country.models import UserRequest, Country
from webapp.user.models import User
from webapp.user.views import blueprint as user_blueprint
from webapp.country.views import blueprint as country_blueprint
from webapp.main.views import blueprint as main_blueprint

app.register_blueprint(country_blueprint)
app.register_blueprint(main_blueprint)
app.register_blueprint(user_blueprint)

admin = Admin(app, index_view=AdminView())
admin.add_view(CountryAdmin(Country, db.session))
admin.add_view(UserAdmin(User, db.session))
admin.add_view(UserRequestAdmin(UserRequest, db.session))

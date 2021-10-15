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

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = "Войдите, чтобы просмотреть страницу"
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)



from flask_login import current_user
from flask import redirect, flash, url_for, request

class AdminView(AdminIndexView):

    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        flash('Вы не админ')
        return redirect(url_for('display', next=request.url))

admin = Admin(app, index_view=AdminView())

from webapp import routes, model
from webapp.model import db, User
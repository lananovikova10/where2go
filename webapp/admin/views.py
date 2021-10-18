
from flask import redirect, flash, url_for, request, Blueprint
from flask_admin.base import AdminIndexView
from flask_login import current_user


from flask_admin.contrib.sqla import ModelView
from wtforms.validators import Email, DataRequired

blueprint = Blueprint('admin_related', __name__, url_prefix='/admin')

# делает страницу админки доступной только для админов
class AdminView(AdminIndexView):

    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        flash('Вы не админ')
        return redirect(url_for('display', next=request.url))

# настройки для отображения таблицы в админке
class UserAdmin(ModelView):
    # хеширует пароль при создании юзера
    def on_model_change(self, form, User, is_created):
        if form.password.data:
            User.set_password(form.password.data)
    
    # проверка при создании
    form_args = {
        'login': {'validators': [DataRequired()]},
        'email': {'validators': [DataRequired(), Email()]},
        'password': {'validators': [DataRequired()]}
        }
    # скрывает поле user_requests на форме
    form_excluded_columns = ['user_requests',]
    # добавляет поиск по email
    column_searchable_list = ['email',]
    # добавляет фильтр по admin
    column_filters = ['admin']

class UserRequestAdmin(ModelView):
    form_args = {
        'country_arr': {'validators': [DataRequired()]},
        'country_dep': {'validators': [DataRequired()]},
        'User': {'validators': [DataRequired()]},
        }
    column_filters = ['user_id',]
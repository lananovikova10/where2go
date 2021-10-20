from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo


from webapp.model import User, Country
from webapp.model import db
from webapp import app
from webapp import log 


class LoginForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()],
                           render_kw={"class": "form-control"})
    password = PasswordField('Пароль', validators=[DataRequired()],
                             render_kw={"class": "form-control"})
    submit = SubmitField('Войти', render_kw={"class": "btn btn-primary"})


class RegistrationForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()],
                           render_kw={"class": "form-control"})
    email = StringField('Электронная почта', validators=[DataRequired(), Email()],
                        render_kw={"class": "form-control"})
    password = PasswordField('Пароль', validators=[DataRequired()],
                             render_kw={"class": "form-control"})
    password2 = PasswordField('Повторите пароль', validators=[DataRequired(),
                              EqualTo('password', message='Пароли не совпадают')],
                              render_kw={"class": "form-control"})
    submit = SubmitField('Зарегистрироваться', render_kw={"class": "btn btn-primary"})

    def validate_username(self, login):
        user = User.query.filter_by(login=login.data).first()
        if user is not None:
            raise ValidationError('Выберите другое имя.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Введите другой адрес почты.')


class CounryChoose(FlaskForm):
    with app.app_context():
        country_info_query = db.session.query(Country.country_name)
        country_name_list = []
        for country in country_info_query:
            country = str(country)
            country = country[2:][:-3].replace("\\xa0", " ")
            country_name_list.append(country)
            country_name_list.sort()

    country_dep = SelectField('Страна отправления', choices=["Россия"],
                              validators=[DataRequired()],
                              render_kw={"class": "form-select form-select-lg mb-3"})
    country_arr = SelectField('Страна назначения', choices=country_name_list,
                              validators=[DataRequired()],
                              render_kw={"class": "form-select form-select-lg mb-3"})                   
    submit = SubmitField('Поехали!', render_kw={"class": "btn btn-primary"})

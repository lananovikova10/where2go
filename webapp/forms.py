from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo

from webapp.model import User

class LoginForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()], render_kw={"class": "form-control"})
    email = StringField('Электронная почта', validators=[DataRequired()], render_kw={"class": "form-control"})
    password = PasswordField('Пароль', validators=[DataRequired()], render_kw={"class": "form-control"})
    submit = SubmitField('Войти',render_kw={"class":"btn btn-primary"})

class RegistrationForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()], render_kw={"class": "form-control"})
    email = StringField('Электронная почта', validators=[DataRequired(), Email()], render_kw={"class": "form-control"})
    password = PasswordField('Пароль', validators=[DataRequired()], render_kw={"class": "form-control"})
    password2 = PasswordField(
        'Повторите пароль', validators=[DataRequired(), EqualTo('password')], render_kw={"class": "form-control"})
    submit = SubmitField('Зарегистрироваться',render_kw={"class":"btn btn-primary"})

    def validate_username(self, login):
        user = User.query.filter_by(login=login.data).first()
        if user is not None:
            raise ValidationError('Выберите другое имя.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Введите другой адрес почты.')
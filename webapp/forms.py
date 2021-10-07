from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')

class CounryChoose(FlaskForm):
    country_name_list = ['Австралия', 'Австрия', 'Азербайджан', 'Албания', 'Алжир', 'Ангола', 'Андорра', 'Антигуа и Барбуда']
    country_code_list = ['AU', 'AU2', 'AZZ', 'ALD', 'ALZ', 'ANG', 'ANO', 'AAB']
    quant = len(country_name_list)

    country_dep = SelectField('Страна отправления', choices=country_name_list,\
                                  validators=[DataRequired()], render_kw={"class": "form-control"})
    country_arr = SelectField('Страна назначения', choices=country_name_list,\
                                  validators=[DataRequired()], render_kw={"class": "form-control"})                      
    submit = SubmitField('Поехали!', render_kw={"class":"btn btn-primary"})
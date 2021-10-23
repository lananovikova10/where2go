import unicodedata


from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField
from wtforms.validators import DataRequired


from webapp.country.models import Country, UserRequest
from webapp import app, db
from webapp import log

from webapp.country import map_countries


class CounryChoose(FlaskForm):
    with app.app_context():
        country_info_query = db.session.query(Country.country_name)
        country_name_list = []
        for country in country_info_query:
            country = str(country)
            country = country[2:][:-3]
            if country in map_countries.Countries.keys():
                country = map_countries.Countries.get(country)
            log.logging.info(country)
            unicodedata.normalize('NFKD', country)
            country = country.replace("и\u0306", "й")
            log.logging.info(country)
            country_name_list.append(country)
            country_name_list.sort()

    country_dep = SelectField('Страна отправления', choices=["Россия"],\
                                  validators=[DataRequired()], render_kw={"class": "form-select form-select-lg mb-3"})
    country_arr = SelectField('Страна назначения', choices=country_name_list,\
                                  validators=[DataRequired()], render_kw={"class": "form-select form-select-lg mb-3"})                      
    submit = SubmitField('Поехали!', render_kw={"class":"btn btn-primary"})

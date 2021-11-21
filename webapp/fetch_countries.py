import requests
import json
import unicodedata
from webapp import log
from webapp import app, db
from webapp.country.models import Country
from webapp import map_countries
from webapp.config import Config

continents_list = ["Европа", "Азия", "Океания", "Африка", "Америка"]


def fetch_country_data():
    countries_data = []
    for continent in continents_list:
        country_api_url = "http://htmlweb.ru/geo/api.php"
        params = {
            "location": continent,
            "json": "",
            "api_key": Config.COUNTRY_API_KEY
        }
        try:
            request_result = requests.get(country_api_url, params=params)
            request_result.raise_for_status()
        except(requests.RequestException):
            log.logging.warning('Ошибка сети')
        countries_fetch_result = json.loads(unicodedata.normalize('NFKD',
                                            request_result.text))
        for value in countries_fetch_result.values():
            countries_data.append(value)
    return countries_data


def parse_country_data():
    list_of_countries = fetch_country_data()
    for country_object in list_of_countries:
        try:
            country_code = country_object.get('id')
            country_name = country_object.get('name')
            country_name = country_name.replace("и\u0306", "й")
            if country_name in map_countries.Countries.keys():
                country_name = map_countries.Countries.get(country_name)
            log.logging.info(country_name)
            save_countries(country_name=country_name,
                           country_code=country_code)
        except(AttributeError):
            log.logging.info('Это не словарь')


def save_countries(country_name, country_code):
    country_exists = Country.query.filter(Country.country_name == country_name).first()
    if not country_exists:
        new_country = Country(country_name=country_name,
                              country_code=country_code)
        db.session.add(new_country)
        db.session.commit()

import requests

from webapp import app
from webapp.model import Country, db
from webapp import db
from webapp.config import Config

continents_list = ["Европа", "Азия", "Океания", "Африка", "Америка"]


def fetch_country_data():
    countries = {}
    countries_data = []
    for continent in continents_list:
        country_api_url = Config.COUNTRY_API_URL
        params = {
            "location": continent,
            "json": "",
            "api_key": Config.COUNTRY_API_KEY
        }
        get_request_result = requests.get(country_api_url, params = params)
        get_request_result.raise_for_status()
        countries_fetch_result = get_request_result.json()
        countries.update(countries_fetch_result)
        for value in countries.values():
            countries_data.append(value)
    return countries_data 


def parse_country_data():
    list_of_countries = fetch_country_data()
    for country_object in list_of_countries:
        try:
            country_name = country_object.get('name')
            country_code = country_object.get('country_code3')
            save_countries(country_name=country_name, country_code=country_code)
        except(AttributeError):
            print('Это не словарь')       


def save_countries(country_name, country_code):
    country_exists = Country.query.filter(Country.country_name == country_name).count()
    if not country_exists:
        new_country = Country(country_name=country_name, country_code=country_code)
        db.session.add(new_country)
        db.session.commit()

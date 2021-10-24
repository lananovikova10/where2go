from webapp import app, db
from webapp.fetch_countries import parse_country_data
from webapp.country.models import Country

with app.app_context():
    Country.query.delete()
    parse_country_data()

from webapp import app, db
from webapp.fetch_countries import parse_country_data

with app.app_context():
    parse_country_data()

from webapp import app, db
from webapp.country.models import Country

with app.app_context():
    Country.query.delete()

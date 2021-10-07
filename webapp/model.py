# from sqlalchemy import Column, Integer, String
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from webapp import db
class Country(db.Model):
    __tablename__ = 'countries'
    id = db.Column(db.Integer, primary_key=True)
    country_code = db.Column(db.String)
    country_name = db.Column(db.String)

    def __repr__(self):
        return f'<Country {self.country_code} {self.country_name}>'

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(128), unique=True)
    password = db.Column(db.String(128))

    def set_password(self, password):
        self.password = generate_password_hash(password)
    def verify_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f'<User {self.login} {self.email}>'
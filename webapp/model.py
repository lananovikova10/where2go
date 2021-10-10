# from sqlalchemy import Column, Integer, String
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey

from webapp import db, app
class Country(db.Model):
    __tablename__ = 'countries'
    id = db.Column(db.Integer, primary_key=True)
    country_code = db.Column(db.String(3))
    country_name = db.Column(db.String)

    def __repr__(self):
        return f'<Country {self.country_code} {self.country_name}>'

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(128), unique=True)
    password = db.Column(db.String(200))

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

class UserRequest(db.Model):
    __tablename__ = 'users_requests'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('users.id'))
    country_dep = db.Column(db.String(120), index=True)
    country_arr = db.Column(db.String(120), index=True)

    def __repr__(self):
        return f'User {self.user_id} requested from {self.country_dep} to {self.country_arr}'

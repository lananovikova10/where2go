from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey

from webapp import db


class Country(db.Model):
    __tablename__ = 'countries'
    id = db.Column(db.Integer, primary_key=True)
    country_code = db.Column(db.String(3))
    country_name = db.Column(db.String)

    def __repr__(self):
        return f'<Country {self.country_code} {self.country_name}>'


class UserRequest(db.Model):
    __tablename__ = 'users_requests'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('users.id'))
    country_dep = db.Column(db.String(120), index=True)
    country_arr = db.Column(db.String(120), index=True)

    def __repr__(self):
        return f'User {self.user_id} requested from {self.country_dep} to {self.country_arr}'

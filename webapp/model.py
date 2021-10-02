# from sqlalchemy import Column, Integer, String

from webapp import db
class Country(db.Model):
    __tablename__ = 'countries'
    id = db.Column(db.Integer, primary_key=True)
    country_code = db.Column(db.String)
    country_name = db.Column(db.String)

    def __repr__(self):
        return f'<User {self.name} {self.email}>'


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)

# from sqlalchemy import Column, Integer, String

from webapp import db
class Country(db.Model):
    __tablename__ = 'countries'
<<<<<<< HEAD
    #Полина: нам точно нужен ид?
    #id = Column(Integer, primary_key=True)
    #Полина: предлагаю pk сделать от country_code (типа RUS, FRA)
    country_code = Column(String(3), unique=True, primary_key=True)
    country_name = Column(String)

    def __repr__(self):
        return f'Country {self.country_code}, {self.country_name}'
=======
    id = db.Column(db.Integer, primary_key=True)
    country_code = db.Column(db.String)
    country_name = db.Column(db.String)

    def __repr__(self):
        return f'<Country {self.country_code} {self.country_name}>'

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(100))
>>>>>>> main

    def __repr__(self):
        return f'<User {self.login} {self.email}>'
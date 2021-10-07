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

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(100))
    requests = relationship("UserRequest", back_populates="users")

    def __repr__(self):
        return f'<User {self.login} {self.email}>'

class UserRequest(db.Model):
    __tablename__ = 'users_requests'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('users.id'))
    country_dep = db.Column(db.String(120), index=True, unique=True)
    country_arr = db.Column(db.String(120), index=True, unique=True)
    user = relationship("User", back_populates="users_requests")

    def __repr__(self):
        return f'User {self.user_id} requested from {self.country_dep} to {self.country_arr}'

import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    # ссылка Полины
    #SQLALCHEMY_DATABASE_URI = 'postgresql://pueuxeap:3V_ALfpfKvH7XOSDHnVSq0uTQHA7PbuP@hattie.db.elephantsql.com/pueuxeap'
    SQLALCHEMY_DATABASE_URI = 'postgresql://lczqhqvn:Dxg4teyAJE8xNcCA1rx1iFE9Q1NaIFXf@hattie.db.elephantsql.com/lczqhqvn'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

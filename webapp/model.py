from sqlalchemy import Column, Integer, String
from db import Base, engine

class Country(Base):
    __tablename__ = 'countries'
    #Полина: нам точно нужен ид?
    #id = Column(Integer, primary_key=True)
    #Полина: предлагаю pk сделать от country_code (типа RUS, FRA)
    country_code = Column(String(3), unique=True, primary_key=True)
    country_name = Column(String)

    def __repr__(self):
        return f'Country {self.country_code}, {self.country_name}'

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
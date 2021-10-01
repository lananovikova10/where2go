from sqlalchemy import Column, Integer, String
from db import Base, engine

class Country(Base):
    __tablename__ = 'countries'
    id = Column(Integer, primary_key=True)
    country_code = Column(String)
    country_name = Column(String)

    def __repr__(self):
        return f'<User {self.name} {self.email}>'

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
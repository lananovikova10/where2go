from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine('postgresql://pueuxeap:3V_ALfpfKvH7XOSDHnVSq0uTQHA7PbuP@hattie.db.elephantsql.com/pueuxeap')

db_session = scoped_session(sessionmaker(bind=engine))

Base = declarative_base()
#to make requests from the model
Base.query = db_session.query_property()
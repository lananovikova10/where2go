from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine('postgresql://qhaxllmg:CtlAnL2FPdiSjIB4655AvaBA2q18JEUp@hattie.db.elephantsql.com/qhaxllmg')

db_session = scoped_session(sessionmaker(bind=engine))

Base = declarative_base()
#to make requests from the model
Base.query = db_session.query_property()
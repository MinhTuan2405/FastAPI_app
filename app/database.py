# connect string: "postgresql://user:password@postgresserver/db"

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from . config import settings

SQLALCHEMY_DATABASE_URL = "postgresql://{}:{}@{}/{}".format (
    settings.database_username, 
    settings.database_password, 
    settings.database_hostname,
    settings.database_name
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def getDatabase ():
    database = SessionLocal ()
    try:
        yield database
    finally:
        database.close ()
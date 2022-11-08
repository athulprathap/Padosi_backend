from click import echo
from sqlalchemy import create_engine, true
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings
import databases
from functools import lru_cache
from . import config
from starlette.config import Config

@lru_cache()
def setting():
    return config.Settings()

# SQLALCHEMY_DATABASE_URL = f"postgresql://postgres:password@localhost:5432/padosii_dev"
def database_pgsql_url_config():
    return str (setting().DB_CONNECTION + "://" + setting().DB_USERNAME + ":" + setting().DB_PASSWORD +
               "@" + setting().DB_HOST + ":" + setting().DB_PORT + "/" + setting().DB_DATABASE)

database = databases.Database(database_pgsql_url_config())
engine = create_engine(database_pgsql_url_config())

Base = declarative_base()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

 # Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

    return database

# @lru_cache()
# def setting():
#     return config.Settings()


# def database_pgsql_url_config():
#     return str(setting().DB_CONNECTION + "://" + setting().DB_USERNAME + ":" + setting().DB_PASSWORD +
#                "@" + setting().DB_HOST + ":" + setting().DB_PORT + "/" + setting().DB_DATABASE)


# database = databases.Database(database_pgsql_url_config())
# engine = sqlalchemy.create_engine(database_pgsql_url_config())


# def get_db():
#     return database
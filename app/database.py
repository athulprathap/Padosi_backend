from click import echo
from sqlalchemy import create_engine, true
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings
import databases


#SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"
# def database_pgsql_url_config():
#     return str (settings().database_username + "://" + settings().database_password+ ":" + settings().database_hostname +
#                "@" + settings().database_port + ":" + settings().settings.database_name+ "/")

# database = databases.Database(database_pgsql_url_config())
engine = create_engine("postgresql://postgres:8085@localhost/padossii",
echo=True)

Base = declarative_base()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

 # Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
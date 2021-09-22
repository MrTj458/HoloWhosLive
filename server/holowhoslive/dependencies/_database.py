from holowhoslive.config import get_settings
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

settings = get_settings()

# SQLAlchemy needs 'postgresql://' instead of 'postgres://' that Heroku gives so swap it over.
db_url = "postgresql://" + settings.database_url.split("://")[1]

engine = create_engine(db_url, future=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """Creates a SqlAlchemy DB Session"""
    with SessionLocal() as db:
        yield db

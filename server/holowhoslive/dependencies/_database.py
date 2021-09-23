from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from holowhoslive.config import get_settings

settings = get_settings()

# SQLAlchemy needs 'postgresql://' instead of 'postgres://' that Heroku gives so swap it over.
db_url = "postgresql+asyncpg://" + settings.database_url.split("://")[1]

engine = create_async_engine(db_url, future=True)

SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, class_=AsyncSession
)

Base = declarative_base()


async def get_db():
    """Creates a SqlAlchemy DB Session"""
    async with SessionLocal() as db:
        yield db

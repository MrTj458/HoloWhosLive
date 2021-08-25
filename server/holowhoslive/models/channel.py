from sqlalchemy import Column, Integer, String, Boolean

from holowhoslive.dependencies.database import Base

class Channel(Base):
    __tablename__ = 'channels'

    id = Column(Integer, primary_key=True, index=True)
    last_name = Column(String, index=True)
    first_name = Column(String, index=True)
    channel_name = Column(String, index=True)
    channel_id = Column(String, unique=True, index=True)

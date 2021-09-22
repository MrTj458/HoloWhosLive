from sqlalchemy import Column, Integer, String, Boolean

from holowhoslive.dependencies import Base


class YtChannel(Base):
    __tablename__ = "yt_channels"

    id = Column(Integer, primary_key=True, index=True)
    last_name = Column(String, index=True)
    first_name = Column(String, index=True)
    channel_id = Column(String, unique=True, index=True)
    group = Column(String, index=True)

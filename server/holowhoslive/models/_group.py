from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship

from holowhoslive.dependencies import Base


class Group(Base):
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    platform = Column(String, index=True)

    yt_channels = relationship("YtChannel", back_populates="group", lazy="selectin")

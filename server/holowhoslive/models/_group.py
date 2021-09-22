from sqlalchemy import Column, Integer, String, Boolean

from holowhoslive.dependencies import Base


class Group(Base):
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    platform = Column(String, index=True)

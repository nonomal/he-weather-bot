from datetime import datetime
from typing import Iterable, Tuple

from sqlalchemy import (
    Boolean,
    Column,
    String,
    BigInteger,
    Integer,
    DateTime,
    UniqueConstraint,
    ForeignKey,
)
from sqlalchemy.orm import relationship

from .database import Base
from ..intergration.location.he_location_client import Location


class Chat(Base):
    __tablename__ = "users"

    chat_id = Column(BigInteger, primary_key=True, index=True)
    is_active = Column(Boolean, default=True)

    latitude = Column(String)
    longitude = Column(String)
    city = Column(String, nullable=False)
    city_name = Column(String, nullable=False)
    time_zone = Column(String, nullable=False)

    # 外键：https://docs.sqlalchemy.org/en/14/orm/basic_relationships.html
    cron_jobs = relationship("CronJobs", backref="parent")
    ding_bot = relationship("DingBots", back_populates="chat", uselist=False)
    locations = relationship("Locations", backref="parent")

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    @property
    def location(self):
        return Location(
            name=self.city_name,
            lat=float(self.latitude),
            lon=float(self.longitude),
            tz=self.time_zone,
        )

    def is_location_exist(self):
        return self.latitude and self.longitude

    @property
    def sub_hours(self) -> Tuple:
        return tuple(job.hour for job in self.cron_jobs)

    @property
    def all_locations(self) -> Iterable[Location]:
        return [self.location, *(x.location for x in self.locations)]

    def __str__(self) -> str:
        return f"chat_{self.chat_id}_{self.city_name}({self.location})"

    def __repr__(self) -> str:
        return f"chat_{self.chat_id}"


class CronJobs(Base):
    __tablename__ = "cron_jobs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    chat_id = Column(BigInteger, ForeignKey("users.chat_id"))
    hour = Column(String, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (UniqueConstraint("chat_id", "hour"),)


class DingBots(Base):
    __tablename__ = "ding_bots"

    id = Column(Integer, primary_key=True, autoincrement=True)
    token = Column(String, index=True)

    chat_id = Column(BigInteger, ForeignKey("users.chat_id"))
    chat = relationship("Chat", back_populates="ding_bot")

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __str__(self) -> str:
        return f"ding_bot_{self.token}"

    __repr__ = __str__


class Locations(Base):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    chat_id = Column(BigInteger, ForeignKey("users.chat_id"))

    latitude = Column(String)
    longitude = Column(String)
    city = Column(String, nullable=False)
    city_name = Column(String, nullable=False)
    time_zone = Column(String, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    @property
    def location(self):
        return Location(
            name=self.city_name,
            lat=float(self.latitude),
            lon=float(self.longitude),
            tz=self.time_zone,
        )

    def __str__(self) -> str:
        return f"location_{self.chat_id}_{self.city_name}({self.location})"

    def __repr__(self) -> str:
        return f"location_{self.chat_id}"

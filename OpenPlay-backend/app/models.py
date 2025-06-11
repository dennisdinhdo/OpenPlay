from sqlalchemy import Column, Integer, String
from app.database import Base

from sqlalchemy import ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

# this is the DB table and what it's created to be

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    phone = Column(String)
    gender = Column(String)
    skill_level = Column(String)  # e.g. beginner, intermediate, advanced
    preferred_position_1 = Column(String)
    preferred_position_2 = Column(String)

class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    location = Column(String)
    event_time = Column(DateTime, default=datetime.utcnow)
    required_positions = Column(String)  # comma-separated values
    creator_id = Column(Integer, ForeignKey("users.id"))
    is_public = Column(String, default="true")  # "true" or "false"
    description = Column(String, nullable=True) 

    creator = relationship("User")

class EventInvite(Base):
    __tablename__ = "invites"

    id = Column(Integer, primary_key=True)
    event_id = Column(Integer, ForeignKey("events.id"))
    invited_user_id = Column(Integer, ForeignKey("users.id"))
    position = Column(String)
    status = Column(String, default="pending")  # pending, accepted, rejected

    event = relationship("Event")
    user = relationship("User")

class EventRoster(Base):
    __tablename__ = "event_roster"

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id"))
    player_id = Column(Integer, ForeignKey("users.id"))
    position = Column(String, nullable=True)  # Optional

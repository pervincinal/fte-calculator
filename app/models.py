from sqlalchemy import Column, Integer, String, JSON, DateTime, ForeignKey, Float
from sqlalchemy.sql import func
from app.database import Base

class Tribe(Base):
    __tablename__ = "tribes"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    priority = Column(String)
    chapter_lead_id = Column(Integer)

class Squad(Base):
    __tablename__ = "squads"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    tribe_id = Column(Integer)
    priority = Column(String)
    status = Column(String)
    last_calculation = Column(JSON)

class ChapterLead(Base):
    __tablename__ = "chapter_leads"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)

class Calculation(Base):
    __tablename__ = "calculations"
    id = Column(Integer, primary_key=True)
    squad_id = Column(Integer)
    inputs = Column(JSON)
    results = Column(JSON)
    created_at = Column(DateTime, server_default=func.now())

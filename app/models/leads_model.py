from dataclasses import dataclass
from datetime import datetime
from app.configs.database import db
from sqlalchemy import Column, String, DateTime, Integer

@dataclass
class Leads(db.Model):

    name: str
    email: str
    phone: str
    creation_date: datetime
    last_visit: datetime
    visits: int

    __tablename__ = 'leads_card'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone = Column(String, unique=True, nullable=False)
    creation_date = Column(DateTime, nullable=False)
    last_visit = Column(DateTime, nullable=False)
    visits = Column(Integer, default=1)

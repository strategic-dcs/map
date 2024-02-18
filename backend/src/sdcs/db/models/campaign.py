
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime, Enum
from sqlalchemy.orm import relationship
from sdcs.db import SQLBase

from .coalition import Coalition

class Campaign(SQLBase):

    id = Column(Integer, primary_key=True)

    mission_id = Column(Integer, ForeignKey('mission.id'))
    mission = relationship('Mission')

    start = Column(DateTime)
    end = Column(DateTime, nullable=True)
    winner = Column(Enum(Coalition), nullable=True)
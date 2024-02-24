
from sqlalchemy import Column, Integer, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sdcs.db import SQLBase

from .coalition import Coalition
from .common import DateTimeUTC

class Campaign(SQLBase):

    id = Column(Integer, primary_key=True)

    mission_id = Column(Integer, ForeignKey('mission.id'))
    mission = relationship('Mission')

    start = Column(DateTimeUTC)
    end = Column(DateTimeUTC, nullable=True)
    winner = Column(Enum(Coalition), nullable=True)
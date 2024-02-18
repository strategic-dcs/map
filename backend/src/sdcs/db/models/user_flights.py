from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Text, Enum, DateTime
from sqlalchemy.orm import relationship

from sdcs.db import SQLBase
from .coalition import Coalition

class UserFlights(SQLBase):

    id = Column(Integer, primary_key=True)

    campaign_id = Column(Integer, ForeignKey('campaign.id'))
    campaign = relationship('Campaign')

    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship('User', back_populates='flights')

    unit_id = Column(Integer, ForeignKey('unit.id'))
    unit = relationship('Unit')

    side = Column(Enum(Coalition))
    start = Column(DateTime)

    leg_count = Column(Integer)
    distance = Column(Integer)
    distance_abs = Column(Integer)

    end = Column(DateTime, nullable=True)
    end_event = Column(Text, nullable=True)

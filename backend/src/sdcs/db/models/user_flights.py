from sqlalchemy import Column, Integer, ForeignKey, Text, Enum
from sqlalchemy.orm import relationship

from sdcs.db import SQLBase
from .coalition import Coalition
from .common import DateTimeUTC

class UserFlights(SQLBase):

    id = Column(Integer, primary_key=True)

    campaign_id = Column(Integer, ForeignKey('campaign.id'))
    campaign = relationship('Campaign')

    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship('User', back_populates='flights')

    unit_id = Column(Integer, ForeignKey('unit.id'))
    unit = relationship('Unit')

    side = Column(Enum(Coalition))
    start = Column(DateTimeUTC)

    leg_count = Column(Integer)
    distance = Column(Integer)
    distance_abs = Column(Integer)

    end = Column(DateTimeUTC, nullable=True)
    end_event = Column(Text, nullable=True)

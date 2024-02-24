from sqlalchemy import Column, Integer, ForeignKey, Boolean, Text, Enum
from sqlalchemy.orm import relationship

from sdcs.db import SQLBase
from .coalition import Coalition
from .common import DateTimeUTC

class Unit(SQLBase):
    id = Column(Integer, primary_key=True)

    campaign_id = Column(Integer, ForeignKey('campaign.id'))
    campaign = relationship('Campaign')

    coalition = Column(Enum(Coalition))

    user_id = Column(Integer, ForeignKey('user.id'), nullable=True)
    user = relationship('User')

    unit_id = Column(Integer)

    group_id = Column(Integer, ForeignKey('unit_group.id'))
    group = relationship('UnitGroup', back_populates='children')

    unit_suffix = Column(Text, nullable=True)

    player_can_drive = Column(Boolean)

    removed_at = Column(DateTimeUTC, nullable=True)
    removed_reason = Column(Text, nullable=True)

    unit_type_id = Column(Integer, ForeignKey('unit_type.id'))
    unit_type = relationship('UnitType')

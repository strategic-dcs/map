from sqlalchemy import Column, Integer, ForeignKey, Enum
from sqlalchemy.orm import relationship

from sdcs.db import SQLBase
from .coalition import Coalition

class UserSide(SQLBase):

    id = Column(Integer, primary_key=True)

    campaign_id = Column(Integer, ForeignKey('campaign.id'))
    campaign = relationship('Campaign')

    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship('User')

    coalition = Column(Enum(Coalition))

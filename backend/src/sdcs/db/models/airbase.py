
from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship
from sdcs.db import SQLBase


class Airbase(SQLBase):

    id = Column(Integer, primary_key=True)

    campaign_id = Column(Integer, ForeignKey('campaign.id'))
    campaign = relationship('Campaign')

    airbase_id = Column(Integer)

    name = Column(Text)
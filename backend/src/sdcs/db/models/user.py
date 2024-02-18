from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Text
from sqlalchemy.orm import relationship

from sdcs.db import SQLBase

class User(SQLBase):
    id = Column(Integer, primary_key=True)
    name = Column(Text)

    flights = relationship('UserFlights')

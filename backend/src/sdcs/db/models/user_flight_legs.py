from sqlalchemy import Column, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from sdcs.db import SQLBase
from .common import DateTimeUTC

class UserFlightLegs(SQLBase):

    id = Column(Integer, primary_key=True)

    flight_id = Column(Integer, ForeignKey('user_flights.id'))
    flight = relationship('UserFlights')

    start_time = Column(DateTimeUTC)
    end_time = Column(DateTimeUTC, nullable=True)

    committed = Column(Boolean)
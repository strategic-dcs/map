from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Text, Enum, DateTime
from sqlalchemy.orm import relationship

from sdcs.db import SQLBase
from .coalition import Coalition

class UserFlightLegs(SQLBase):

    id = Column(Integer, primary_key=True)

    flight_id = Column(Integer, ForeignKey('user_flights.id'))
    flight = relationship('UserFlights')

    start_time = Column(DateTime)
    end_time = Column(DateTime, nullable=True)

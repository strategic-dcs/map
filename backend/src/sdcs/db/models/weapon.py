from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Text, DateTime
from sqlalchemy.orm import relationship

from sdcs.db import SQLBase

class Weapon(SQLBase):
    id = Column(Integer, primary_key=True)

    # weapon_name = Column(Text)

    unit_id = Column(Integer, ForeignKey('unit.id'))
    unit = relationship('Unit')

    flight_leg_id = Column(Integer, ForeignKey('user_flight_legs.id'))
    flight_leg = relationship('UserFlightLegs')

    weapon_type_id = Column(Integer, ForeignKey('weapon_type.id'))
    weapon_type = relationship('WeaponType')
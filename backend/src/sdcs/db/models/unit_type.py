from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Text, Enum
from sqlalchemy.orm import relationship

from sdcs.db import SQLBase
from .unit_class import UnitClass

class DcsUnitType(SQLBase):
    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False, unique=True)

class UnitType(SQLBase):
    id = Column(Integer, primary_key=True)
    type_name = Column(Text, nullable=False, unique=True)
    is_static = Column(Boolean)
    unit_class = Column(Enum(UnitClass))

    dcs_type_id = Column(Integer, ForeignKey('dcs_unit_type.id'))
    dcs_type = relationship('DcsUnitType')

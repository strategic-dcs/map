from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Text, Enum
from sdcs.db import SQLBase
from .unit_class import UnitClass

class UnitType(SQLBase):
    id = Column(Integer, primary_key=True)
    type_name = Column(Text, nullable=False, unique=True)
    is_static = Column(Boolean)
    unit_type = Column(Text)
    unit_class = Column(Enum(UnitClass))
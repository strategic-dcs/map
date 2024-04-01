from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Text, DateTime
from sqlalchemy.orm import relationship

from sdcs.db import SQLBase

class WeaponType(SQLBase):
    id = Column(Integer, primary_key=True)

    name = Column(Text)
    display_name = Column(Text, nullable=True)

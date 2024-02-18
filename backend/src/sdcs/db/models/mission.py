from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Text
from sdcs.db import SQLBase

class Mission(SQLBase):

    id = Column(Integer, primary_key=True)
    name = Column(Text)
    display_name = Column(Text)

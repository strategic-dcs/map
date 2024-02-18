from enum import Enum as _Enum
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Text, Enum
from sqlalchemy.orm import relationship

from sdcs.db import SQLBase
from .coalition import Coalition

class GroupTemplateClass(str, _Enum):
  GROUND = "GROUND"
  SHIP = "SHIP"
  CARGOPLANE = "CARGOPLANE"
  AI_FIGHTER = "AI_FIGHTER"


class UnitGroup(SQLBase):
    id = Column(Integer, primary_key=True)

    campaign_id = Column(Integer, ForeignKey('campaign.id'))
    campaign = relationship('Campaign')

    coalition = Column(Enum(Coalition))

    group_id = Column(Integer)

    group_desc = Column(Text, nullable=True)

    parent_group_id = Column(Integer, ForeignKey('unit_group.id'), nullable=True)
    parent_group = relationship('UnitGroup', back_populates='children_groups')

    group_level = Column(Integer, nullable=True)
    group_cost = Column(Integer, nullable=True)

    created_by_id = Column(Integer, ForeignKey('user.id'), nullable=True)
    created_by = relationship('User', foreign_keys=[created_by_id])

    user_id = Column(Integer, ForeignKey('user.id'), nullable=True)
    user = relationship('User', foreign_keys=[user_id])

    use_iads = Column(Boolean)
    immortal = Column(Boolean)
    disableai = Column(Boolean)
    hidden_on_mfd = Column(Boolean)
    uncontrollable = Column(Boolean)
    max_range_percent = Column(Integer)
    unit_count = Column(Integer)
    template_class = Column(Enum(GroupTemplateClass), nullable=True)
    initial_group = Column(Boolean)

    children = relationship('Unit')
    children_groups = relationship('UnitGroup')
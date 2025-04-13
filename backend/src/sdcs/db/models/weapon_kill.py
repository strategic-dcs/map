import enum

from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Text, DateTime, Enum
from sqlalchemy.orm import relationship

from sdcs.db import SQLBase
from .common import DateTimeUTC
from .kill_association_method import KillAssociationMethod


class WeaponKill(SQLBase):
    id = Column(Integer, primary_key=True)

    kill_at = Column(DateTimeUTC)

    weapon_id = Column(Integer, ForeignKey('weapon.id'))
    weapon = relationship('Weapon')

    target_unit_id = Column(Integer, ForeignKey('unit.id'))
    target_unit = relationship('Unit')

    target_player_id = Column(Integer, ForeignKey('user.id'), nullable=True)
    target_player = relationship('User', foreign_keys=[target_player_id])

    kill_player_id = Column(Integer, ForeignKey('user.id'), nullable=True)
    kill_player = relationship('User', foreign_keys=[kill_player_id])

    superceded = Column(Boolean)
    assoc_method = Column(Enum(KillAssociationMethod), nullable=True)
    on_ground = Column(Boolean)


    vanity_points = Column(Integer)
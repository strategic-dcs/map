from enum import Enum

from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Text, DateTime
from sqlalchemy.orm import relationship

from sdcs.db import SQLBase


class KillAssociationMethod(str, Enum):
    UNKNOWN = "UNKNOWN"
    KILL = "KILL"
    HIT = "HIT"
    SPLASH = "SPLASH"
    PROX = "PROX"
    PROX_BY = "PROX_BY"
    PROX_BY_TYPE = "PROX_BY_TYPE"
    PROX_TYPE = "PROX_TYPE"
    SHOT_BY = "SHOT_BY"
    SHOT_BY_TYPE = "SHOT_BY_TYPE"
    SHOOTING_ACTIVE = "SHOOTING_ACTIVE"
    SHOOTING = "SHOOTING"
    SHOOTING_NEAR = "SHOOTING_NEAR"


class WeaponKill(SQLBase):
    id = Column(Integer, primary_key=True)

    kill_at = Column(DateTime)

    weapon_id = Column(Integer, ForeignKey('weapon.id'))
    weapon = relationship('Weapon')

    target_unit_id = Column(Integer, ForeignKey('unit.id'))
    target_unit = relationship('Unit')

    target_player_id = Column(Integer, ForeignKey('user.id'), nullable=True)
    target_player = relationship('User', foreign_keys=[target_player_id])

    kill_player_id = Column(Integer, ForeignKey('user.id'), nullable=True)
    kill_player = relationship('User', foreign_keys=[kill_player_id])

    superceded = Column(Boolean)
    #assoc_method = Column(Enum(KillAssociationMethod), nullable=True)
    on_ground = Column(Boolean)

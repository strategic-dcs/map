from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

from .core import SDCSBaseModel
from .kills import KillsByType
from .unit import Unit
from .dcs_unit_type import DCSUnitType
from .weapon_type import WeaponType


class Weapon(SDCSBaseModel):
    id: int = Field(description="Weapon ID")
    weapon_type: WeaponType
    unit: Unit

class WeaponSummary(SDCSBaseModel):
    weapon_type: WeaponType = Field(description="Weapon Type")
    unit_type: DCSUnitType = Field(description="DCS Unit TYpe")
    shots: int = Field(description="shots")
    kills: KillsByType
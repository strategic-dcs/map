from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

from .core import SDCSBaseModel
from .player import PlayerInfo
from .unit import Unit

class Weapon(SDCSBaseModel):
    id: int = Field(description="Weapon ID")
    weapon_name: str
    unit: Unit
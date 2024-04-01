from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

from .core import SDCSBaseModel
from .player import PlayerInfo
from .unit import Unit
from .weapon import Weapon
from sdcs.db.models.kill_association_method import KillAssociationMethod

class WeaponKill(SDCSBaseModel):
    id: int = Field(description="Weapon Kill")
    kill_at: datetime = Field(description="Time of Kill")
    kill_player: Optional[PlayerInfo] = Field(description="Killer Player")
    target_player: Optional[PlayerInfo] = Field(description="Target Player")
    target_unit: Unit = Field(description="Weapon Kill")
    weapon: Weapon = Field(description="weapon that caused the kill")
    assoc_method: KillAssociationMethod = Field(description="Method used to determine Kill")

from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime

from sdcs.db.models.kill_association_method import KillAssociationMethod

from .core import SDCSBaseModel
from .kills import KillsByType
from .weapon_type import WeaponType
from .unit_type import UnitType


class Unit(SDCSBaseModel):
    id: int = Field(description="Database Unit ID")
    unit_type: UnitType
    unit_suffix: Optional[str] = Field(description="Unit Display Name")
    removed_reason: Optional[str] = Field(description="What caused this unit not to exist")


class UnitSummary(SDCSBaseModel):
    unit_type: str = Field(description="Unit Type")
    flights: int = Field(description="Number of Flights")
    kills: KillsByType
    duration: int = Field(description="Seconds Controlled")


class AIUnitKill(SDCSBaseModel):
    id: int = Field(description="Weapon Kill DB ID")
    kill_at: datetime = Field(description="Time of Kill (UTC)")
    weapon_type: WeaponType = Field(description="Weapon Type")
    target_unit_type: str = Field(description="Unit Type")
    target_on_ground: bool = Field(description="Target on the ground at time of death")
    target_player_name: Optional[str] = Field(description="Target player name")
    assoc_method: KillAssociationMethod = Field(description="Method used to determine Kill")
    team_kill: bool = Field(description="Team Kill")
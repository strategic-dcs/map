from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime

from .core import SDCSBaseModel
from .kills import KillsByType
from .unit import Unit


class PlayerSummary(SDCSBaseModel):
    user_id: int = Field(description="user id")
    user_name: str = Field(description="Unit Type")
    flights: int = Field(description="Number of Flights")
    kills: KillsByType
    duration: int = Field(description="Seconds Controlled")


class PlayerKill(SDCSBaseModel):
    id: int = Field(description="Weapon Kill DB ID")
    kill_at: datetime = Field(description="Time of Kill (UTC)")
    weapon_name: str = Field(description="Weapon Name")
    killer_unit_type: str = Field(description="Unit Type")
    target_unit_type: str = Field(description="Unit Type")
    target_on_ground: bool = Field(description="Target on the ground at time of death")
    target_player_name: Optional[str] = Field(description="Target player name")


class PlayerModule(SDCSBaseModel):
    unit_type: str = Field(description="Module name")
    duration: int = Field(description="Seconds in module")


class PlayerInfo(SDCSBaseModel):
    name: str = Field(description="Current User Name")


class PlayerFlight(SDCSBaseModel):

    id: int = Field(description="Database ID of Flight")

    leg_count: int = Field(description="Number of legs")

    distance: int = Field(description="Distance from start to end of leg (direct)")
    distance_abs: int = Field(description="Distance from start to end of leg (route taken)")

    end_event: str = Field(description="Reason for end of flight")

    unit: Unit = Field(description="Unit for flight")

    start: datetime = Field(description="Start of Flight")
    end: datetime = Field(description="End of Flight")

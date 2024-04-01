from typing import Optional
from pydantic import BaseModel, Field

from .core import SDCSBaseModel

class KillTarget(SDCSBaseModel):
    player: Optional[int] = Field(description="Player Kills")
    ai: Optional[int] = Field(description="AI Kills")
    tk: Optional[int] = Field(description="Team Kills")


class Kills(SDCSBaseModel):
    id: int = Field(description="Pilot ID")
    pilot: str = Field(description="Pilot Name")
    kills: KillTarget = Field(description="Kills")


class KillsByType(SDCSBaseModel):
    aa: Optional[KillTarget] = Field(description="Air to Air Kills")
    ag: Optional[KillTarget] = Field(description="Air to Ground Kills")
    ga: Optional[KillTarget] = Field(description="Ground to Air Kills")
    gg: Optional[KillTarget] = Field(description="Ground to Ground Kills")

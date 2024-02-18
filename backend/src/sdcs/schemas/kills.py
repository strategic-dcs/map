from typing import Optional
from pydantic import BaseModel, Field

from .core import SDCSBaseModel

class Kills(SDCSBaseModel):
    pilot: str = Field(description="Pilot Name")
    kills: int = Field(description="Kills")


class KillsByType(SDCSBaseModel):
    a2a: int = Field(description="Air to Air Kills")
    a2g: int = Field(description="Air to Ground Kills")
    g2a: int = Field(description="Ground to Air Kills")
    g2g: int = Field(description="Ground to Ground Kills")

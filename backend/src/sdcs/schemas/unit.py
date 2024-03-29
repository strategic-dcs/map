from typing import Optional
from pydantic import BaseModel, Field

from .core import SDCSBaseModel
from .kills import KillsByType


class DCSUnitType(SDCSBaseModel):
    id: int = Field(description="Database DCSUnitType ID")
    name: str = Field(description="Model name in DCS")


class UnitType(SDCSBaseModel):
    id: int = Field(description="Database UnitType ID")
    type_name: str = Field(description="SDCS Type Name (eg Shelter3 vs Factory share same unit_type within DCS)")
    dcs_type: DCSUnitType = Field(description="DCS Unit Type")


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

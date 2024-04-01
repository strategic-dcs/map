from pydantic import Field

from .core import SDCSBaseModel
from .dcs_unit_type import DCSUnitType


class UnitType(SDCSBaseModel):
    id: int = Field(description="Database UnitType ID")
    type_name: str = Field(description="SDCS Type Name (eg Shelter3 vs Factory share same unit_type within DCS)")
    dcs_type: DCSUnitType = Field(description="DCS Unit Type")
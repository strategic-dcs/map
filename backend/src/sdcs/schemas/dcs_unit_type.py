
from pydantic import Field
from .core import SDCSBaseModel

class DCSUnitType(SDCSBaseModel):
    id: int = Field(description="Database DCSUnitType ID")
    name: str = Field(description="Model name in DCS")

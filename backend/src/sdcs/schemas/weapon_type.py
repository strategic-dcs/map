from pydantic import Field
from .core import SDCSBaseModel


class WeaponType(SDCSBaseModel):
    id: int = Field(description="Weapon Type")
    name: str = Field(description="Weapon Name")
from typing import Optional
from pydantic import BaseModel, Field

from .core import SDCSBaseModel

class Mission(SDCSBaseModel):
    id: int = Field(description="Unique Mission Database ID")
    name: str = Field(description="Unique String Identifier (directory names)")
    display_name: str = Field(description="Display Name")



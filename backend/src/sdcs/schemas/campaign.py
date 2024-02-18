from datetime import datetime
from typing import Optional
from pydantic import Field

from .core import SDCSBaseModel
from .mission import Mission
from .coalition import Coalition

class Campaign(SDCSBaseModel):

    id: int = Field(description="Unique Campaign Identifier")
    mission: Mission = Field(description="Mission Information")
    start: datetime = Field(description="Campaign Start Date/Time")
    end: Optional[datetime] = Field(description="Campaign End Date/Time")
    winner: Optional[Coalition]
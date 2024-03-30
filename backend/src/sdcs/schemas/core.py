from typing import Dict, Any
from pydantic import BaseModel, Extra

class SDCSBaseModel(BaseModel):

    def dict(self, *args, **kwargs) -> Dict[str, Any]:
        _ignored = kwargs.pop('exclude_none')
        return super().dict(*args, exclude_none=True, **kwargs)

    # Handle all the getters
    class Config:
        orm_mode = True
        extra = Extra.forbid
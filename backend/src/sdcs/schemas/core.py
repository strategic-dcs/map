from pydantic import BaseModel, Extra

class SDCSBaseModel(BaseModel):
    # Handle all the getters
    class Config:
        orm_mode = True
        extra = Extra.forbid
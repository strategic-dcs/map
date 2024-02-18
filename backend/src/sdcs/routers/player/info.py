from fastapi import Depends

from . import router

from sdcs.schemas.player import PlayerInfo
from sdcs.db import models, get_db, Session


@router.get("/{player_id}", response_model=PlayerInfo, summary="Get public player information for given ID")
def get_player_info(player_id: int, db: Session = Depends(get_db)):
    return db.query(models.User).get(player_id)
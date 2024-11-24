from typing import Optional
from fastapi import Depends

from sqlalchemy import func, and_

from . import router

from sdcs.schemas.player import PlayerInfo
from sdcs.db import models, get_db, Session
from sdcs.utils import print_query


@router.get("/{player_id}", response_model=Optional[PlayerInfo], summary="Get public player information for given ID")
def get_player_info(player_id: int, campaign_id: int = None, db: Session = Depends(get_db)):

    query = db.query(
        models.User.name,
        models.UserSide.coalition)

    if campaign_id is not None:
        query = query.join(
            models.UserSide,
            and_(
                models.UserSide.user_id == models.User.id,
                models.UserSide.campaign_id == campaign_id,
            ),
            isouter=True
        )

    else:
        # Select the most recent campaign
        query = query.join(
            models.UserSide,
            and_(
                models.UserSide.user_id == models.User.id,
                models.UserSide.campaign_id == db.query(func.max(models.Campaign.id)).as_scalar()
            ),
            isouter=True
        )

    query = query.filter(models.User.id == player_id)

    res = query.first()
    if not res:
        return None

    return {
        "name": res[0],
        "coalition": res[1],
    }
from typing import Optional
from fastapi import Depends, Query

from sqlalchemy import func, and_

from . import router

from sdcs.schemas.player import PlayerInfo
from sdcs.db import models, get_db, Session
from sdcs.utils import print_query


@router.get("/{player_id}", response_model=Optional[PlayerInfo], summary="Get public player information for given ID")
def get_player_info(player_id: int, from_campaign:int = Query(None, alias="from"), to:int = None, db: Session = Depends(get_db)):

    query = db.query(
        models.User.name,
        models.UserSide.coalition)

    latest_campaign = db.query(func.max(models.Campaign.id))

    if to is None:
        to = latest_campaign

    if from_campaign is None:
        from_campaign = to

    if from_campaign == to:
        query = query.join(
            models.UserSide,
            and_(
                models.UserSide.user_id == models.User.id,
                models.UserSide.campaign_id == to,
            ),
            isouter=True
        )
    else:
        # Select the most recent campaign
        query = query.join(
            models.UserSide,
            and_(
                models.UserSide.user_id == models.User.id,
                models.UserSide.campaign_id == latest_campaign
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
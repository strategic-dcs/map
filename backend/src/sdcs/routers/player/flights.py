from fastapi import Depends, Query
from sqlalchemy import func

from . import router

from sdcs.config import settings
from sdcs.schemas.player import PlayerFlight
from sdcs.db import models, get_db, Session


@router.get("/{player_id}/flights", response_model=list[PlayerFlight], summary="Get Flights for a given player")
def get_player_info(player_id: int, from_campaign:int = Query(None, alias="from"), to:int = None, db: Session = Depends(get_db)):
    q = (
        db.query(models.UserFlights)
            .filter(
                models.UserFlights.user_id == player_id,
                models.UserFlights.end != None,
                models.UserFlights.campaign_id > settings.FIRST_CAMPAIGN)
    )

    if to is None:
        to = db.query(func.max(models.Campaign.id))

    if from_campaign is None:
        from_campaign = to

    if from_campaign == to:
        q = q.filter(models.UserFlights.campaign_id == to)
    else:
        q = q.filter(
            models.UserFlights.campaign_id >= from_campaign,
            models.UserFlights.campaign_id <= to
        )

    return q.order_by(models.UserFlights.id.desc()).all()
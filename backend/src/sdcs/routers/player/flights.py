from fastapi import Depends

from . import router

from sdcs.config import settings
from sdcs.schemas.player import PlayerFlight
from sdcs.db import models, get_db, Session


@router.get("/{player_id}/flights", response_model=list[PlayerFlight], summary="Get Flights for a given player")
def get_player_info(player_id: int, campaign_id: int = None, db: Session = Depends(get_db)):
    q = (
        db.query(models.UserFlights)
            .filter(
                models.UserFlights.user_id == player_id,
                models.UserFlights.end != None,
                models.UserFlights.campaign_id > settings.FIRST_CAMPAIGN)
    )

    if campaign_id is not None:
        q = q.filter(models.UserFlights.campaign_id == campaign_id)

    return q.order_by(models.UserFlights.id.desc()).all()
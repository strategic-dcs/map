from fastapi import Depends

from . import router

from sdcs.schemas.weapon_kill import WeaponKill
from sdcs.db import models, get_db, Session


@router.get("/{player_id}/deaths", response_model=list[WeaponKill], summary="Get Flights for a given player")
def get_player_info(player_id: int, campaign_id: int = None, db: Session = Depends(get_db)):

    q = (
        db.query(models.WeaponKill)
            .join(models.Weapon)
            .join(models.UserFlightLegs)
            .join(models.UserFlights)
            .filter(
                models.WeaponKill.target_player_id == player_id,
            )
    )

    if campaign_id is not None:
        q = q.filter(models.UserFlights.campaign_id == campaign_id)

    return q.order_by(models.WeaponKill.id.desc()).all()
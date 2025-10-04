from sqlalchemy import func
from fastapi import Depends, Query

from . import router

from sdcs.schemas.weapon_kill import WeaponKill
from sdcs.db import models, get_db, Session


@router.get("/{player_id}/deaths", response_model=list[WeaponKill], summary="Get Flights for a given player")
def get_player_info(player_id: int, from_campaign:int = Query(None, alias="from"), to:int = None, db: Session = Depends(get_db)):

    q = (
        db.query(models.WeaponKill)
            .join(models.Weapon)
            .join(models.Unit, models.Weapon.unit_id == models.Unit.id)
            .filter(
                models.WeaponKill.target_player_id == player_id,
                models.WeaponKill.superceded == False,
            )
    )

    if to is None:
        to = db.query(func.max(models.Campaign.id))

    if from_campaign is None:
        from_campaign = to

    if from_campaign == to:
        q = q.filter(models.Unit.campaign_id == to)
    else:
        q = q.filter(
            models.Unit.campaign_id >= from_campaign,
            models.Unit.campaign_id <= to
        )

    return q.order_by(models.WeaponKill.id.desc()).all()
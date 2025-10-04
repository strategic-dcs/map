from fastapi import Depends, Query
from sqlalchemy import desc, func, text, case, and_, distinct, extract
from sqlalchemy.orm import aliased

from . import router
from sdcs.config import settings
from sdcs.schemas.player import PlayerSummary, PlayerKill, PlayerModule
from sdcs.db import models, get_db, Session


@router.get("/{player_id}/modules", response_model=list[PlayerModule], summary="Returns player module information")
def get_player_modules(player_id:int, from_campaign:int = Query(None, alias="from"), to:int = None, db: Session = Depends(get_db)):

    query = (
        db
            .query(
                models.UnitType.type_name,
                func.sum(extract('epoch', models.UserFlights.end - models.UserFlights.start)).label('duration'),
            )
            .select_from(models.UserFlights)
            .join(models.User, models.UserFlights.user_id == models.User.id)
            .join(models.Unit, models.UserFlights.unit_id == models.Unit.id)
            .join(models.UnitType)
            .filter(
                models.User.id == player_id,
                models.UserFlights.end != None,
                models.UserFlights.campaign_id > settings.FIRST_CAMPAIGN
            )
    )

    if to is None:
        to = db.query(func.max(models.Campaign.id))

    if from_campaign is None:
        from_campaign = to

    if from_campaign == to:
        query = query.filter(
            models.Unit.campaign_id == to,
        )
    else:
        query = query.filter(
            models.Unit.campaign_id >= from_campaign,
            models.Unit.campaign_id <= to,
        )

    query = (
        query
            .group_by(
                models.UnitType.type_name,
            )
            .order_by(text('duration DESC'))
    )

    #print(query.statement.compile())

    return [dict(zip(['unit_type', 'duration'], x)) for x in query.all()]
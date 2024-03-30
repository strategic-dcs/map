from fastapi import Depends
from sqlalchemy import desc, func, text, case, and_, distinct, extract
from sqlalchemy.orm import aliased

from . import router
from sdcs.schemas.player import PlayerSummary, PlayerKill, PlayerModule
from sdcs.db import models, get_db, Session


@router.get("/{player_id}/modules", response_model=list[PlayerModule], summary="Returns player module information")
def get_player_modules(player_id: int, campaign_id: int = None, db: Session = Depends(get_db)):

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
                models.UserFlights.campaign_id > 48
            )
    )

    if campaign_id is not None:
        query = query.filter(
            models.Unit.campaign_id == campaign_id,
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
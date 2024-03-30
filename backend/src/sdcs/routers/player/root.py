from typing import Union
from sqlalchemy import desc, func, text, case, and_, distinct
from sqlalchemy.orm import aliased
from fastapi import Depends

from . import router

from sdcs.schemas.player import PlayerSummary

from sdcs.db import models, get_db, Session


@router.get("", response_model=list[PlayerSummary], summary="Returns player summary of all time")
def get_player_summary(campaign_id: int = None, db: Session = Depends(get_db)):
    unitK = aliased(models.Unit)
    unitTypeK = aliased(models.UnitType)

    unitT = aliased(models.Unit)
    unitTypeT = aliased(models.UnitType)

    query = (
        db
            .query(
                models.User.id,
                models.User.name,
                (models.UserFlightLegs.end_time - models.UserFlightLegs.start_time).label('duration'),
                func.sum(
                    case(
                        (
                            and_(
                                unitTypeK.unit_class.in_(["AIR", "AIR_RW", "AIR_INTEL"]),
                                unitTypeT.unit_class.in_(["AIR", "AIR_RW", "AIR_INTEL"]),
                                models.WeaponKill.on_ground.is_(False),
                            ), 1
                        ),
                        else_=0)
                    ).label('kills_aa'),
                func.sum(
                    case(
                        (
                            and_(
                                unitTypeK.unit_class.in_(["AIR", "AIR_RW", "AIR_INTEL"]),
                                models.WeaponKill.on_ground.is_(True),
                            ), 1
                        ),
                        else_=0)
                    ).label('kills_ag'),
                func.sum(
                    case(
                        (
                            and_(
                                unitTypeK.unit_class.not_in(["AIR", "AIR_RW", "AIR_INTEL"]),
                                unitTypeT.unit_class.in_(["AIR", "AIR_RW", "AIR_INTEL"]),
                                models.WeaponKill.on_ground.is_(False),
                            ), 1
                        ),
                        else_=0)
                    ).label('kills_ga'),
                func.sum(
                    case(
                        (
                            and_(
                                unitTypeK.unit_class.not_in(["AIR", "AIR_RW", "AIR_INTEL"]),
                                models.WeaponKill.on_ground.is_(True),
                            ), 1
                        ),
                        else_=0)
                    ).label('kills_gg'),
            )
            .select_from(models.UserFlights)
            .join(models.User, models.UserFlights.user_id == models.User.id)
            .join(models.UserFlightLegs, models.UserFlightLegs.flight_id == models.UserFlights.id)
            .join(models.Weapon, models.Weapon.flight_leg_id == models.UserFlightLegs.id, isouter=True)
            .join(models.WeaponKill, isouter=True)
            .join(unitK, models.UserFlights.unit_id == unitK.id, isouter=True)
            .join(unitTypeK, unitK.unit_type_id == unitTypeK.id, isouter=True)
            .join(unitT, models.WeaponKill.target_unit_id == unitT.id, isouter=True)
            .join(unitTypeT, unitT.unit_type_id == unitTypeT.id, isouter=True)
            .filter(
                models.UserFlightLegs.end_time != None
            ))

    if campaign_id is not None:
        query = query.filter(
            unitK.campaign_id == campaign_id,
        )

    query = (
        query
            .group_by(
                models.User.id,
                models.UserFlightLegs.id,
            )
            .order_by(text('duration DESC'))
            .with_labels()
    )

    # Build into our summary
    merge = {}
    for row in query.all():
        if row[0] not in merge:
            merge[row[0]] = {
                "user_id": row[0],
                "user_name": row[1],
                "flights": 1,
                "duration": row[2].total_seconds(),
                "kills": {
                    "a2a": row[3],
                    "a2g": row[4],
                    "g2a": row[5],
                    "g2g": row[6],
                }
            }
            continue

        target = merge[row[0]]
        target["flights"] += 1
        target["duration"] += row[2].total_seconds()
        target["kills"]["a2a"] += row[3]
        target["kills"]["a2g"] += row[4]
        target["kills"]["g2a"] += row[5]
        target["kills"]["g2g"] += row[6]

    return sorted(merge.values(), key=lambda a: a["duration"], reverse=True)


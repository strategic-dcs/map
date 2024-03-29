from typing import Union
from sqlalchemy import desc, func, text, case, and_, distinct
from sqlalchemy.orm import aliased
from fastapi import Depends

from . import router

from sdcs.schemas.kills import Kills
from sdcs.schemas.unit import UnitSummary

from sdcs.db import models, get_db, Session


@router.get("/summary/top10/aa", response_model=list[Kills], summary="Returns top 10 AA")
def get_top10_aa_kills_global(campaign_id: int = None, db: Session = Depends(get_db)):

    unitK = aliased(models.Unit)
    unitTypeK = aliased(models.UnitType)

    unitT = aliased(models.Unit)
    unitTypeT = aliased(models.UnitType)

    rows = ['pilot', 'kills']

    query = (
        db
            .query(
                models.User.name.label('pilot'),
                func.count().label('kills')
            )
            .select_from(models.WeaponKill)
            .join(models.User, models.WeaponKill.kill_player_id == models.User.id)
            .join(models.Weapon)
            .join(unitK, models.Weapon.unit_id == unitK.id)
            .join(unitT, models.WeaponKill.target_unit_id == unitT.id)
            .join(unitTypeK, unitK.unit_type_id == unitTypeK.id)
            .join(unitTypeT, unitT.unit_type_id == unitTypeT.id)
            .filter(
                unitTypeK.unit_class.in_(["AIR", "AIR_RW", "AIR_INTEL"]),
                unitTypeT.unit_class.in_(["AIR", "AIR_RW", "AIR_INTEL"]),
                models.WeaponKill.on_ground.is_(False),
                models.WeaponKill.superceded.is_(False),
                unitK.campaign_id > 48,
            ))

    if campaign_id is not None:
        query = query.filter(
            unitK.campaign_id == campaign_id,
        )

    query = (
        query
            .group_by(
                    models.User.id
            )
            .order_by(text('kills DESC'))
            .limit(10)
    )

    return [dict(zip(rows, row)) for row in query.all()]


@router.get("/summary/top10/ag", response_model=list[Kills], summary="Returns top 10 AG kills of all time")
def get_top10_ag_kills_global(campaign_id: int = None, db: Session = Depends(get_db)):

    unitK = aliased(models.Unit)
    unitTypeK = aliased(models.UnitType)

    unitT = aliased(models.Unit)
    unitTypeT = aliased(models.UnitType)

    rows = ['pilot', 'kills']

    query = (
        db
            .query(
                models.User.name.label('pilot'),
                func.count().label('kills')
            )
            .select_from(models.WeaponKill)
            .join(models.User, models.WeaponKill.kill_player_id == models.User.id)
            .join(models.Weapon)
            .join(unitK, models.Weapon.unit_id == unitK.id)
            .join(unitT, models.WeaponKill.target_unit_id == unitT.id)
            .join(unitTypeK, unitK.unit_type_id == unitTypeK.id)
            .join(unitTypeT, unitT.unit_type_id == unitTypeT.id)
            .filter(
                unitTypeK.unit_class.in_(["AIR", "AIR_RW", "AIR_INTEL"]),
                models.WeaponKill.on_ground.is_(True),
                models.WeaponKill.superceded.is_(False),
                unitK.campaign_id > 48,
            ))

    if campaign_id is not None:
        query = query.filter(
            unitK.campaign_id == campaign_id,
        )

    query = (
        query
            .group_by(
                    models.User.id
            )
            .order_by(text('kills DESC'))
            .limit(10)
    )

    return [dict(zip(rows, row)) for row in query.all()]


@router.get("/summary/top10/gg", response_model=list[Kills], summary="Returns top 10 GG kills of all time")
def get_top10_agg_kills_global(campaign_id: int = None, db: Session = Depends(get_db)):

    unitK = aliased(models.Unit)
    unitTypeK = aliased(models.UnitType)

    unitT = aliased(models.Unit)
    unitTypeT = aliased(models.UnitType)

    rows = ['pilot', 'kills']

    query = (
        db
            .query(
                models.User.name.label('pilot'),
                func.count().label('kills')
            )
            .select_from(models.WeaponKill)
            .join(models.User, models.WeaponKill.kill_player_id == models.User.id)
            .join(models.Weapon)
            .join(unitK, models.Weapon.unit_id == unitK.id)
            .join(unitT, models.WeaponKill.target_unit_id == unitT.id)
            .join(unitTypeK, unitK.unit_type_id == unitTypeK.id)
            .join(unitTypeT, unitT.unit_type_id == unitTypeT.id)
            .filter(
                unitTypeK.unit_class.not_in(["AIR", "AIR_RW", "AIR_INTEL"]),
                models.WeaponKill.on_ground.is_(True),
                models.WeaponKill.superceded.is_(False),
                unitK.campaign_id > 48,
            ))

    if campaign_id is not None:
        query = query.filter(
            unitK.campaign_id == campaign_id,
        )

    query = (
        query
            .group_by(
                    models.User.id
            )
            .order_by(text('kills DESC'))
            .limit(10)
    )

    return [dict(zip(rows, row)) for row in query.all()]


@router.get("/summary/top10/ga", response_model=list[Kills], summary="Returns top 10 GA kills of all time")
def get_top10_agg_kills_global(campaign_id: int = None, db: Session = Depends(get_db)):

    unitK = aliased(models.Unit)
    unitTypeK = aliased(models.UnitType)

    unitT = aliased(models.Unit)
    unitTypeT = aliased(models.UnitType)

    rows = ['pilot', 'kills']

    query = (
        db
            .query(
                models.User.name.label('pilot'),
                func.count().label('kills')
            )
            .select_from(models.WeaponKill)
            .join(models.User, models.WeaponKill.kill_player_id == models.User.id)
            .join(models.Weapon)
            .join(unitK, models.Weapon.unit_id == unitK.id)
            .join(unitT, models.WeaponKill.target_unit_id == unitT.id)
            .join(unitTypeK, unitK.unit_type_id == unitTypeK.id)
            .join(unitTypeT, unitT.unit_type_id == unitTypeT.id)
            .filter(
                unitTypeK.unit_class.not_in(["AIR", "AIR_RW", "AIR_INTEL"]),
                unitTypeT.unit_class.in_(["AIR", "AIR_RW", "AIR_INTEL"]),
                models.WeaponKill.on_ground.is_(False),
                models.WeaponKill.superceded.is_(False),
                unitK.campaign_id > 48,
            ))

    if campaign_id is not None:
        query = query.filter(
            unitK.campaign_id == campaign_id,
        )

    query = (
        query
            .group_by(
                    models.User.id
            )
            .order_by(text('kills DESC'))
            .limit(10)
    )

    return [dict(zip(rows, row)) for row in query.all()]


@router.get("/summary/top10/units", response_model=list[UnitSummary], summary="Returns top 10 GA kills of all time")
def get_top10_units_by_duration(campaign_id: int = None, db: Session = Depends(get_db)):

    unitK = aliased(models.Unit)
    unitTypeK = aliased(models.UnitType)

    unitT = aliased(models.Unit)
    unitTypeT = aliased(models.UnitType)

    query = (
        db
            .query(
                unitTypeK.type_name,
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
            .join(models.UserFlightLegs, models.UserFlightLegs.flight_id == models.UserFlights.id)
            .join(models.Weapon, models.Weapon.flight_leg_id == models.UserFlightLegs.id, isouter=True)
            .join(models.WeaponKill, isouter=True)
            .join(unitK, models.UserFlights.unit_id == unitK.id, isouter=True)
            .join(unitTypeK, unitK.unit_type_id == unitTypeK.id, isouter=True)
            .join(unitT, models.WeaponKill.target_unit_id == unitT.id, isouter=True)
            .join(unitTypeT, unitT.unit_type_id == unitTypeT.id, isouter=True)
            .filter(
                models.UserFlightLegs.end_time != None,
                models.WeaponKill.superceded.is_(False),
                unitK.campaign_id > 48,
            ))

    if campaign_id is not None:
        query = query.filter(
            unitK.campaign_id == campaign_id,
        )

    query = (
        query
            .group_by(
                unitTypeK.type_name,
                models.UserFlightLegs.id,
            )
            .order_by(text('duration DESC'))
            .with_labels()
    )

    # print(str(query.statement.compile(compile_kwargs={"literal_binds": True})))

    # Build into our summary
    merge = {}
    for row in query.all():
        if row[0] not in merge:
            merge[row[0]] = {
                "unit_type": row[0],
                "flights": 1,
                "duration": row[1].total_seconds(),
                "kills": {
                    "a2a": row[2],
                    "a2g": row[3],
                    "g2a": row[4],
                    "g2g": row[5],
                }
            }
            continue

        target = merge[row[0]]
        target["flights"] += 1
        target["duration"] += row[1].total_seconds()
        target["kills"]["a2a"] += row[2]
        target["kills"]["a2g"] += row[3]
        target["kills"]["g2a"] += row[4]
        target["kills"]["g2g"] += row[5]

    return sorted(merge.values(), key=lambda a: a["duration"], reverse=True)

from fastapi import Depends
from sqlalchemy import desc, func, text, case, and_, distinct, extract
from sqlalchemy.orm import aliased

from . import router
from sdcs.schemas.player import PlayerSummary, PlayerKill, PlayerModule
from sdcs.db import models, get_db, Session


def get_player_summary(db: Session, campaign_id: int = None):

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
                models.UserFlightLegs.end_time != None,
                models.UserFlights.campaign_id > 48
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


def get_player_modules(db: Session, player_id: int, campaign_id: int = None):

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

    print(query.statement.compile())

    return [dict(zip(['unit_type', 'duration'], x)) for x in query.all()]


def get_player_kills(db: Session, player_id: int, campaign_id: int = None):

    userT = aliased(models.User)

    unitK = aliased(models.Unit)
    unitTypeK = aliased(models.UnitType)
    dcsUnitTypeK = aliased(models.DcsUnitType)

    unitT = aliased(models.Unit)
    unitTypeT = aliased(models.UnitType)
    dcsUnitTypeT = aliased(models.DcsUnitType)

    fields = (
        'id', 'kill_at',
        'weapon_name',
        'killer_unit_type',
        'target_unit_type',
        'target_on_ground',
        'target_player_name',
        'assoc_method'
    )

    query = (
        db
            .query(
                models.WeaponKill.id,
                models.WeaponKill.kill_at,
                models.Weapon.weapon_name,
                dcsUnitTypeK.name,
                unitTypeT.type_name,
                models.WeaponKill.on_ground,
                userT.name,
                models.WeaponKill.assoc_method,
            )
            .select_from(models.WeaponKill)
            .join(models.Weapon, models.WeaponKill.weapon_id == models.Weapon.id)
            .join(models.UserFlightLegs, models.Weapon.flight_leg_id == models.UserFlightLegs.id)
            .join(models.UserFlights, models.UserFlightLegs.flight_id == models.UserFlights.id)
            .join(userT, models.WeaponKill.target_player_id == userT.id, isouter=True)
            .join(unitK, models.UserFlights.unit_id == unitK.id)
            .join(unitTypeK, unitK.unit_type_id == unitTypeK.id)
            .join(dcsUnitTypeK, unitTypeK.dcs_type_id == dcsUnitTypeK.id)
            .join(unitT, models.WeaponKill.target_unit_id == unitT.id)
            .join(unitTypeT, unitT.unit_type_id == unitTypeT.id)
            .filter(
                models.WeaponKill.kill_player_id == player_id,
                models.WeaponKill.target_unit_id != None,
                models.WeaponKill.superceded.is_(False)
            ))

    if campaign_id is not None:
        query = query.filter(
            unitK.campaign_id == campaign_id,
        )

    query = (
        query
            .order_by(text('kill_at DESC'))
    )

    return [dict(zip(fields, x)) for x in query.all()]


@router.get("/{campaign_id}/players", response_model=list[PlayerSummary], summary="Returns player summary for a given campaign_id")
def get_top10_units_by_duration_for_campaign(campaign_id: int, db: Session = Depends(get_db)):
    return get_player_summary(db, campaign_id)


@router.get("/players", response_model=list[PlayerSummary], summary="Returns player summary of all time")
def get_top10_units_by_duration(db: Session = Depends(get_db)):
    return get_player_summary(db)


@router.get("/{campaign_id}/players/{player_id}/kills", response_model=list[PlayerKill], summary="Returns Player Kills for Campaign")
def get_player_kills_for_campaign(player_id: int, campaign_id: int, db: Session = Depends(get_db)):
    return get_player_kills(db, player_id, campaign_id)


@router.get("/players/{player_id}/kills", response_model=list[PlayerKill], summary="Returns Player Kills for Campaign")
def get_player_kills_for_campaign(player_id: int, db: Session = Depends(get_db)):
    return get_player_kills(db, player_id)


@router.get("/{campaign_id}/players/{player_id}/modules", response_model=list[PlayerModule], summary="Returns Player Kills for Campaign")
def get_player_module_time_for_campaign(player_id: int, campaign_id: int = None, db: Session = Depends(get_db)):
    return get_player_modules(db, player_id, campaign_id)


@router.get("/players/{player_id}/modules", response_model=list[PlayerModule], summary="Returns Player Kills for Campaign")
def get_player_module_time(player_id: int, db: Session = Depends(get_db)):
    return get_player_modules(db, player_id)

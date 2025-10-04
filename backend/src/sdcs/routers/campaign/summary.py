from sqlalchemy import func, text, case, and_
from sqlalchemy.orm import aliased
from fastapi import Depends, Query

from . import router

from sdcs.schemas.unit import UnitSummary
from sdcs.config import settings

from sdcs.db import models, get_db, Session


@router.get("/summary/units", response_model=list[UnitSummary], summary="Returns top 10 GA kills of all time")
def get_units_by_duration(from_campaign:int = Query(None, alias="from"), to:int = None, db:Session = Depends(get_db)):

    unitK = aliased(models.Unit)
    unitTypeK = aliased(models.UnitType)

    unitT = aliased(models.Unit)
    unitTypeT = aliased(models.UnitType)

    rows = ['type_name', 'duration', 'aa', 'aa_tk', 'ag', 'ag_tk', 'ga', 'ga_tk', 'gg', 'gg_tk', 'suicide', 'is_pvp']

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
                                unitT.coalition != unitK.coalition,
                                unitT.id != unitK.id,
                            ), 1
                        ),
                        else_=0)
                    ).label('kills_aa'),
                func.sum(
                    case(
                        (
                            and_(
                                unitTypeK.unit_class.in_(["AIR", "AIR_RW", "AIR_INTEL"]),
                                unitTypeT.unit_class.in_(["AIR", "AIR_RW", "AIR_INTEL"]),
                                models.WeaponKill.on_ground.is_(False),
                                unitT.coalition == unitK.coalition,
                                unitT.id != unitK.id,
                            ), 1
                        ),
                        else_=0)
                    ).label('kills_aa_tk'),
                func.sum(
                    case(
                        (
                            and_(
                                unitTypeK.unit_class.in_(["AIR", "AIR_RW", "AIR_INTEL"]),
                                models.WeaponKill.on_ground.is_(True),
                                unitT.coalition != unitK.coalition,
                                unitT.id != unitK.id,
                            ), 1
                        ),
                        else_=0)
                    ).label('kills_ag'),
                func.sum(
                    case(
                        (
                            and_(
                                unitTypeK.unit_class.in_(["AIR", "AIR_RW", "AIR_INTEL"]),
                                models.WeaponKill.on_ground.is_(True),
                                unitT.coalition == unitK.coalition,
                                unitT.id != unitK.id,
                            ), 1
                        ),
                        else_=0)
                    ).label('kills_ag_tk'),
                func.sum(
                    case(
                        (
                            and_(
                                unitTypeK.unit_class.not_in(["AIR", "AIR_RW", "AIR_INTEL"]),
                                unitTypeT.unit_class.in_(["AIR", "AIR_RW", "AIR_INTEL"]),
                                models.WeaponKill.on_ground.is_(False),
                                unitT.coalition != unitK.coalition,
                                unitT.id != unitK.id,
                            ), 1
                        ),
                        else_=0)
                    ).label('kills_ga'),
                func.sum(
                    case(
                        (
                            and_(
                                unitTypeK.unit_class.not_in(["AIR", "AIR_RW", "AIR_INTEL"]),
                                unitTypeT.unit_class.in_(["AIR", "AIR_RW", "AIR_INTEL"]),
                                models.WeaponKill.on_ground.is_(False),
                                unitT.coalition == unitK.coalition,
                                unitT.id != unitK.id,
                            ), 1
                        ),
                        else_=0)
                    ).label('kills_ga_tk'),
                func.sum(
                    case(
                        (
                            and_(
                                unitTypeK.unit_class.not_in(["AIR", "AIR_RW", "AIR_INTEL"]),
                                models.WeaponKill.on_ground.is_(True),
                                unitT.coalition != unitK.coalition,
                                unitT.id != unitK.id,
                            ), 1
                        ),
                        else_=0)
                    ).label('kills_gg'),
                func.sum(
                    case(
                        (
                            and_(
                                unitTypeK.unit_class.not_in(["AIR", "AIR_RW", "AIR_INTEL"]),
                                models.WeaponKill.on_ground.is_(True),
                                unitT.coalition == unitK.coalition,
                                unitT.id != unitK.id,
                            ), 1
                        ),
                        else_=0)
                    ).label('kills_gg_tk'),
                func.sum(
                    case(
                        (
                            and_(
                                unitT.id == unitK.id,
                            ), 1
                        ),
                        else_=0)
                    ).label('kills_suicide'),
                models.WeaponKill.target_player_id.is_not(None).label('is_pvp'),
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
                models.UserFlightLegs.committed.is_(True),
                models.WeaponKill.superceded.is_(False),
                unitK.campaign_id > settings.FIRST_CAMPAIGN,
            ))


    # Pick our latest campaign for coalition details
    latest_campaign = db.query(func.max(models.Campaign.id))

    if to is None:
        to = latest_campaign

    if from_campaign is None:
        from_campaign = to

    if from_campaign == to:
        query = query.filter(
            unitK.campaign_id == to,
        )
    else:
        query = query.filter(
            unitK.campaign_id >= from_campaign,
            unitK.campaign_id <= to,
        )

    query = (
        query
            .group_by(
                unitTypeK.type_name,
                models.UserFlightLegs.id,
                'is_pvp',
            )
            .order_by(text('duration DESC'))
            .with_labels()
    )

    # print(str(query.statement.compile(compile_kwargs={"literal_binds": True})))

    # Build into our summary
    merge = {}
    for row in query.all():
        row = dict(zip(rows, row))

        if row['type_name'] not in merge:
            merge[row['type_name']] = {
                "unit_type": row['type_name'],
                "flights": 0,
                "duration": 0,
                "kills": {}
            }

        # Add up
        target = merge[row['type_name']]
        target["flights"] += 1
        target["duration"] += row['duration'].total_seconds()

        kill_target = 'player' if row['is_pvp'] else 'ai'

        for kt in ['aa', 'ag', 'ga', 'gg']:
            for tk in ['', '_tk']:
                field = f"{kt}{tk}"
                if field not in row or not row[field]:
                    continue

                if kt not in target["kills"]:
                    target["kills"][kt] = {}

                if tk or kt == "suicide":
                    kill_target = 'tk'

                if kill_target not in target["kills"][kt]:
                    target["kills"][kt][kill_target] = 0

                target["kills"][kt][kill_target] += row[field]

        if row['suicide']:
            target["kills"]['suicide'] = row['suicide']

    return sorted(merge.values(), key=lambda a: a["duration"], reverse=True)

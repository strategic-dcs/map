from sqlalchemy import func, text, case, and_
from sqlalchemy.orm import aliased
from fastapi import Depends

from . import router

from sdcs.schemas.unit import UnitSummary

from sdcs.db import models, get_db, Session


@router.get("/summary/units", response_model=list[UnitSummary], summary="Returns top 10 GA kills of all time")
def get_units_by_duration(campaign_id: int = None, db: Session = Depends(get_db)):

    unitK = aliased(models.Unit)
    unitTypeK = aliased(models.UnitType)

    unitT = aliased(models.Unit)
    unitTypeT = aliased(models.UnitType)

    rows = ['type_name', 'duration', 'aa', 'ag', 'ga', 'gg', 'is_pvp']

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

        kill_target = 'pvp' if row['is_pvp'] else 'ai'

        for kt in ['aa', 'ag', 'ga', 'gg']:
            if not row[kt]:
                continue

            if kt not in target["kills"]:
                target["kills"][kt] = {}

            if kill_target not in target["kills"][kt]:
                target["kills"][kt][kill_target] = 0

            target["kills"][kt][kill_target] += row[kt]

    return sorted(merge.values(), key=lambda a: a["duration"], reverse=True)

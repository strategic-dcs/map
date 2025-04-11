from typing import Union
from sqlalchemy import desc, func, text, case, and_, distinct, or_
from sqlalchemy.orm import aliased
from fastapi import Depends

from . import router

from sdcs.config import settings
from sdcs.schemas.player import PlayerSummary
from sdcs.utils import print_query

from sdcs.db import models, get_db, Session


@router.get("", response_model=list[PlayerSummary], summary="Returns player summary of all time")
def get_player_summary(campaign_id: int = None, db: Session = Depends(get_db)):
    unitK = aliased(models.Unit)
    unitTypeK = aliased(models.UnitType)

    unitT = aliased(models.Unit)
    unitTypeT = aliased(models.UnitType)

    rows = ['id', 'name', 'duration', 'aa', 'aa_tk', 'ag', 'ag_tk', 'ga', 'ga_tk', 'gg', 'gg_tk', 'suicide', 'is_pvp', 'user_side', 'vanity_points']

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

                func.sum(
                    case(
                        (
                            or_(
                                models.UserFlightLegs.end_airbase_id.is_not(None),
                                models.UserFlightLegs.end_farp_id.is_not(None),
                            ), models.WeaponKill.vanity_points
                        ),
                        else_=0)
                    ).label('vanity_points'),


                models.WeaponKill.target_player_id.is_not(None).label('is_pvp'),
                models.UserSide.coalition.label('user_side'),
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
                models.UserFlightLegs.committed.is_(True),
                models.WeaponKill.superceded.is_(False),
                unitK.campaign_id > settings.FIRST_CAMPAIGN,
            ))

    if campaign_id is not None:
        query = query.filter(
            unitK.campaign_id == campaign_id,
        )

        # We join on player side
        query = query.join(
            models.UserSide,
            and_(
                models.UserSide.campaign_id == campaign_id,
                models.UserSide.user_id == models.User.id,
            ),
            isouter=True)
    else:
        # Select the most recent campaign
        query = query.join(
            models.UserSide,
            and_(
                models.UserSide.user_id == models.User.id,
                models.UserSide.campaign_id == db.query(func.max(models.Campaign.id))
            ),
            isouter=True
        )

    query = (
        query
            .group_by(
                models.User.id,
                models.UserFlightLegs.id,
                'is_pvp',
                'user_side',
            )
            .order_by(text('duration DESC'))
    )

    # print_query(query)

    # Build into our summary
    merge = {}
    for row in query.all():
        row = dict(zip(rows, row))

        if row['id'] not in merge:
            merge[row['id']] = {
                "user_id": row['id'],
                "user_name": row['name'],
                "user_side": row['user_side'],
                "flights": 0,
                "duration": 0,
                "kills": {},
                "vanity_points": 0
            }

        target = merge[row['id']]
        target["flights"] += 1
        target["duration"] += row['duration'].total_seconds()
        target["vanity_points"] += row['vanity_points']

        kill_target = 'player' if row['is_pvp'] else 'ai'

        for kt in ['aa', 'ag', 'ga', 'gg']:
            for tk in ['', '_tk']:
                field = f"{kt}{tk}"
                if field not in row or not row[field]:
                    continue

                if kt not in target["kills"]:
                    target["kills"][kt] = {}

                if tk:
                    kill_target = 'tk'

                if kill_target not in target["kills"][kt]:
                    target["kills"][kt][kill_target] = 0

                target["kills"][kt][kill_target] += row[field]

        if row['suicide']:
            target["kills"]['suicide'] = row['suicide']

    return sorted(merge.values(), key=lambda a: a["duration"], reverse=True)


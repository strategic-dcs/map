from typing import Union
from sqlalchemy import desc, func, text, case, and_, or_, distinct
from sqlalchemy.orm import aliased
from fastapi import Depends

from . import router

from sdcs.schemas.weapon import WeaponSummary

from sdcs.db import models, get_db, Session


def get_weapon_information(db: Session, campaign_id: int = None, dcs_type_id: int = None, weapon_type_id: int = None):
    unitK = aliased(models.Unit)
    unitTypeK = aliased(models.UnitType)
    dcsTypeK = aliased(models.DcsUnitType)

    unitT = aliased(models.Unit)
    unitTypeT = aliased(models.UnitType)

    # For weapons we just want the number deployed, we can't do shots fired since it varies bsaed on weapon
    rows = ['dcs_type_id', 'weapon_type_id', 'shots', 'aa', 'aa_player', 'ag', 'ag_player', 'ga', 'ga_player', 'gg', 'gg_player']

    query = (
        db
            .query(
                dcsTypeK.id,
                models.Weapon.weapon_type_id,
                func.count(models.Weapon.id).label('shots'),
                func.sum(
                    case(
                        (
                            and_(
                                unitTypeK.unit_class.in_(["AIR", "AIR_RW", "AIR_INTEL"]),
                                unitTypeT.unit_class.in_(["AIR", "AIR_RW", "AIR_INTEL"]),
                                models.WeaponKill.on_ground.is_(False),
                                unitT.coalition != unitK.coalition,
                                models.WeaponKill.target_player_id.is_(None),
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
                                unitT.coalition != unitK.coalition,
                                models.WeaponKill.target_player_id.is_not(None),
                            ), 1
                        ),
                        else_=0)
                    ).label('kills_aa_player'),
                func.sum(
                    case(
                        (
                            and_(
                                unitTypeK.unit_class.in_(["AIR", "AIR_RW", "AIR_INTEL"]),
                                models.WeaponKill.on_ground.is_(True),
                                unitT.coalition != unitK.coalition,
                                models.WeaponKill.target_player_id.is_(None),
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
                                unitT.coalition != unitK.coalition,
                                models.WeaponKill.target_player_id.is_not(None),
                            ), 1
                        ),
                        else_=0)
                    ).label('kills_ag_player'),
                func.sum(
                    case(
                        (
                            and_(
                                unitTypeK.unit_class.not_in(["AIR", "AIR_RW", "AIR_INTEL"]),
                                unitTypeT.unit_class.in_(["AIR", "AIR_RW", "AIR_INTEL"]),
                                models.WeaponKill.on_ground.is_(False),
                                unitT.coalition != unitK.coalition,
                                models.WeaponKill.target_player_id.is_(None),
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
                                unitT.coalition != unitK.coalition,
                                models.WeaponKill.target_player_id.is_not(None),
                            ), 1
                        ),
                        else_=0)
                    ).label('kills_ga_player'),
                func.sum(
                    case(
                        (
                            and_(
                                unitTypeK.unit_class.not_in(["AIR", "AIR_RW", "AIR_INTEL"]),
                                models.WeaponKill.on_ground.is_(True),
                                unitT.coalition != unitK.coalition,
                                models.WeaponKill.target_player_id.is_(None),
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
                                unitT.coalition != unitK.coalition,
                                models.WeaponKill.target_player_id.is_not(None),
                            ), 1
                        ),
                        else_=0)
                    ).label('kills_gg_player'),
            )
            .select_from(models.Weapon)
            .join(models.WeaponKill, and_(
                models.WeaponKill.weapon_id == models.Weapon.id,
                models.WeaponKill.superceded.is_(False),
                ), isouter=True)
            .join(unitK, models.Weapon.unit_id == unitK.id)
            .join(unitTypeK, unitK.unit_type_id == unitTypeK.id)
            .join(dcsTypeK, unitTypeK.dcs_type_id == dcsTypeK.id)
            .join(unitT, models.WeaponKill.target_unit_id == unitT.id, isouter=True)
            .join(unitTypeT, unitT.unit_type_id == unitTypeT.id, isouter=True)
            .filter(
                models.WeaponKill.kill_player_id.is_(None),
                unitK.user_id.is_(None),
                unitK.campaign_id > 48,
                or_(
                    models.WeaponKill.target_unit_id.is_(None),
                    models.Weapon.unit_id != models.WeaponKill.target_unit_id
                )
            ))

    if campaign_id is not None:
        query = query.filter(unitK.campaign_id == campaign_id)

    if weapon_type_id is not None:
        query = query.filter(models.Weapon.weapon_type_id == weapon_type_id)

    if dcs_type_id is not None:
        query = query.filter(dcsTypeK.id == dcs_type_id)


    query = (
        query
            .group_by(
                dcsTypeK.id,
                models.Weapon.weapon_type_id,
            )
            .order_by(text('shots DESC'))
    )

    # Build into our summary
    output = []
    unit_cache = {}
    weapon_cache = {}

    id = 0
    for row in query.all():
        row = dict(zip(rows, row))
        id += 1

        if row["dcs_type_id"] not in unit_cache:
            unit_cache[row["dcs_type_id"]] = db.query(models.DcsUnitType).get(row["dcs_type_id"])

        if row["weapon_type_id"] not in weapon_cache:
            weapon_cache[row["weapon_type_id"]] = db.query(models.WeaponType).get(row["weapon_type_id"])

        target = {
            'unit_type': unit_cache[row["dcs_type_id"]],
            'weapon_type': weapon_cache[row["weapon_type_id"]],
            'shots': row['shots'],
            'kills': {}
        }

        for kt in ['aa', 'ag', 'ga', 'gg']:
            for tk in ['', '_player']:
                field = f"{kt}{tk}"
                if field not in row or not row[field]:
                    continue

                if kt not in target["kills"]:
                    target["kills"][kt] = {}

                kill_target = 'ai' if not tk else 'player'
                target["kills"][kt][kill_target] = row[field]

        # Remove optional nulls
        if 'team_kill' in target and not target['team_kill']:
            del target['team_kill']

        output.append(target)
    return output


@router.get("", response_model=list[WeaponSummary], summary="Returns ai unit summary")
def get_weapon_information_response(campaign_id: int = None, db: Session = Depends(get_db)):

    return sorted(
        get_weapon_information(db, campaign_id),
        key=lambda a: a["shots"], reverse=True)

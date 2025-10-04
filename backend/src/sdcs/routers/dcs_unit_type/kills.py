
from fastapi import Depends, Query
from sqlalchemy import desc, func, text, case, and_, or_, distinct, extract
from sqlalchemy.orm import aliased

from . import router
from sdcs.db import models, get_db, Session
from sdcs.schemas.unit import AIUnitKill


@router.get("/{dcs_unit_type_id}/kills", response_model=list[AIUnitKill], summary="Get unit type information by ID")
def get_unit_type_kills(dcs_unit_type_id: int, from_campaign:int = Query(None, alias="from"), to:int = None, weapon_id: int = None, db: Session = Depends(get_db)):

    userT = aliased(models.User)

    unitK = aliased(models.Unit)
    unitTypeK = aliased(models.UnitType)
    dcsUnitTypeK = aliased(models.DcsUnitType)

    unitT = aliased(models.Unit)
    unitTypeT = aliased(models.UnitType)

    fields = (
        'id',
        'kill_at',
        'weapon_type',
        'target_unit_type',
        'target_on_ground',
        'target_player_name',
        'assoc_method',
        'team_kill',
    )

    query = (
        db
            .query(
                models.WeaponKill.id,
                models.WeaponKill.kill_at,
                models.Weapon.weapon_type_id,
                unitTypeT.type_name,
                models.WeaponKill.on_ground,
                userT.name,
                models.WeaponKill.assoc_method,
                (unitT.coalition == unitK.coalition).label('team_kill'),
            )
            .select_from(models.WeaponKill)
            .join(models.Weapon, models.WeaponKill.weapon_id == models.Weapon.id)
            .join(unitK, models.Weapon.unit_id == unitK.id)
            .join(unitTypeK, unitK.unit_type_id == unitTypeK.id)
            .join(dcsUnitTypeK, unitTypeK.dcs_type_id == dcsUnitTypeK.id)
            .join(unitT, models.WeaponKill.target_unit_id == unitT.id)
            .join(userT, models.WeaponKill.target_player_id == userT.id, isouter=True)
            .join(unitTypeT, unitT.unit_type_id == unitTypeT.id)
            .filter(
                dcsUnitTypeK.id == dcs_unit_type_id,
                models.WeaponKill.kill_player_id.is_(None),
                models.WeaponKill.superceded.is_(False),
                models.Weapon.unit_id != models.WeaponKill.target_unit_id
            ))

    # Undefined campaign, pick the last
    if to is None:
        to = db.query(func.max(models.Campaign.id))

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

    if weapon_id is not None:
        query = query.filter(models.Weapon.weapon_type_id == weapon_id)

    query = (
        query
            .order_by(text('kill_at DESC'))
    )

    output = [dict(zip(fields, x)) for x in query.all()]
    weapon_cache = {}
    for row in output:
        # Replace weapon type with data
        if row["weapon_type"] not in weapon_cache:
            weapon_cache[row["weapon_type"]] = db.query(models.WeaponType).get(row["weapon_type"])
        row["weapon_type"] = weapon_cache[row["weapon_type"]]

    return output


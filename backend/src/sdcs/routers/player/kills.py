from fastapi import Depends
from sqlalchemy import desc, func, text, case, and_, distinct, extract
from sqlalchemy.orm import aliased

from . import router
from sdcs.schemas.player import PlayerSummary, PlayerKill, PlayerModule
from sdcs.db import models, get_db, Session



@router.get("/{player_id}/kills", response_model=list[PlayerKill], summary="Get Kills for a given player")
def get_player_kills(player_id: int, campaign_id: int = None, db: Session = Depends(get_db)):

    userT = aliased(models.User)

    unitK = aliased(models.Unit)
    unitTypeK = aliased(models.UnitType)
    dcsUnitTypeK = aliased(models.DcsUnitType)

    unitT = aliased(models.Unit)
    unitTypeT = aliased(models.UnitType)

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


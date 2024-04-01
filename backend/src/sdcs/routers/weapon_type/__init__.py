from fastapi import APIRouter, Depends
from sdcs.schemas.weapon import WeaponType
from sdcs.db import models, get_db, Session

router = APIRouter(
    prefix="/weapon_type",
    tags=["weapon_type"],
    redirect_slashes=False,
)


@router.get("", response_model=list[WeaponType], summary="All Weapon Types")
def get_all_unit_types(db: Session = Depends(get_db)):
    return db.query(models.WeaponType).all()


@router.get("/{weapon_type_id}", response_model=WeaponType, summary="Get unit type information by ID")
def get_all_unit_types(weapon_type_id: int, db: Session = Depends(get_db)):
    return db.query(models.WeaponType).get(weapon_type_id)

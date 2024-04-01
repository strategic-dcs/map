from fastapi import Depends
from sdcs.schemas.dcs_unit_type import DCSUnitType
from sdcs.db import models, get_db, Session

from . import router

@router.get("", response_model=list[DCSUnitType], summary="All Unit Types")
def get_all_unit_types(db: Session = Depends(get_db)):
    return db.query(models.DcsUnitType).all()


@router.get("/{dcs_unit_type_id}", response_model=DCSUnitType, summary="Get unit type information by ID")
def get_all_unit_types(dcs_unit_type_id: int, db: Session = Depends(get_db)):
    return db.query(models.DcsUnitType).get(dcs_unit_type_id)

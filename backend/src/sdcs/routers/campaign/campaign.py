from sqlalchemy import desc
from fastapi import Depends

from . import router

from sdcs.schemas.campaign import Campaign

from sdcs.db import models, get_db, Session


@router.get("", response_model=list[Campaign], summary="Retruns a list all campaigns")
def get_campaigns(db: Session = Depends(get_db)):
    return (
        db.query(models.Campaign)
            .filter(
                models.Campaign.id > 48
            )
            .order_by(desc(models.Campaign.id)).all()
    )


@router.get("/current", response_model=Campaign,  summary="Returns the current campaign")
def get_current_campaign(db: Session = Depends(get_db)):
    return db.query(models.Campaign).filter(
        models.Campaign.end == None
    ).order_by(desc(models.Campaign.id)).first()

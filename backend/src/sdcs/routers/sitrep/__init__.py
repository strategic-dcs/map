from fastapi import APIRouter

router = APIRouter(
    prefix="/sitrep",
    tags=["sitrep"],
    redirect_slashes=False,
)

from .sitrep import *
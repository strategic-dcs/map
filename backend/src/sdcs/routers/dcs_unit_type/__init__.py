from fastapi import APIRouter

router = APIRouter(
    prefix="/dcs_unit_type",
    tags=["dcs_unit_type"],
    redirect_slashes=False,
)

from .root import *
from .kills import *
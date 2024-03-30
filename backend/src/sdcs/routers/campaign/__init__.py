from fastapi import APIRouter

router = APIRouter(
    prefix="/campaign",
    tags=["campaign"],
    redirect_slashes=False,
)

from .summary import *
from .campaign import *
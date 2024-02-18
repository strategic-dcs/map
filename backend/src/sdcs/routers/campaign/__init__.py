from fastapi import APIRouter

router = APIRouter(
    prefix="/campaign",
    tags=["campaign"],
    redirect_slashes=False,
)

from .player import *
from .campaign import *
from .top10 import *
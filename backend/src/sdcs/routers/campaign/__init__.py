from fastapi import APIRouter

router = APIRouter(
    prefix="/campaign",
    tags=["campaign"],
    redirect_slashes=False,
)

# from .player import *
from .summary import *
from .campaign import *
from fastapi import APIRouter

router = APIRouter(
    prefix="/player",
    tags=["player"],
    redirect_slashes=False,
)

from .summary import *
from .info import *
from .flights import *
from .deaths import *
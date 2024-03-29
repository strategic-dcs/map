from fastapi import APIRouter

router = APIRouter(
    prefix="/player",
    tags=["player"],
    redirect_slashes=False,
)

from .root import *
from .flights import *
from .deaths import *
from .kills import *
from .modules import *
from .info import *
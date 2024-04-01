from fastapi import APIRouter

router = APIRouter(
    prefix="/weapon",
    tags=["weapon"],
    redirect_slashes=False,
)

from .root import *
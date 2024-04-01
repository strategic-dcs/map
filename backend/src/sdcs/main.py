from fastapi import Request, Response, FastAPI
from fastapi.responses import JSONResponse
from fastapi_discord import Unauthorized
from fastapi_discord.exceptions import ClientSessionNotInitialized

from .discord import router as discord_router
from .db import get_engine, get_session_maker
from . import routers

tags_metadata = [
    {
        "name": "sitrep",
        "description": "For live map display",
    },
    {
        "name": "campaign",
        "description": "Campaign Information",
    },
    {
        "name": "player",
        "description": "Player Information",
    },
    {
        "name": "weapon",
        "description": "Weapon Usage Information",
    },
    {
        "name": "dcs_unit_type",
        "description": "DCS Unit Type Information",
    },
    {
        "name": "weapon_type",
        "description": "DCS Weapon Type",
    },
]

app = FastAPI(
    title="Strategic DCS API",
    openapi_tags=tags_metadata,
    swagger_ui_parameters={
        "defaultModelsExpandDepth": -1
    })


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    response = Response("Internal server error", status_code=500)
    try:
        request.state.db = app.state.db_session()
        response = await call_next(request)
    finally:
        db = request.state._state.get('db')
        if db:
            request.state.db.close()
    return response



app.state.engine = get_engine()
app.state.db_session = get_session_maker(app.state.engine)


app.include_router(discord_router, prefix="/api/auth", tags=["Auth"])
app.include_router(routers.sitrep)
app.include_router(routers.campaign)
app.include_router(routers.player)
app.include_router(routers.weapon)
app.include_router(routers.dcs_unit_type)
app.include_router(routers.weapon_type)

@app.exception_handler(Unauthorized)
async def unauthorized_error_handler(_, __):
    return JSONResponse({"error": "Unauthorized"}, status_code=401)

@app.exception_handler(ClientSessionNotInitialized)
async def client_session_error_handler(_, e: ClientSessionNotInitialized):
    print(e)
    return JSONResponse({"error": "Internal Error"}, status_code=500)

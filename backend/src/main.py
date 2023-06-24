from typing import List

from fastapi import Request, FastAPI, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware
from config import settings
from fastapi_discord import Unauthorized
from fastapi_discord.exceptions import ClientSessionNotInitialized
from fastapi_discord.models import GuildPreview, Guild

from auth.discord import router as auth_router, discord

app = FastAPI()
# app.mount("/static", StaticFiles(directory="/../static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_origin_regex=settings.CORS_ORIGINS_REGEX,
    allow_credentials=True,
    allow_methods=("GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"),
    allow_headers=settings.CORS_HEADERS,
)

app.include_router(auth_router, prefix="/api/auth", tags=["Auth"])

@app.exception_handler(Unauthorized)
async def unauthorized_error_handler(_, __):
    return JSONResponse({"error": "Unauthorized"}, status_code=401)


@app.exception_handler(ClientSessionNotInitialized)
async def client_session_error_handler(_, e: ClientSessionNotInitialized):
    print(e)
    return JSONResponse({"error": "Internal Error"}, status_code=500)

@app.get(
    "/api/guilds",
    dependencies=[Depends(discord.requires_authorization)],
    response_model=List[GuildPreview],
)
async def get_guilds(guilds: List = Depends(discord.guilds)):
    return guilds

@app.get(
    "/api/guilds/{guild_id}",
    dependencies=[Depends(discord.requires_authorization)]
)
async def get_guild(guild_id: str, request: Request) -> List[Guild]:
    route = f"/users/@me/guilds/{guild_id}/member"
    token = discord.get_token(request)

    return await discord.request(route, token)

@app.get(
    "/api/sitrep",
)
async def get_sitrep(request: Request):
    print(request.headers)

    discord_token = discord.get_token(request)
    if not await discord.isAuthenticated(discord_token):
        raise Unauthorized

    sitrep = {
        "theater_name": 'Caucasus',
        "theater_center":[43.05, 39.40],
        "airfields": [
            {
                'name': 'Kobuleti',
                "coalition": 'RED',
                "position": [41.93, 41.86444]
            },
            {
                'name': 'Kutaisi',
                "coalition": 'BLUE',
                "position": [42.17639, 42.48222]
            },
            {
                'name': 'Batumi',
                "coalition": 'BLUE',
                "position": [41.61028, 41.59917]
            },
            {
                'name': 'Beslan',
                "coalition": 'RED',
                "position": [43.20528, 44.60639]
            },
            {
                'name': 'Gudauta',
                "coalition": 'RED',
                "position": [43.11111, 40.57778]
            },
            {
                'name': 'Krasnodar-Center',
                "coalition": 'RED',
                "position": [45.03472, 39.17083]
            },
            {
                'name': 'Sukhumi',
                "coalition": 'RED',
                "position": [42.85833, 41.12861]
            },
            {
                'name': 'Vody',
                "coalition": 'RED',
                "position": [44.225, 43.08194]
            },
            {
                'name': 'Anapa',
                "coalition": 'BLUE',
                "position": [44.99528, 37.34722]
            },
            {
                'name': 'Gelendzhik',
                "coalition": 'BLUE',
                "position": [44.56667, 38.01667]
            },
            {
                'name': 'Mozdok',
                "coalition": 'RED',
                "position": [43.79167, 44.60306]
            },
            {
                'name': 'Nalchik',
                "coalition": 'RED',
                "position": [43.51389, 43.63611]
            },
            {
                'name': 'Sochi',
                "coalition": 'BLUE',
                "position": [43.45, 39.95694]
            },
            {
                'name': 'Senaki-Kolkhi',
                "coalition": 'BLUE',
                "position": [42.25, 42.03333]
            },
            {
                'name': 'Novorossiysk',
                "coalition": 'BLUE',
                "position": [44.68333, 37.76667]
            },
            {
                'name': 'Vaziani',
                "coalition": 'BLUE',
                "position": [41.62222, 45.03194]
            },
            {
                'name': 'Maykop',
                "coalition": 'RED',
                "position": [44.66667, 40.1]
            },
            {
                'name': 'Krimsk',
                "coalition": 'RED',
                "position": [44.92934, 37.99117]
            }
        ],
        "farps": [{
            "position": { "x": 1, "y": 2 }
        }]
    }
    return sitrep

if __name__ == "__main__":
    import uvicorn
    uvicorn.run('main:app', host="localhost", port=8000, log_level="debug", reload=True)

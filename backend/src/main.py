from fastapi import Request, FastAPI
from fastapi.responses import JSONResponse
from fastapi_discord import Unauthorized
from fastapi_discord.exceptions import ClientSessionNotInitialized

from discord import router as discord_router, discord
import json

from db import DB

app = FastAPI()

app.include_router(discord_router, prefix="/api/auth", tags=["Auth"])

@app.exception_handler(Unauthorized)
async def unauthorized_error_handler(_, __):
    return JSONResponse({"error": "Unauthorized"}, status_code=401)

@app.exception_handler(ClientSessionNotInitialized)
async def client_session_error_handler(_, e: ClientSessionNotInitialized):
    print(e)
    return JSONResponse({"error": "Internal Error"}, status_code=500)

@app.get("/api/sitrep")
async def get_sitrep(request: Request):
    discordUser = await discord.user(request) # will raise Unauthorized if not logged in
    print(f"Loading For Discord User ID: {discordUser.id}")


    coalition = await DB().get_user_coalition_by_discord_id(discordUser.id)
    print(f"Loading For Coalition: {coalition}")

    if coalition is None:
        return JSONResponse({"error": "User not found"}, status_code=404)

    response = json.loads( open("data/database.json", 'r').read() )
    for zone in response['grid']['zones']:
        zone['state'] = zone['state'][coalition.lower()]

    return response

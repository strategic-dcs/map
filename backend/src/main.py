from fastapi import Request, FastAPI
from fastapi.responses import JSONResponse
from fastapi_discord import Unauthorized
from fastapi_discord.exceptions import ClientSessionNotInitialized

from discord import router as discord_router, discord
import json

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
    coalition = "NEUTRAL"

    print(f"Loading For Coalition: {coalition}")

    data = json.loads( open("shared_data/website_data.json", 'r').read() )

    # default state
    default_state = {
        "line_style": "DASHED",
        "line_color": [1,1,1,0.6],
        "fill_color": [0,0,0,0],
        "zone_type": "UNKNOWN"
    }

    # filter airfield for coalition
    airfields_friendly = []
    for air in data['airfields']:
        if air['coalition'].lower() == coalition.lower():
            airfields_friendly.append({
                "name": air['name'],
                "level": air['level'],
                "position": air['position'],
                "coalition": air['coalition'],
            })

    airfields_enemy = []
    for air in data['airfields']:
        if air['coalition'].lower() != coalition.lower():
            airfields_enemy.append({
                "name": air['name'],
                "position": air['position'],
                "coalition": air['coalition'],
            })

    farps = []
    for farp in data['farps']:
        if farp['coalition'].lower() == coalition.lower():
            farps.append({
                "name": farp['name'],
                "level": farp['level'],
                "position": farp['position'],
                "coalition": farp['coalition'],
            })

    response = {
        "time": data['time'],
        "current_coalition": coalition.lower(),
        "theatre": data['theatre'],
        "zones": [{ "name": z['name'], "points": z["points"], "state": z["state"].get(coalition.lower(), default_state) } for z in data['zones']],
        "airfields_friendly": airfields_friendly,
        "airfields_enemy": airfields_enemy,
        "farps": farps,
        "online_users": data.get("players", []),
        "seconds_left_until_restart": data['seconds_left_until_restart'],
    }

    if coalition == "RED":
        response['units'] = data['red_units']
    else:
        response['units'] = data['blue_units']

    return response

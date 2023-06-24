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

app.include_router(auth_router, prefix="/auth", tags=["Auth"])

@app.exception_handler(Unauthorized)
async def unauthorized_error_handler(_, __):
    return JSONResponse({"error": "Unauthorized"}, status_code=401)


@app.exception_handler(ClientSessionNotInitialized)
async def client_session_error_handler(_, e: ClientSessionNotInitialized):
    print(e)
    return JSONResponse({"error": "Internal Error"}, status_code=500)

# @router.get(
#         "/",
#         dependencies=[Depends(discord.requires_authorization)],
#         response_class=HTMLResponse)
# async def index(request: Request):
#     print("---------")
#     # if await discord.isAuthenticated(token):
#     return "<h1>Hello, World!</h1>"
#     # else:
#     #     auth_url = discord.get_authorize_url()
#     #     return f'<a href="{auth_url}">Login with Discord</a>'


@app.get(
    "/guilds",
    dependencies=[Depends(discord.requires_authorization)],
    response_model=List[GuildPreview],
)
async def get_guilds(guilds: List = Depends(discord.guilds)):
    return guilds

@app.get(
    "/guilds/{guild_id}",
    dependencies=[Depends(discord.requires_authorization)]
)
async def get_guild(guild_id: str, request: Request) -> List[Guild]:
    route = f"/users/@me/guilds/{guild_id}/member"
    token = discord.get_token(request)
    
    return await discord.request(route, token)



if __name__ == "__main__":
    import uvicorn
    uvicorn.run('main:app', host="localhost", port=8000, log_level="debug", reload=True)
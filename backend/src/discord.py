from typing import List

from fastapi import Request, Response, Depends
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi_discord import DiscordOAuthClient, Unauthorized, User
from fastapi_discord.models import GuildPreview, Guild

from config import settings

from fastapi import APIRouter

router = APIRouter()

discord = DiscordOAuthClient(
    client_id=settings.DISCORD_OAUTH_CLIENT_ID,
    client_secret=settings.DISCORD_OAUTH_SECRET,
    redirect_uri=settings.DISCORD_OAUTH_REDIRECT_URI,
    scopes=["identify"]
)

@router.on_event("startup")
async def on_startup():
    await discord.init()

@router.get("/login", response_class=HTMLResponse)
async def login():
    return f'<a href="{discord.oauth_login_url}">Login with Discord</a>'

@router.get("/callback")
async def callback(code: str, request: Request, response: Response):
    print(f"Callback method.... code: {code} - {discord.client_id} - {discord.client_secret}")
    print(f"""
          #####
            DISCORD_CLIENT_ID={discord.client_id}
          #####
    """)
    token, refresh_token = await discord.get_access_token(code)

    print("Setting token to cookie")
    response.set_cookie(key="oauth2_token", value=token)

    return { "access_token": token, "refresh_token": refresh_token }

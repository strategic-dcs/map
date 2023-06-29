from pydantic import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()

class Config(BaseSettings):
    HOST: str

    CORS_ORIGINS: list[str]
    CORS_ORIGINS_REGEX: str
    CORS_HEADERS: list[str]

    DISCORD_OAUTH_CLIENT_ID: str
    DISCORD_OAUTH_SECRET: str
    DISCORD_OAUTH_REDIRECT_URI: str

    DB_HOST: str
    DB_USER: str
    DB_PASSWORD: str

host = os.getenv('HOST') or "localhost"

settings = Config(
    HOST=host,

    CORS_ORIGINS=[f"http://{host}:3000"],
    CORS_ORIGINS_REGEX="localhost",
    CORS_HEADERS=["*"],

    DISCORD_OAUTH_CLIENT_ID=os.getenv('DISCORD_OAUTH_CLIENT_ID'),
    DISCORD_OAUTH_SECRET=os.getenv('DISCORD_OAUTH_SECRET'),
    DISCORD_OAUTH_REDIRECT_URI=os.getenv('DISCORD_OAUTH_REDIRECT_URI') or f"http://{host}:3000/auth/callback",

    DB_HOST=os.getenv('DB_HOST'),
    DB_USER=os.getenv('DB_USER'),
    DB_PASSWORD=os.getenv('DB_PASSWORD'),
    DB_PORT=os.getenv('DB_PORT') or 3306,

)

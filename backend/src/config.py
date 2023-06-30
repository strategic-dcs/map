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

    DATABASE_URL: str

host = os.getenv('HOST') or "localhost"

settings = Config(
    HOST=host,

    CORS_ORIGINS=[f"http://{host}:3000"],
    CORS_ORIGINS_REGEX="localhost",
    CORS_HEADERS=["*"],

    DISCORD_OAUTH_CLIENT_ID=os.getenv('DISCORD_OAUTH_CLIENT_ID'),
    DISCORD_OAUTH_SECRET=os.getenv('DISCORD_OAUTH_SECRET'),
    DISCORD_OAUTH_REDIRECT_URI=os.getenv('DISCORD_OAUTH_REDIRECT_URI') or f"http://{host}:3000/auth/callback",

    DATABASE_URL="mysql+pymysql://root:password@db:3306/sdcs",
)

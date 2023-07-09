from pydantic import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()

class Config(BaseSettings):
    DISCORD_OAUTH_CLIENT_ID: str
    DISCORD_OAUTH_SECRET: str
    FQDN: str

    DATABASE_URL: str

settings = Config(
    DISCORD_OAUTH_CLIENT_ID=os.getenv('DISCORD_OAUTH_CLIENT_ID'),
    DISCORD_OAUTH_SECRET=os.getenv('DISCORD_OAUTH_SECRET'),
    FQDN=os.getenv('FQDN'),

    DATABASE_URL=os.getenv('DATABASE_URL') or "mysql+mysqlconnector://root:password@db:3306/sdcs",
)

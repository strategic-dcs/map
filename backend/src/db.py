import mysql.connector
from config import settings

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session


print(f"Connection to database: {settings.DATABASE_URL}")
engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = SessionLocal()



class DB():
    async def get_user_coalition_by_discord_id(self, discord_id: int):
        with engine.connect() as connection:
            result = connection.execute(text("""
                SELECT side.coalition FROM User
                INNER JOIN UserSide side
                    on side.user_id = User.id
                WHERE
                    User.discord_id = :discord_id
                    AND side.campaign_id = (
                        SELECT id FROM Campaign ORDER BY id DESC LIMIT 1
                    )
            """), { "discord_id": discord_id })

            row = result.fetchone()

            if not row:
                return None
            else:
                return row[0]

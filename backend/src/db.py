from config import settings

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session

engine = create_engine(settings.DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = SessionLocal() # the app never writes, so no need to close the session?

class DB():
    async def get_user_coalition_by_discord_id(self, discord_id: int):
        result = session.execute(text("""
            SELECT side.coalition FROM user
            INNER JOIN userside side
                on side.user_id = user.id
            WHERE
                user.discord_id = :discord_id
                AND side.campaign_id = (
                    SELECT id FROM campaign ORDER BY id DESC LIMIT 1
                )
        """), { "discord_id": discord_id })

        row = result.fetchone()

        if not row:
            return None
        else:
            return row[0]

import mysql.connector
from config import settings

class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

class DB(metaclass=SingletonMeta):
    def __init__(self):
        self.connection = mysql.connector.connect(
            host=settings.DB_HOST,
            user=settings.DB_USER,
            password=settings.DB_PASSWORD,
            port=settings.DB_PORT,
            database='sdcs'
        )

        self.connection.autocommit = True

    def get_cursor(self):
        return self.connection.cursor(buffered=True)

    def get_user_coalition_by_discord_id(self, discord_id: int):
        cursor = self.get_cursor()

        cursor.execute("""
          SELECT side.coalition FROM user
          INNER JOIN userside side
            on side.user_id = user.id
          WHERE
            user.discord_id = %s
            AND side.campaign_id = (
                SELECT id FROM campaign ORDER BY id DESC LIMIT 1
            )
        """,
         (discord_id,))

        data = cursor.fetchone()[0]

        return data

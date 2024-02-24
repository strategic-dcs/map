from datetime import timezone
import sqlalchemy.types as types


class DateTimeUTC(types.TypeDecorator):

    impl = types.DateTime

    cache_ok = True

    def process_result_value(self, value, dialect):
        if not value:
            return None
        return value.replace(tzinfo=timezone.utc)

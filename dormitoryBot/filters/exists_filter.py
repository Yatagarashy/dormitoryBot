from aiogram.filters import BaseFilter
from sqlite3 import Cursor



class ExistsFilter(BaseFilter):
    async def __call__(self, event, cursor: Cursor) -> bool:
        exists = cursor.execute("SELECT * FROM users WHERE telegram_id = ?", (event.from_user.id,)).fetchone()

        if exists is None:
            return False
        else:
            return True
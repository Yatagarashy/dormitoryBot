from aiogram import BaseMiddleware
from typing import Callable, Dict, Awaitable, Any
from aiogram.types import TelegramObject, Update, Message, CallbackQuery
from sqlite3 import Cursor, Connection


class DbSessionMiddleware(BaseMiddleware):

    def __init__(self, cursor: Cursor, connection: Connection):
        super().__init__()
        self.cursor = cursor
        self.connection = connection

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
    ) -> Any:
        

        data['cursor'] = self.cursor
        data['connection'] = self.connection
        return await handler(event, data)
        
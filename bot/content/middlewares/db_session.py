import asyncpg
from typing import Callable, Awaitable, Dict, Any
from aiogram.types.base import TelegramObject
from database.db import Database
from aiogram import BaseMiddleware


class DbSession(BaseMiddleware):
    def __init__(self, pool_connect: asyncpg.pool.Pool):
        self.pool_connect = pool_connect
        super(DbSession, self).__init__()

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
    ) -> Any:
        async with self.pool_connect.acquire() as connect:
            data['database'] = Database(connect=connect)
            return await handler(event, data)

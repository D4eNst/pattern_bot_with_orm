# from .models import
import asyncpg
import logging
from aiogram.fsm.storage.redis import RedisStorage
from redis import asyncio as aioredis

from data.config import settings


class Database:

    def __init__(self, connect: asyncpg.pool.Pool):
        self.connect = connect
        self.cursor = self.connect

    async def create_tables(self) -> None:
        await self.connect.execute("""
            CREATE TABLE IF NOT EXISTS table_name(
                id INT PRIMARY KEY,
                first INT,
                second TEXT
            )""")


redis = aioredis.from_url(settings.redis_url)
storage = RedisStorage(redis=redis)


async def get_pool_connect() -> asyncpg.pool.Pool | None:
    """
        Returns a pool of database connections with data that is defined in config.py
        Make sure that you have correctly specified all the data in the .env file.
        :returns: An instance of ~asyncpg.pool.Pool.
    """

    pool_connect = None

    try:
        pool_connect = await asyncpg.create_pool(settings.postgres_dsn)
    except asyncpg.exceptions.InvalidCatalogNameError:
        logging.info("Creating database")

        conn = await asyncpg.connect(settings.postgres_dsn_to_main_db)
        await conn.execute(f'CREATE DATABASE {settings.POSTGRES_DATABASE}')
        await conn.close()

        pool_connect = await asyncpg.create_pool(settings.postgres_dsn)
        async with pool_connect.acquire() as connect:
            await Database(connect).create_tables()
    except Exception as e:
        logging.error(f"Error in creating pool:\n{e}")

    return pool_connect

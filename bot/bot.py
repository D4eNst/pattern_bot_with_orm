from aiogram import Dispatcher, Bot
from database.db import storage
from data.config import settings

bot = Bot(token=settings.TOKEN, parse_mode='HTML')
dp = Dispatcher(storage=storage)

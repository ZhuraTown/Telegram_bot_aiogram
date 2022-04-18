import logging
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

# @Random_zhura_45_bot
API_TOKEN = "1913518174:AAHB6daABGP9G3Ec93_4bnJHQWXSjtbyZiM"

storage = MemoryStorage()

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=storage)





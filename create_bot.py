import logging
from aiogram import Bot, Dispatcher


API_TOKEN = "1913518174:AAHB6daABGP9G3Ec93_4bnJHQWXSjtbyZiM"

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)





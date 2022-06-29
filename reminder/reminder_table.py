import asyncio
import datetime

from data_base.db_commands import CommandsDB
from aiogram import Bot
from aiogram.utils.exceptions import ChatNotFound

""" Напоминатель по заполнению табеля времени
 WEEKEND - дни недели без проверок(сб и вс)
 TIME_REMIND_H - час напоминания
 TIME_REMIND_START_M - минуты для напоминания
 TIME_REMIND_FINISH_M - минуты для напоминания
 """
WEEKEND = [5, 6]
TIME_REMIND_START_M = 0
TIME_REMIND_FINISH_M = 45
TIME_REMIND_H = 9
DELAY = 60


async def remind_fill_out_form(bot: Bot):
    # while True:
    #     await asyncio.sleep(DELAY * delay_to_check)
    #     now_time = datetime.datetime.now()
    #     NOW_DAY = now_time.weekday()
    #     NOW_HOUR = now_time.hour
    #     NOW_MINUTE = now_time.minute
    #     if NOW_DAY not in WEEKEND:
    #         if TIME_REMIND_H == NOW_HOUR:
    #             if TIME_REMIND_START_M <= NOW_MINUTE <= TIME_REMIND_FINISH_M:
    chat_ids = CommandsDB.get_users_with_chat_id_is_remind()
    for chat_id in chat_ids:
        try:
            await bot.send_message(chat_id[0],
                                   text=f"{'<b>'}Пора заполнить табель!{'</b>'}",
                                   parse_mode='HTML')
        except ChatNotFound:
            print(f'Чат не нашел, искал {chat_id}')

# async def del_remind_fill_out_form(bot: Bot, delay_to_check: int or float = 45):
#     pass

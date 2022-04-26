from aiogram.utils.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from .callback_datas import workers_callback, menu_callback, add_users, none_callback


def get_inline_workers_panel():
    btn_sec = InlineKeyboardButton(text='Охрана',
                                   callback_data=workers_callback.new(
                                       type_step='workers',
                                       type_worker='Охрана',
                                       amount=0))
    btn_duty = InlineKeyboardButton(text='Дежурный',
                                    callback_data=workers_callback.new(
                                        type_step='workers',
                                        type_worker='Дежурный',
                                        amount=0))
    btn_worker = InlineKeyboardButton(text='Рабочий',
                                      callback_data=workers_callback.new(
                                          type_step='workers',
                                          type_worker='Рабочий',
                                          amount=0))
    btn_itr = InlineKeyboardButton(text='ИТР',
                                   callback_data=workers_callback.new(
                                       type_step='workers',
                                       type_worker='ИТР',
                                       amount=0))
    btn_skip = InlineKeyboardButton(text='Пропустить',
                                    callback_data=menu_callback.new(
                                        btn_menu='add_users',
                                        type_btn='skip'
                                    ))
    btn_cancel = InlineKeyboardButton(text='Отменить',
                                      callback_data=menu_callback.new(
                                          btn_menu='add_users',
                                          type_btn='cancel'
                                      ))
    return InlineKeyboardMarkup(row_width=2).row(btn_sec, btn_duty). \
        row(btn_worker, btn_itr).row(btn_skip).row(btn_cancel)


def get_panel_attempt_add_users():
    btn_next = InlineKeyboardButton(text='Продолжить',
                                    callback_data=menu_callback.new(
                                        btn_menu='finish_add',
                                        type_btn='Продолжить'))
    btn_add = InlineKeyboardButton(text='Добавить',
                                   callback_data=menu_callback.new(
                                       btn_menu='finish_add',
                                       type_btn='Добавить'))
    return InlineKeyboardMarkup(row_width=1).row(btn_next).row(btn_add)


def get_btn_add_users():
    btn_empty = InlineKeyboardButton(text=' ', callback_data=none_callback.new(
        none_call='empty'
    ))
    btn_add_1 = InlineKeyboardButton(text='+1', callback_data=add_users.new(
        type='1', type_btn='plus'
    ))
    btn_add_10 = InlineKeyboardButton(text='+10', callback_data=add_users.new(
        type='10', type_btn='plus'
    ))
    btn_minus_1 = InlineKeyboardButton(text='-1', callback_data=add_users.new(
        type='1', type_btn='minus'
    ))
    btn_minus_10 = InlineKeyboardButton(text='-10', callback_data=add_users.new(
        type='10', type_btn='minus'))
    return InlineKeyboardMarkup(row_width=4).row(btn_add_1, btn_add_10).row(btn_empty).row(btn_minus_1, btn_minus_10)



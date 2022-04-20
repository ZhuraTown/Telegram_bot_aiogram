import sqlite3 as sq
from aiogram import types
from sqlalchemy import (Column, Integer, BigInteger, String, Sequence,
                        TIMESTAMP, Boolean, JSON)
from sqlalchemy import sql



# def sql_start():
#     global base, cur
#     base = sq.connect('base_tg_bot.db')
#     cur = base.cursor()
#     if base:
#         print('База подключена')
#     base.execute('CREATE TABLE IF NOT EXISTS users(id_user PRIMARY KEY, name_user TEXT, password TEXT)')
#     base.commit()


# class User(db.Model):
#     __tablename__ = 'users'
#     company_name = Column(String(50))
#     admin_user = Column(Boolean)
#     pin_code = Column(String(8))
#     query: sql.Select
#
#
# class DBCommands:
#     async def get_user(self, company_name) -> User:
#         user = await User.query.where(User.company_name == company_name).gino.first()
#         return user
#
#     async def add_new_user(self, name_company, state) -> User:
#         # user = types.User.get_current()
#         new_company = User()
#         new_company.company_name = state['company_name']
#         new_company.admin_user = state['admin_user']
#         new_company.pin_code = state['pin_code']
#         await new_company.create()
#         return new_company
#
#     async def count_users(self):
#         total = await db.func.count(User.company_name).gino.scalar()
#         return total
#
#
# async def create_db():
#     print('Создание таблицы')
#     await db.set_bind("postgres://localhost/main")
#     db.gino = GinoSchemaVisitor
#     await db.gino.create_all()




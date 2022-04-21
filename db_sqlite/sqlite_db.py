# class
#
# def sql_start():
#     global base, cur
#     base = sq.connect('base_tg_bot.db')
#     cur = base.cursor()
#     if base:
#         print('База подключена')
#     base.execute('CREATE TABLE IF NOT EXISTS users(id_user PRIMARY KEY, name_user TEXT, password TEXT)')
#     base.commit()
#
#
# db = Gino()
#
#
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
#


from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy import (Column, Integer, BigInteger, String, Sequence,
                        TIMESTAMP, Boolean, JSON)
from time import sleep

engine = create_engine('sqlite:///webinar.db', echo=True)
session = sessionmaker(bind=engine)()
base = declarative_base()


class User(base):
    __tablename__ = 'users_table'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)

    def __repr__(self):
        return '<User(name="{}", fullname="{}")>'.format(self.name, self.fullname)


base.metadata.create_all(engine)
#
# names = ['vasya', 'vlad', 'yura']
#
# for name in names:
#
#     User(name=name, fullname=f'Last_name {name}')
#     session.add(User(name=name, fullname=f'Last_name {name}'))
#     session.commit()
# q = session.query(User).filter_by(name='vlad')
# session.add_all([User(name='Petr', fullname='Ivanov'), User(name='Irina', fullname='Noskova')])
# session.commit()
sleep(1)
for element in session.query(User).all():
   print(element)

   # https://www.youtube.com/watch?v=PAKJpfxeXjc
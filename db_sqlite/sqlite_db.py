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
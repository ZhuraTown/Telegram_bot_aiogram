from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

import os

base = declarative_base()
path_to_db = os.path.dirname(os.path.realpath(__file__))

engine = create_engine('sqlite:///' + os.path.join(path_to_db, 'tg_bot.db'), echo=True,
                       connect_args={'check_same_thread': False})

session = sessionmaker(bind=engine)
session = scoped_session(session)

connect = engine.connect()



from sqlalchemy import (Column, Integer, BigInteger, String, Sequence,
                        TIMESTAMP, Boolean, JSON, ForeignKey, Date, DateTime)

from data_base.database import base, engine


class User(base):
    __tablename__ = 'users'

    user_id = Column(
        Integer,
        unique=True,
        primary_key=True,
        autoincrement=True
    )
    name = Column(String)
    password = Column(String, default='000000')
    comment = Column(String, default=None)
    admin = Column(Boolean, default=False)

    def __repr__(self):
        return '<User(user_id="{}", name="{}",password="{}", admin="{}", comment="{}")>'. \
            format(self.user_id, self.name, self.password, self.admin, self.comment)

    # query: sql.select


class TableWork(base):
    __tablename__ = 'work_time'

    work_sting_id = Column(Integer,
                           unique=True,
                           primary_key=True,
                           autoincrement=True
                           )
    user_id = Column(Integer, ForeignKey('users.user_id'), comment='Автор записи')
    name_work = Column(String, comment='Наименование работ')
    name_stage = Column(Integer, comment='Наименование этапа')
    name_build = Column(String, comment='Наименование здания')
    name_level = Column(String, comment='Наименование этажа')
    number_security = Column(Integer, comment='Охрана')
    number_duty = Column(Integer, comment='Дежурный')
    number_worker = Column(Integer, comment='Рабочий')
    number_ITR = Column(Integer, comment='ИТР')
    date_created = Column(Date, comment='Дата создания')

    def __repr__(self):
        return '<User(user_id="{}", name_work="{}",name_stage="{}", name_build="{}", ' \
               'name_level="{}",security="{}", duty="{}", worker="{}", itr="{}", date_created="{}" )>' \
            .format(self.user_id, self.name_work,
                    self.name_stage, self.name_build,
                    self.name_level, self.number_security,
                    self.number_duty, self.number_worker,
                    self.number_ITR, self.date_created)

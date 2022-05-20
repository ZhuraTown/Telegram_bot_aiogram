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


class TableWork(base):
    __tablename__ = 'main_table_work'

    work_sting_id = Column(Integer,
                           unique=True,
                           primary_key=True,
                           autoincrement=True
                           )
    user_name = Column(String, comment='Автор записи')
    name_work = Column(String, comment='Наименование работ')
    name_stage = Column(String, comment='Наименование этапа')
    name_build = Column(String, comment='Наименование здания')
    name_level = Column(String, comment='Наименование этажа')
    number_security_p = Column(Integer, default=0, comment='Охрана План')
    number_security_f = Column(Integer, default=0, comment='Охрана Факт')
    number_duty_p = Column(Integer, default=0, comment='Дежурный План')
    number_duty_f = Column(Integer, default=0, comment='Дежурный Факт')
    number_worker_p = Column(Integer, default=0, comment='Рабочий План')
    number_worker_f = Column(Integer, default=0, comment='Рабочий Факт')
    number_ITR_p = Column(Integer, default=0, comment='ИТР План')
    number_ITR_f = Column(Integer, default=0, comment='ИТР Факт')
    date_created = Column(Date, comment='Дата создания')

    def __repr__(self):
        return '<TableWork(user_id="{}", name_work="{}",name_stage="{}", name_build="{}", ' \
               'name_level="{}",security_p="{}",security_f="{}" ' \
               'duty_p="{}", duty_f="{}", ' \
               'worker_p="{}",worker_f="{}", itr_p="{}", itr_f="{}" ' \
               'date_created="{}" )>' \
            .format(self.user_name, self.name_work,
                    self.name_stage, self.name_build,
                    self.name_level, self.number_security_p,
                    self.number_security_f, self.number_duty_p,
                    self.number_duty_f, self.number_worker_p,
                    self.number_worker_f, self.number_ITR_p,
                    self.number_ITR_f, self.date_created)


class TableNameWork(base):
    __tablename__ = 'names_work'

    work_name_id = Column(Integer,
                          unique=True,
                          primary_key=True,
                          autoincrement=True
                          )
    name_work = Column(String, comment='Наименование работ')

    def __repr__(self):
        return "<TableNameWork(user_id='{}', name_work='{}')".format(self.work_name_id, self.name_work)


class TableNameBuild(base):
    __tablename__ = 'builds_work'

    build_id = Column(Integer,
                      unique=True,
                      primary_key=True,
                      autoincrement=True
                      )
    name_build = Column(String, comment='Наименование здания')

    def __repr__(self):
        return "<builds_work(build_id='{}', name_build='{}')".format(self.build_id, self.name_build)


class TableLinks(base):
    __tablename__ = 'links'

    link_id = Column(Integer,
                     primary_key=True,
                     autoincrement=True)
    name_link = Column(String,
                       unique=True,
                       comment='Наименование ссылки')
    link = Column(String, unique=True, comment='Ссылка')
    comment_link = Column(String, default='Комментарий не добавлен')

    def __repr__(self):
        return "<links(name_link='{}', link='{}', comment_link='{}')>". \
            format(self.name_link, self.link, self.comment_link)

from datetime import datetime
from random import randint
from typing import List, Dict, Union, Any

from sqlalchemy import distinct, func
from data_base.database import session

from .models import User, TableNameWork, base, engine, TableNameBuild, TableWork, TableLinks


class CommandsDB:
    @staticmethod
    def create_db():
        base.metadata.create_all(engine)
        CommandsDB.add_link(
            'google_form',
            "https://docs.google.com/forms/d/e"
            "/1FAIpQLSfj3nGZjk6T5sFKn7Cc1lMCLy7dlPOs4kEOe5EVVSaLClL08g/viewform?usp=sf_link")

    ##############################
    #       ПОЛЬЗОВАТЕЛИ
    ##############################
    @staticmethod
    def get_user_with_name(name):
        my_query = session.query(User.name, User.user_id).filter(User.name == name).all()
        return my_query

    @staticmethod
    def get_all_users(user_password=False) -> list or dict:
        if not user_password:
            rows = session.query(User.user_id, User.name, User.comment, User.password, User.admin).all()
        else:
            rows = {user[1]: [user[0], user[2]] for user in session.query(User.name, User.password, User.admin).all()}
        return rows

    @staticmethod
    def get_names_all_users() -> list:
        return [name[0] for name in session.query(User.name).all()]

    @staticmethod
    def add_user_system(name, password, comment=None, admin=False):
        try:
            if session.query(User.name).filter(User.name == name).count() == 0:
                session.add(User(name=name,
                                 password=password,
                                 comment=comment,
                                 admin=admin))
                session.flush()
                return True
            else:
                print(f"Пользователь с именем {name}, уже есть в БД")
                return False
        except:
            session.rollback()
            print(f'Ошибка записи {name} в БД')
            return False
        finally:
            session.commit()

    @staticmethod
    def update_name_user_with_name(name, new_name):
        try:
            session.query(User).filter(User.name == name).update({"name": new_name})
            session.flush()
            print('Пользователь успешно изменён')
            return True
        except:
            session.rollback()
            print('Что-то пошло не так. Изменить пользователя не удалось')
            return False
        finally:
            session.commit()

    @staticmethod
    def get_password_user_with_name(name):
        return session.query(User.password).filter(User.name == name).one()[0]

    @staticmethod
    def update_pincode_user_with_name(name, new_pin):
        try:
            session.query(User).filter(User.name == name).update({"password": new_pin})
            session.flush()
            print('Пользователь успешно изменён')
            return True
        except:
            session.rollback()
            print('Что-то пошло не так. Изменить пользователя не удалось')
            return False
        finally:
            session.commit()

    @staticmethod
    def delete_user_with_name(name):
        try:
            session.query(User).filter(User.name == name).delete()
            session.flush()
            print(f"Удаление прошло успешно.Пользователь с именем {name}")
            return True
        except:
            session.rollback()
            print(f'Ошибка удаления пользователя с именем {name} из БД')
            return False
        finally:
            session.commit()

    @staticmethod
    def delete_user_with_id(id):
        try:
            session.query(User).filter(User.user_id == id).delete()
            session.flush()
        except:
            session.rollback()
            print(f'Ошибка удаления пользователя с ID {id} из БД')
        finally:
            print(f"Удаление прошло успешно.Пользователь с ID {id}")
            session.commit()

    ################################
    #
    ################################
    @staticmethod
    def add_link(name_link, link) -> bool:
        try:
            if session.query(TableLinks.link).filter(TableLinks.link == link).count() == 0:
                session.add(TableLinks(name_link=name_link, link=link))
                session.flush()
                return True
            else:
                print(f"Ссылка  {link}, уже есть в БД")
                return False
        except:
            session.rollback()
            print(f'Ошибка записи {link} в БД')
            return False
        finally:
            session.commit()

    @staticmethod
    def get_link(name_link) -> str:
        return session.query(TableLinks.link).filter(TableLinks.name_link == name_link).one()[0]

    #################################
    #      НАИМЕНОВАНИЯ РАБОТ
    ################################
    @staticmethod
    def add_name_work(name):
        try:
            if session.query(TableNameWork.name_work).filter(TableNameWork.name_work == name).count() == 0:
                session.add(TableNameWork(name_work=name))
                session.flush()
                return True
            else:
                return False
        except:
            session.rollback()
            print(f'Ошибка записи {name} в БД')
        finally:
            session.commit()

    @staticmethod
    def del_name_work(id_name):
        try:
            session.query(TableNameWork).filter(TableNameWork.work_name_id == id_name).delete()
            session.flush()
            print(f"Удаление работы с ID {id_name} успешно")
            return True
        except:
            session.rollback()
            print(f'Ошибка работы с наименованием {id_name} из БД')
            return False
        finally:
            session.commit()

    @staticmethod
    def get_all_names_work():
        rows = session.query(TableNameWork.work_name_id, TableNameWork.name_work).all()
        return rows

    @staticmethod
    def get_name_work_for_id(id_name):
        row = session.query(TableNameWork.name_work).filter(TableNameWork.work_name_id == id_name).one()
        return row[0]

    ##################################
    #             ЗДАНИЯ
    #################################
    @staticmethod
    def add_name_build(name):
        try:
            if session.query(TableNameBuild.name_build).filter(TableNameBuild.name_build == name).count() == 0:
                session.add(TableNameBuild(name_build=name))
                session.flush()
                return True
            else:
                return False
        except:
            session.rollback()
            print(f'Ошибка записи {name} в БД')
        finally:
            session.commit()

    @staticmethod
    def del_name_build(name):
        try:
            session.query(TableNameBuild).filter(TableNameBuild.name_build == name).delete()
            session.flush()
            print(f"Удаление {name} успешно")
            return True
        except:
            session.rollback()
            print(f'Ошибка удаления {name} из БД')
            return False
        finally:
            session.commit()

    @staticmethod
    def get_all_names_builds():
        rows = session.query(TableNameBuild.build_id, TableNameBuild.name_build).all()
        return rows

    @staticmethod
    def get_name_build_with_id(build_id):
        rows = session.query(TableNameBuild.name_build).filter(TableNameBuild.build_id == build_id).one()
        return rows[0]

    ###############################
    #   ЗАПИСЬ ФОРМЫ ТАБЕЛЯ
    ###############################
    @staticmethod
    def add_new_string_work_tm(user_name: str, name_work: str, name_stage: str,
                               name_build: str, level: str,
                               number_security: list,
                               number_duty: list,
                               number_worker: list,
                               number_itr: list):
        try:
            data_today = datetime.now().date()
            session.add(TableWork(user_name=user_name, name_work=name_work, name_stage=name_stage,
                                  name_build=name_build, name_level=level, date_created=data_today,
                                  number_security_p=number_security[0], number_security_f=number_security[1],
                                  number_duty_p=number_duty[0], number_duty_f=number_duty[1],
                                  number_worker_p=number_worker[0], number_worker_f=number_worker[1],
                                  number_ITR_p=number_itr[0], number_ITR_f=number_itr[1],
                                  ))
            session.flush()
            return True
        except:
            session.rollback()
            print(f'Ошибка записи в БД')
        finally:
            session.commit()

    @staticmethod
    def get_forms_with_user_with_name(user_name: str, name_work: str) -> List[Dict[str, Union[Dict[str, List[Any]], Any]]]:
        TB = TableWork
        rows = session.query(TB.user_name, TB.name_work, TB.name_stage, TB.name_build, TB.name_level, TB.date_created,
                             TB.number_security_p, TB.number_security_f, TB.number_duty_p, TB.number_duty_f,
                             TB.number_worker_p, TB.number_worker_f, TB.number_ITR_p, TB.number_ITR_f,
                             ).filter(TB.user_name == user_name, TB.name_work == name_work).all()
        answer = [{
            'name_work': row[1],
            "name_stage": row[2],
            "name_build": row[3],
            "level": row[4],
            'workers': {
                "Охрана": [row[6], row[7]],
                "Дежурный": [row[8], row[9]],
                "Рабочий": [row[10], row[11]],
                "ИТР": [row[12], row[13]]
            }
        } for row in rows]
        return answer

    @staticmethod
    def get_name_forms_with_user(user_name):
        TB = TableWork
        return [name.name_work for name in session.query(TB.name_work).filter(TB.user_name == user_name).distinct().all()]


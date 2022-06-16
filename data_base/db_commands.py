from datetime import datetime
from random import randint
from typing import List, Dict, Union, Any

from sqlalchemy import distinct, func
from data_base.database import session

from data_base.models import User, TableNameWork, base, engine, TableNameBuild, TableWork


class CommandsDB:
    @staticmethod
    def create_db():
        base.metadata.create_all(engine)

    ##############################
    #       ПОЛЬЗОВАТЕЛИ
    ##############################
    @staticmethod
    def get_user_with_id(id_user: str or int):
        my_query = session.query(User.name, User.user_id).filter(User.user_id == id_user).all()
        return my_query

    @staticmethod
    def get_all_users(user_password=False) -> list or dict:
        if not user_password:
            rows = session.query(User.user_id, User.name, User.comment, User.password, User.admin).all()
        else:
            rows = {user[1]: [user[0], user[2], user[3]] for user in
                    session.query(User.name, User.password, User.admin, User.user_id).all()}
        return rows

    @staticmethod
    def get_names_all_users() -> list:
        return [name[0] for name in session.query(User.name).all()]

    @staticmethod
    def add_user_system(name: str, password: str or int, comment: str = None, admin: bool = False):
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

    #################################
    #      НАИМЕНОВАНИЯ РАБОТ
    ################################
    @staticmethod
    def add_name_work(name, user) -> bool:
        try:
            if session.query(TableNameWork.work_name).filter(TableNameWork.work_name == name).count() == 0:
                name_work = TableNameWork(work_name=name, user_id=user)
                session.add(name_work)
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
            session.query(TableNameWork).filter(TableNameWork.work_id == id_name).delete()
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
    def get_all_names_work_with_user_id(id_user: int):
        rows = session.query(TableNameWork.work_name, TableNameWork.work_id). \
            filter(TableNameWork.user_id == id_user).all()
        return rows

    @staticmethod
    def get_name_work_for_id(id_name):
        row = session.query(TableNameWork.work_name).filter(TableNameWork.work_id == id_name).one()
        return row[0]

    @staticmethod
    def get_name_work_id_for_work_name(work_name):
        row = session.query(TableNameWork.work_id).filter(TableNameWork.work_name == work_name).one()
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
    def add_new_string_work(user_name: str, name_work: str, name_stage: str,
                            name_build: str, level: str,
                            number_security: list,
                            number_duty: list,
                            number_worker: list,
                            number_itr: list, ):
        try:
            date = datetime.today().date()
            tb = TableWork
            if session.query(tb.work_sting_id). \
                    filter(tb.user_name == user_name, tb.name_work == name_work,
                           tb.name_stage == name_stage, tb.name_build == name_build,
                           tb.name_level == level, tb.date_created == date).count() == 0:
                session.add(TableWork(user_name=user_name, name_work=name_work, name_stage=name_stage,
                                      name_build=name_build, name_level=level,
                                      number_security_p=number_security[0], number_security_f=number_security[1],
                                      number_duty_p=number_duty[0], number_duty_f=number_duty[1],
                                      number_worker_p=number_worker[0], number_worker_f=number_worker[1],
                                      number_ITR_p=number_itr[0], number_ITR_f=number_itr[1], date_created=date
                                      ))
                session.flush()
                return True
        except:
            session.rollback()
            print(f'Ошибка записи в БД')
        finally:
            session.commit()

    @staticmethod
    def edit_form_string_with_id(id_string: str or int, name_stage: str, name_build: str,
                                 level: str,
                                 number_security: list,
                                 number_duty: list,
                                 number_worker: list,
                                 number_itr: list, ):
        tb = TableWork
        try:
            session.query(tb).filter(tb.work_sting_id == id_string). \
                update({"name_stage": name_stage, 'name_build': name_build, 'name_level': level,
                        'number_security_p': number_security[0], 'number_security_f': number_security[1],
                        'number_duty_p': number_duty[0], 'number_duty_f': number_duty[1],
                        'number_worker_p': number_worker[0], 'number_worker_f': number_worker[1],
                        'number_ITR_p': number_itr[0], 'number_ITR_f': number_itr[1]})
            session.flush()
            print('Форма успешно измененна')
            return True
        except:
            session.rollback()
            print('Что-то пошло не так. Изменить пользователя не удалось')
            return False
        finally:
            session.commit()

    @staticmethod
    def get_forms_with_user_with_name(user_name: str, name_work: str) -> List[
        Dict[str, Union[Dict[str, List[Any]], Any]]]:
        TB = TableWork
        rows = session.query(TB.user_name, TB.name_work, TB.name_stage, TB.name_build, TB.name_level, TB.date_created,
                             TB.number_security_p, TB.number_security_f, TB.number_duty_p, TB.number_duty_f,
                             TB.number_worker_p, TB.number_worker_f, TB.number_ITR_p, TB.number_ITR_f,
                             ).filter(TB.user_name == user_name, TB.name_work == name_work).all()
        return rows

    @staticmethod
    def get_name_forms_with_user_with_date(user_name, date):
        TB = TableWork
        return [name.name_work for name in
                session.query(TB.name_work).filter(TB.user_name == user_name, TB.date_created == date).distinct().all()]

    @staticmethod
    def del_str_form_with_name_work_or_id_form(id_form:str or int = None, name_work: str = None):
        try:
            if id_form:
                session.query(TableWork).filter(TableWork.work_sting_id == id_form).delete()
                print(f"Удаление id:{id_form}  успешно")
            elif name_work:
                session.query(TableWork).filter(TableWork.name_work == name_work).delete()
                print(f"Удаление name:{name_work} успешно")
            session.flush()
            return True
        except:
            session.rollback()
            print(f'Ошибка удаления {id_form} из БД')
            return False
        finally:
            session.commit()

    @staticmethod
    def get_ids_str_form_with_work_user_today(user_name: str, name_work: str) -> list:
        date_today = datetime.today().date()
        rows = session.query(TableWork.work_sting_id). \
            filter(TableWork.user_name == user_name,
                   TableWork.name_work == name_work,
                   TableWork.date_created == date_today).all()
        return [id_form.work_sting_id for id_form in rows]

    @staticmethod
    def check_that_str_form_with_id_in_db(id_str: int or str) -> bool:
        return True if session.query(TableWork.work_sting_id).filter(TableWork.work_sting_id == id_str).all() else False

    @staticmethod
    def get_str_form_with_id(id_str: int or str) -> list:
        TB = TableWork
        rows = session.query(TB.work_sting_id, TB.name_stage, TB.name_build, TB.name_level,
                             TB.number_security_p, TB.number_security_f, TB.number_duty_p, TB.number_duty_f,
                             TB.number_worker_p, TB.number_worker_f, TB.number_ITR_p, TB.number_ITR_f,
                             ).filter(TB.work_sting_id == id_str).all()
        return rows

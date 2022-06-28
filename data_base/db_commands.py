from datetime import datetime
from random import randint
from typing import List, Dict, Union, Any

from sqlalchemy import distinct, func
from data_base.database import session

from data_base.models import User, TableNameWork, base, engine, TableNameBuild, TableWork, TableReminder


class CommandsDB:
    @staticmethod
    def create_db():
        base.metadata.create_all(engine)
        CommandsDB.add_admin_user()

    ##############################
    #       ПОЛЬЗОВАТЕЛИ
    ##############################
    @staticmethod
    def get_user_with_id(id_user: str or int):
        """ Вернуть имя пользователя с ID """
        my_query = session.query(User.name, User.user_id).filter(User.user_id == id_user).all()
        if my_query:
            return my_query[0]
        return None

    @staticmethod
    def add_admin_user():
        try:
            if not session.query(User.name, User.user_id).filter(User.admin == True).all():
                session.add(User(name='Администратор',
                                 password="000000",
                                 admin=True))
                session.flush()
        except Exception as e:
            print(f'Не удалось добавить администратора в БД {e}')
            session.rollback()
        finally:
            session.commit()

    @staticmethod
    def get_user_id_with_name(name_user: str, id_gp: int or str):
        """ Получить ID пользователя по ему Имени """
        return session.query(User.user_id).filter(User.name == name_user, User.cont_id == id_gp).one()

    @staticmethod
    def get_all_users(user_password=False,
                      contractor: bool = False, gp: str = None, gp_id: int = None) -> list or dict:
        """ Получить список пользователей в БД
         user_password - получить словарь со всеми пользователями, ключ - PINCODE
         contractor - получить из БД массив только с Ген Подрядчиками
         gp - получить из БД массив подрядчиков только с ГП = gp"""
        if not user_password:
            if contractor:
                rows = session.query(User.user_id, User.name, User.password, User.contractor, ).filter(
                    User.contractor == True).all()
            else:
                rows = session.query(User.user_id, User.name, User.password). \
                    filter(User.cont_name == gp, User.contractor == False, User.cont_id == gp_id). \
                    order_by(User.name).all()
            return rows
        else:
            rows = {user[1]: [user[0], user[2], user[3], user[4], user[5], user[6]] for user in
                    session.query(User.name, User.password, User.admin, User.user_id,
                                  User.cont_name, User.contractor, User.cont_id).all()}
        return rows

    @staticmethod
    def get_all_get_contractors() -> list:
        """ Получить отсортированный список кортежей с Ген подрядчиками"""
        rows = session.query(User.user_id, User.name, User.password,
                             User.admin, User.cont_name, User.contractor).order_by(User.name).all()
        return rows

    @staticmethod
    def get_all_user_with_gp(gp: str) -> list:
        """ Получить все имена Пользователей с ГП """
        return [name[0] for name in session.query(User.name).filter(User.cont_name == gp).order_by(User.name).all()]

    @staticmethod
    def get_all_gp() -> list:
        """ Получить все имена ГП """
        return [name[0] for name in session.query(User.name).filter(User.contractor == True).order_by(User.name).all()]

    @staticmethod
    def add_get_contractor(name: str, password: str or int):
        """ Добавить ГП в БД """
        try:
            if session.query(User.name).filter(User.name == name).count() == 0:
                session.add(User(name=name,
                                 password=password,
                                 contractor=True))
                session.flush()
                return True
            else:
                print(f"Ген Подрядчик {name}, уже есть в БД")
                return False
        except:
            session.rollback()
            print(f'Ошибка записи {name} в БД')
            return False
        finally:
            session.commit()

    @staticmethod
    def add_user_with_gp(name: str, password: str or int, gp: str, id_gp: int):
        """ Добавить Подрядчика под ГП в БД """
        try:
            if session.query(User.name).filter(User.name == name, User.cont_name == gp).count() == 0:
                session.add(User(name=name,
                                 password=password,
                                 contractor=False,
                                 cont_name=gp,
                                 cont_id=id_gp))
                session.flush()
                return True
            else:
                print(f"Подрядчик {name}, уже есть в БД")
                return False
        except:
            session.rollback()
            print(f'Ошибка записи {name} в БД')
            return False
        finally:
            session.commit()

    @staticmethod
    def update_name_user_with_gp_with_name(id_user: int, new_name: str, gp: str):
        try:
            session.query(User).filter(User.user_id == id_user, User.cont_name == gp).update({"name": new_name})
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
    def update_gp_user_with_name(name: str, new_name: str):
        try:
            session.query(User).filter(User.name == name, User.contractor == True).update({"name": new_name})
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
        """ Получить запись из БД с PINCOCDE пользователя с именем name """
        return session.query(User.password).filter(User.name == name).one()[0]

    @staticmethod
    def get_password_user_with_name_with_gp(name: str, gp: str):
        """ Получить запись из БД с PINCOCDE пользователя с именем name и ГП gp"""
        return session.query(User.password).filter(User.name == name, User.cont_name == gp).one()[0]

    @staticmethod
    def update_pincode_user_with_name(id_user: int, new_pin: int or str):
        """ Изменить PINCODE пользователя с id_user """
        try:
            session.query(User).filter(User.user_id == id_user).update({"password": new_pin})
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
    def delete_user_with_id(id_user: int or str):
        """ Удалить пользователя с ID """
        try:
            session.query(User).filter(User.user_id == id_user).delete()
            session.flush()
        except:
            session.rollback()
            print(f'Ошибка удаления пользователя с ID {id_user} из БД')
        finally:
            print(f"Удаление прошло успешно.Пользователь с ID {id_user}")
            session.commit()

    #################################
    #      НАИМЕНОВАНИЯ РАБОТ
    ################################
    @staticmethod
    def add_name_work(name: str, user_id: str or int, is_gp: bool) -> bool:
        """ Добавить наименование работ  """
        try:
            if session.query(TableNameWork.work_name).filter(TableNameWork.work_name == name,
                                                             TableNameWork.user_id == user_id,
                                                             TableNameWork.is_gp == is_gp).count() == 0:
                name_work = TableNameWork(work_name=name, user_id=user_id)
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
        """ Удалить наименование работ по ID """
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
        return row

    ##################################
    #             ЗДАНИЯ
    #################################
    @staticmethod
    def add_name_build(name: str, gp: str, id_gp: int) -> bool:
        """ Добавить здание в БД с ГП (gp) """
        try:
            if session.query(TableNameBuild.name_build). \
                    filter(TableNameBuild.name_build == name, TableNameBuild.name_cont == gp).count() == 0:
                session.add(TableNameBuild(name_build=name, name_cont=gp, id_cont=id_gp))
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
    def del_name_build(build_id: str or int):
        """ Удаление здание с ID """
        try:
            session.query(TableNameBuild).filter(TableNameBuild.build_id == build_id).delete()
            session.flush()
            print(f"Удаление {build_id} успешно")
            return True
        except:
            session.rollback()
            print(f'Ошибка удаления {build_id} из БД')
            return False
        finally:
            session.commit()

    @staticmethod
    def get_all_builds_with_gp(gp: str) -> list:
        """ Получить все здания с ГП (gp) """
        rows = session.query(TableNameBuild.build_id, TableNameBuild.name_build, TableNameBuild.name_cont) \
            .filter(TableNameBuild.name_cont == gp) \
            .order_by(TableNameBuild.name_build).all()
        return rows

    @staticmethod
    def get_all_builds_with_id_gp(gp_id: str or int) -> list:
        """ Получение всех зданий, добавленных gp_id  """
        rows = session.query(TableNameBuild.build_id, TableNameBuild.name_build, TableNameBuild.name_cont) \
            .filter(TableNameBuild.id_cont == gp_id) \
            .order_by(TableNameBuild.name_build).all()
        return rows

    @staticmethod
    def get_name_build_with_id(build_id):
        """ Получить наименование здание по ID """
        rows = session.query(TableNameBuild.name_build).filter(TableNameBuild.build_id == build_id).one()
        return rows[0]

    ###############################
    #   ЗАПИСЬ ФОРМЫ ТАБЕЛЯ
    ###############################
    @staticmethod
    def add_new_string_work(user_name: str, name_work: str, name_stage: int,
                            name_build: str, level: str, number_security: list,
                            number_duty: list, number_worker: list, number_itr: list,
                            contractor: str, is_gp: bool, id_gp: int):
        """ Добавить запись формы в БД """
        try:
            date = datetime.today().date()
            tb = TableWork
            if session.query(tb.work_sting_id). \
                    filter(tb.user_name == user_name, tb.name_work == name_work,
                           tb.name_stage == name_stage, tb.name_build == name_build,
                           tb.name_level == level, tb.date_created == date, tb.contractor == contractor).count() == 0:
                session.add(TableWork(user_name=user_name, name_work=name_work, name_stage=name_stage,
                                      name_build=name_build, name_level=level.upper(),
                                      number_security_p=number_security[0], number_security_f=number_security[1],
                                      number_duty_p=number_duty[0], number_duty_f=number_duty[1],
                                      number_worker_p=number_worker[0], number_worker_f=number_worker[1],
                                      number_ITR_p=number_itr[0], number_ITR_f=number_itr[1], date_created=date,
                                      contractor=contractor, form_is_gp=is_gp, id_gp=id_gp
                                      ))
                session.flush()
                return True
        except:
            session.rollback()
            print(f'Ошибка записи в БД')
            return False
        finally:
            session.commit()

    @staticmethod
    def edit_form_string_with_id(id_string: str or int, name_stage: str, name_build: str,
                                 level: str,
                                 number_security: list,
                                 number_duty: list,
                                 number_worker: list,
                                 number_itr: list,
                                 contractor: str):
        """ Редактировать запись формы с id_string """
        tb = TableWork
        try:
            session.query(tb).filter(tb.work_sting_id == id_string). \
                update({"name_stage": name_stage, 'name_build': name_build, 'name_level': level.upper(),
                        'number_security_p': number_security[0], 'number_security_f': number_security[1],
                        'number_duty_p': number_duty[0], 'number_duty_f': number_duty[1],
                        'number_worker_p': number_worker[0], 'number_worker_f': number_worker[1],
                        'number_ITR_p': number_itr[0], 'number_ITR_f': number_itr[1],
                        'contractor': contractor
                        })
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
    def get_name_forms_with_user_with_date(user_name: str, date: datetime.today().date(),
                                           id_gp: int):
        """ Получить наименования работ созданным пользователем """
        TB = TableWork
        return [(name.name_work, name.id_gp) for name in
                session.query(TB.name_work, TB.contractor, TB.id_gp).
                    filter(TB.user_name == user_name, TB.date_created == date, TB.id_gp == id_gp).distinct().all()]

    @staticmethod
    def del_str_form_with_name_work_or_id_form(id_form: str or int = None, name_work: str = None):
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
    def get_ids_str_form_with_work_user_today(user_name: str, name_work: str, contractor: str) -> list:
        """ Получить ID записей формы у пользователя user_name с ГП contractor """
        date_today = datetime.today().date()
        rows = session.query(TableWork.work_sting_id). \
            filter(TableWork.user_name == user_name,
                   TableWork.name_work == name_work,
                   TableWork.date_created == date_today,
                   TableWork.contractor == contractor) \
            .order_by(TableWork.name_stage, TableWork.name_build, TableWork.name_level).all()
        return [id_form.work_sting_id for id_form in rows]

    @staticmethod
    def get_stages_today_from_form(cont: str or int) -> list:
        """ Получить из БД Этапы работы с ген подрядчиком (по id)"""
        date_today = datetime.today().date()
        row = session.query(TableWork.name_stage).filter(TableWork.date_created == date_today,
                                                         TableWork.id_gp == cont).distinct().all()
        return [i[0] for i in row]

    @staticmethod
    def get_names_work_companies_from_form(id_gp: int or str):
        """ Получить наименование компании и работ из ДБ по id_GP """
        date_today = datetime.today().date()
        row = session.query(TableWork.user_name, TableWork.name_work, TableWork.form_is_gp).filter(
            TableWork.date_created == date_today,
            TableWork.id_gp == id_gp).order_by(TableWork.user_name).distinct().all()
        return row

    @staticmethod
    def check_that_str_form_with_id_in_db(id_str: int or str) -> bool:
        """ Проверить, что запись формы с ID есть в БД """
        return True if session.query(TableWork.work_sting_id).filter(TableWork.work_sting_id == id_str).all() else False

    @staticmethod
    def get_str_form_with_id(id_str: int or str) -> list:
        """ Получить запись формы из БД по ID Записи """
        TB = TableWork
        rows = session.query(TB.work_sting_id, TB.contractor, TB.name_stage, TB.name_build, TB.name_level,
                             TB.number_security_p, TB.number_security_f, TB.number_duty_p, TB.number_duty_f,
                             TB.number_worker_p, TB.number_worker_f, TB.number_ITR_p, TB.number_ITR_f,
                             ).filter(TB.work_sting_id == id_str).all()
        return rows

    @staticmethod
    def get_all_str_from_form_with_cont(gp_id: str or int) -> list:
        """ Получить все записи с Ген подрядчиком по gp_ID """
        TB = TableWork
        date_today = datetime.today().date()
        rows = session.query(TB.name_stage, TB.name_build, TB.name_level, TB.contractor, TB.user_name, TB.name_work,
                             TB.number_security_p, TB.number_security_f,
                             TB.number_duty_p, TB.number_duty_f,
                             TB.number_worker_p, TB.number_worker_f,
                             TB.number_ITR_p, TB.number_ITR_f, TB.form_is_gp
                             ).filter(TB.id_gp == gp_id, TB.date_created == date_today).order_by(TB.name_stage,
                                                                                                 TB.name_build,
                                                                                                 TB.name_level).all()
        return rows

    @staticmethod
    def get_all_str_from_table() -> list:
        TB = TableWork
        rows = session.query(TB.work_sting_id, TB.user_name, TB.contractor, TB.name_work, TB.date_created,
                             TB.name_stage, TB.name_build, TB.name_level,
                             TB.number_security_p, TB.number_security_f, TB.number_duty_p, TB.number_duty_f,
                             TB.number_worker_p, TB.number_worker_f, TB.number_ITR_p, TB.number_ITR_f,
                             ).all()

        return rows

    ###################
    #   USER_CHAT_IDS
    ###################
    @staticmethod
    def add_new_chat_id_user(chat_id: str or int):
        """ Добавить нового пользователя в БД напоминания и дать статус True или добавить напоминание зашедшему юзеру"""
        try:
            TB = TableReminder
            if session.query(TB.chat_id, TB.is_remind).filter(TB.chat_id == chat_id).count() == 0:
                session.add(TableReminder(chat_id=chat_id, is_remind=True))
                session.flush()
                return True
            else:
                session.query(TB).filter(TB.chat_id == chat_id).update({'is_remind': True})
                session.flush()
        except Exception as e:
            session.rollback()
            print(f'Ошибка записи в БД {e}')
            return False
        finally:
            session.commit()

    @staticmethod
    def change_state_reminder_chat_id(chat_id: str or int, is_remind: bool):
        """ Изменить состояние напоминаиня пользователя с chat_id на is_remind """
        TB = TableReminder
        try:
            if session.query(TB.chat_id, TB.is_remind).filter(TB.chat_id == chat_id).count() == 1:
                session.query(TB).filter(TB.chat_id == chat_id).update({'is_remind': is_remind})
                session.flush()
                return True
        except Exception as e:
            session.rollback()
            print(f'Не удалось редактировать запись{chat_id}. Except: {e}')
            return False
        finally:
            session.commit()

    @staticmethod
    def get_users_with_chat_id_is_remind():
        TB = TableReminder
        return session.query(TB.chat_id).filter(TB.is_remind == True).all()

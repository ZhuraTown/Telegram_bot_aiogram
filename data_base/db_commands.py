from random import randint
from sqlalchemy import distinct, func
from data_base.database import session

from .models import User


class CommandsDB:

    @staticmethod
    def get_user_with_name(name):
        my_query = session.query(User.name, User.user_id).filter(User.name == name).all()
        return my_query

    @staticmethod
    def get_all_users():
        rows = session.query(User.user_id, User.name, User.comment, User.password).all()
        return rows

    @staticmethod
    def add_user_system(name, comment):
        try:
            if session.query(User.name).filter(User.name == name).count() == 0:
                session.add(User(name=name,
                                 password=f'{randint(1000, 9999)}',
                                 comment=comment))
                session.flush()
            else:
                print(f"Пользователь с именем {name}, уже есть в БД")
        except:
            session.rollback()
            print(f'Ошибка записи {name} в БД')
        finally:
            session.commit()

    @staticmethod
    def update_user_with_name(name, new_name):
        session.query(User).filter(User.name == name).update({"name": new_name})

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

    @staticmethod
    def get_count(name):
        return session.query(User.name).filter(User.name == name).count()

from itertools import cycle
from datetime import datetime
from data_base.db_commands import CommandsDB
import random


# Записи в БД
# coms = CommandsDB.get_all_users(without_admin=True)
# date_today = datetime.today().date()
#
# stgs = [5, 10, 13, 15]
# contractor = [coms[0][1], coms[1][1]]
# builds = [i[1] for i in CommandsDB.get_all_names_builds()]
# lvls = cycle([f"{i}L" for i in range(1, 10)])
#
# for company in coms:
#     name_work = random.choice(CommandsDB.get_all_names_work_with_user_id(company[0]))[0]
#     for cont in contractor:
#         for build in builds:
#             stg = random.choice(stgs)
#             lv = next(lvls)
#             workers = {'Рабочие': 0, 'Дежурный': 0, 'ИТР': 0, 'Охрана': 0}
#             for i in workers:
#                 num = random.randint(1, 10)
#                 workers[i] = [num, num]
#             CommandsDB.add_new_string_work(company[1], name_work, stg, build, lv,
#                                            workers["Охрана"], workers["Дежурный"],
#                                            workers["Рабочие"], workers["ИТР"], cont)
#

# for line in CommandsDB.get_all_users(without_admin=True):
#     CommandsDB.add_name_work(user=line[0], name=next(names_work))
# for line in CommandsDB.get_all_users(without_admin=True):
#     print(line)

# print(CommandsDB.get_all_names_work_with_user_id(2))
# print(CommandsDB.get_all_users(without_admin=True))
# #
# for line in CommandsDB.get_all_str_from_table():
#     CommandsDB.del_str_form_with_name_work_or_id_form(line[0])
#     ## print(line)

#
# cont = "АПА"
# for line in CommandsDB.get_all_str_from_form_with_cont(cont):
#     print(line)
# #
# for line in CommandsDB.get_all_str_from_table():
#     print(line)

# Наименования работ
# names_work = ['АУВПТ, ВПВ', 'Обеспечение', '"Электрика(ЭОМ,СГП)"', 'Связь', 'Вода(ОВ1)']
# for user, name in zip(CommandsDB.get_all_users(without_admin=True), names_work):
#     # CommandsDB.add_name_work(name, user[0])
#     print(user)
#
# CommandsDB.add_name_work('Обеспечение', 2)
from itertools import cycle
from datetime import datetime
from data_base.db_commands import CommandsDB
import random

# coms = CommandsDB.get_names_all_users(without_admin=True)
# date_today = datetime.today().date()
# name_works = ['Электрика', "Воздух", "Внешний монтаж", "Обеспечение"]
# stgs = [5, 10, 13, 15]
# contractor = [coms[0], coms[1]]
# builds = [i[1] for i in CommandsDB.get_all_names_builds()]
# lvls = cycle([f"{i}L" for i in range(1, 10)])
#
# for company in coms:
#     name_work = random.choice(name_works)
#     for cont in contractor:
#         for build in builds:
#             stg = random.choice(stgs)
#             lv = next(lvls)
#             workers = {'Рабочие': 0, 'Дежурный': 0, 'ИТР': 0, 'Охрана': 0}
#             for i in workers:
#                 num = random.randint(1, 10)
#                 workers[i] = [num, num]
#             CommandsDB.add_new_string_work(company, name_work, stg, build, lv,
#                                            workers["Охрана"], workers["Дежурный"],
#                                            workers["Рабочие"], workers["ИТР"], cont)

for line in CommandsDB.get_all_str_from_table():
    print(line)
import itertools
from string import ascii_uppercase

import xlsxwriter
import datetime
import os

from itertools import cycle

__path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
__excel_creator_dir = 'excel_creator'
__time_sheet_xls_dir = 'time_sheet_xls'
__path_to_dir = os.path.join(__path, __excel_creator_dir, __time_sheet_xls_dir)


class ExcelFormat:

    def __init__(self, work_book):
        self.work_book = work_book

    def date_format(self):
        data_format = self.work_book.add_format()
        data_format.set_font("Times New Roman")
        data_format.set_bold()
        data_format.set_border(1)
        data_format.set_align('centre')
        data_format.set_align('vcenter')
        data_format.set_font_size(18)
        return data_format

    def title_format(self):
        title_format = self.work_book.add_format()
        title_format.set_font("Times New Roman")
        title_format.set_font_size(26)
        title_format.set_bold()
        title_format.set_align('center')
        return title_format

    def companies_format(self, set_bold: bool = True, set_border: bool = False):
        companies_format = self.work_book.add_format()
        companies_format.set_font("Times New Roman")
        if set_bold:
            companies_format.set_bold()
        if set_border:
            companies_format.set_border(2)
        else:
            companies_format.set_border(1)
        companies_format.set_align('centre')
        companies_format.set_align('vcenter')
        companies_format.set_font_size(18)
        return companies_format

    def tb_tm_sh_title(self, set_bold: bool = True, set_border: bool = True):
        tb_time_sheet = self.work_book.add_format()
        tb_time_sheet.set_font("Times New Roman")
        if set_bold:
            tb_time_sheet.set_bold()
        if set_border:
            tb_time_sheet.set_border(2)
        else:
            tb_time_sheet.set_border(1)
        tb_time_sheet.set_align('vcenter')
        tb_time_sheet.set_align('center')
        tb_time_sheet.set_text_wrap()
        tb_time_sheet.set_font_size(11)
        return tb_time_sheet

    def tb_cell_write(self, set_bold: bool = False, grey: bool = False,
                      set_top_line: bool = False, red_font: bool = False,
                      set_bold_border: bool = False, set_right_line: bool = False,
                      set_right_line_b: bool = False):
        """
        set_bold - сделать шрифт полужирным
        grey - закрасить ячейку в цвет
        top_line - нарисовать толстую линию сверху ячейки
        """
        tb_cell = self.work_book.add_format()
        tb_cell.set_font("Times New Roman")
        if set_bold:
            tb_cell.set_bold()
        if grey:
            tb_cell.set_bg_color("#F2F2F2")
        if set_bold_border:
            tb_cell.set_border(2)
        else:
            tb_cell.set_border(1)
        if set_right_line:
            tb_cell.set_right(2)
        if set_right_line_b:
            tb_cell.set_right(5)
        if set_top_line:
            tb_cell.set_top(2)
        if red_font:
            tb_cell.set_font_color('red')
        tb_cell.set_align('vcenter')
        tb_cell.set_align('center')
        tb_cell.set_text_wrap()
        tb_cell.set_font_size(11)
        return tb_cell

    def tb_plan_format(self, set_bold: bool = True, set_border: bool = True):
        tb_plan = self.work_book.add_format()
        tb_plan.set_font("Times New Roman")
        if set_bold:
            tb_plan.set_bold()
        if set_border:
            tb_plan.set_border(2)
        else:
            tb_plan.set_border(1)
        tb_plan.set_bg_color("#F2F2F2")
        tb_plan.set_align('centre')
        tb_plan.set_align('vcenter')
        tb_plan.set_font_size(18)
        return tb_plan


class ExcelWriter:
    __path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    __excel_creator_dir = 'excel_creator'
    __time_sheet_xls_dir = 'time_sheet_xls'
    __path_to_dir = os.path.join(__path, __excel_creator_dir, __time_sheet_xls_dir)

    def __init__(self, name_document: str):
        self.date = datetime.datetime.today().date()
        self.name = f"{name_document}_{self.date}.xlsx"
        # Создание папки для хранения отчетов
        if not os.path.exists(self.__path_to_dir):
            os.mkdir(self.__path_to_dir)
        self.workbook = xlsxwriter.Workbook(os.path.join(self.__path_to_dir, self.name))
        self.format = ExcelFormat(self.workbook)
        self.cur_row = 6
        self._result_row = 0
        self._summ_row_start = 0
        self._summ_row_finish = 0
        self._last_colm_workers = 0
        self._row_plan_workers = 0
        self.letters_excel = self.create_letters_excel()

    def create_letters_excel(self):
        def iter_all_strings():
            for size in itertools.count(1):
                for s in itertools.product(ascii_uppercase, repeat=size):
                    yield "".join(s)
        answer = {}
        for i, lt in zip(range(0, 101), iter_all_strings()):
            if i == 100:
                break
            answer[i] = lt
        return answer

    def get_path_to_file(self):
        """ Путь к файлу где хранится таблица """
        return os.path.join(self.__path_to_dir, self.name)

    def _add_worksheet(self, cont):
        """ Создание листа """
        self.cur_row = 6
        if '/' in cont:
            cont = '_'.join(cont.split('/'))
        elif '\\' in cont:
            cont = '_'.join(cont.split("\\"))
        elif ':' in cont:
            cont = '_'.join(cont.split(':'))
        elif '*' in cont:
            cont = '_'.join(cont.split('*'))
        elif '?' in cont:
            cont = '_'.join(cont.split('?'))
        elif '[' in cont:
            cont = '_'.join(cont.split('['))
        elif ']' in cont:
            cont = '_'.join(cont.split(']'))
        self.worksheet = self.workbook.add_worksheet(name=cont)
        self.worksheet.set_default_row(28)
        self._total_plan_fact_companies = {}

    def close(self):
        self.workbook.close()

    def _write_title_work(self, count_companies: int, stages_db: list):
        """ Заполнение оглавления табеля (Численность персонала, задействованного...) """
        len_title = 4 + count_companies * 8 + 2 if 4 + count_companies * 8 + 2 >= 24 else 24
        row_title = 1
        stages = stages_db
        stages.sort()
        stages = [str(i) for i in stages]
        stages_for_title = ', '.join(stages)
        a = f'Численность персонала, задействованного на этапах {stages_for_title}  по Обустройству МФК "Лахта центр'
        self.worksheet.merge_range(row_title, 0, row_title, len_title, a, self.format.title_format())

    def _write_date_work(self):
        """ Заполнение даты заполнения табеля """
        row = 3
        date = self.date.strftime('%d.%m.%Y')
        self.worksheet.merge_range(row, 0, row, 3, date, self.format.date_format())

    def _write_title_table_companies(self):
        """ Заполнение оглавления таблицы Подрядчики (Компания План Факт Дефицит) """
        row = 5
        col_comp, col_pl, col_f, col_def = 0, 4, 6, 8
        self.worksheet.merge_range(row, col_comp, row, col_comp + 3,
                                   'Подрядчик', self.format.companies_format(set_border=True))
        self.worksheet.merge_range(row, col_pl, row, col_pl + 1,
                                   'План', self.format.tb_plan_format(set_border=True))
        self.worksheet.merge_range(row, col_f, row, col_f + 1,
                                   'Факт', self.format.companies_format(set_border=True))
        self.worksheet.merge_range(row, col_def, row, col_def + 1,
                                   'Дефицит', self.format.companies_format(set_border=True))

    def write_companies_to_tb(self, nms_comps: list):
        """ Заполнение таблицы Подрядчики (Компания План Факт Дефицит) """
        self._row_compis_in_total_tb = self.cur_row
        col_comp, col_pl, col_f, col_def = 0, 4, 6, 8
        tb_names = {}
        for name in nms_comps:
            if name[0] not in tb_names:
                self.worksheet.merge_range(self.cur_row, col_comp, self.cur_row, col_comp + 3,
                                           name[0], self.format.companies_format(set_bold=False))
                tb_names[name[0]] = 0
                self.cur_row += 1
            # Старый кусок кода
            # self.worksheet.merge_range(self.cur_row, col_pl, self.cur_row, col_pl + 1,
            #                            num_0, self.format.tb_plan_format(set_bold=False, set_border=False))
            # self.worksheet.merge_range(self.cur_row, col_f, self.cur_row, col_f + 1,
            #                            num_0, self.format.companies_format(set_bold=False))
            # self.worksheet.merge_range(self.cur_row, col_def, self.cur_row, col_def + 1,
            #                            num_0, self.format.companies_format(set_bold=False))

    def write_total_nums_works_to_tb(self, nms_comps: list):
        row = self._row_compis_in_total_tb
        col_comp, col_pl, col_f, col_def = 0, 4, 6, 8
        nums = self._total_plan_fact_companies
        names_to_tb = {}

        for name in nms_comps:
            name = name[0]
            if name not in names_to_tb:
                names_to_tb[name] = 0
                self.worksheet.merge_range(row, col_pl, row, col_pl + 1,
                                           nums[name]['План'], self.format.tb_plan_format(set_bold=False, set_border=False))
                self.worksheet.merge_range(row, col_f, row, col_f + 1,
                                           nums[name]['Факт'], self.format.companies_format(set_bold=False))
                self.worksheet.merge_range(row, col_def, row, col_def + 1,
                                           nums[name]['Факт'] - nums[name]['План'], self.format.companies_format(set_bold=False))
                row += 1

        # Подсчет итого План и Факт по компаниям
        sum_p = 0
        sum_f = 0
        for name in nums:
            sum_p += nums[name]['План']
            sum_f += nums[name]['Факт']

        self.worksheet.merge_range(row, col_comp, row, col_comp + 3,
                                   "Итого", self.format.companies_format(set_border=True))
        self.worksheet.merge_range(row, col_pl, row, col_pl + 1,
                                   sum_p, self.format.tb_plan_format(set_border=True))
        self.worksheet.merge_range(row, col_f, row, col_f + 1,
                                   sum_f, self.format.companies_format(set_border=True))
        self.worksheet.merge_range(row, col_def, row, col_def + 1,
                                   ' ', self.format.companies_format(set_border=True))

    def write_title_tb_tm_sh(self):
        """ Оглавление таблицы Этап Здание Этаж Подрядчик"""
        row = self.cur_row + 4
        for i in range(0, 4):
            """ Растягиваю по высоте строки"""
            self.worksheet.set_row(row + i, height=30)
        self.worksheet.merge_range(row, 0, row + 2, 0, 'Этап', self.format.tb_tm_sh_title())
        self.worksheet.merge_range(row, 1, row + 2, 1, 'Здание', self.format.tb_tm_sh_title())
        self.worksheet.merge_range(row, 2, row + 2, 2, 'Этаж', self.format.tb_tm_sh_title())
        self.worksheet.set_column(3, 3, width=18)
        self.worksheet.merge_range(row, 3, row + 2, 3, 'Основной\nподрядчик', self.format.tb_tm_sh_title())

    def write_title_companies_tb(self, companies_and_work: list):
        """ Заполнение подрядчиками и наименованиями работ оглавления таблицы табеля времени"""
        self.column_companies_work = {}
        row_name_comp = self.cur_row + 3
        row_name_work = row_name_comp + 1
        row_titles_workers = row_name_work + 1
        row_plan_fact_workers = row_titles_workers + 1
        self._row_plan_workers = row_plan_fact_workers

        col_comp = 4
        titles_1 = ['Охрана', "Дежурный", "Рабочие", "ИТР ПТО"]
        titles_2 = ["Рабочие", "ИТР"]
        for comp_and_work in companies_and_work:

            if bool(comp_and_work[2]):
                """Сужаю по ширине столбцы"""
                self.worksheet.set_column(col_comp, col_comp + 7, width=7)
                self.worksheet.merge_range(row_name_comp, col_comp, row_name_comp, col_comp + 7,
                                           comp_and_work[0], self.format.tb_tm_sh_title())
                # name_work = comp_and_work[1] if len(comp_and_work) > 1 else 'Нет наименования работ'
                self.worksheet.merge_range(row_name_work, col_comp, row_name_work, col_comp + 7,
                                           comp_and_work[1], self.format.tb_tm_sh_title())

                # Сохраняю номер колонки для Подрядчика и наименования работ
                self.column_companies_work[(comp_and_work[0], comp_and_work[1])] = col_comp
                # Создаю счетчик для компании по сотрудникам План и Факт
                if not self._total_plan_fact_companies.get(comp_and_work[0]):
                    self._total_plan_fact_companies[comp_and_work[0]] = {"План": 0, "Факт": 0}


                for i, title in zip(range(0, 4), titles_1):
                    self.worksheet.merge_range(row_titles_workers, col_comp + i * 2, row_titles_workers,
                                               col_comp + i * 2 + 1,
                                               title, self.format.tb_tm_sh_title(set_bold=True))
                    self.worksheet.write(row_plan_fact_workers, col_comp + i * 2,
                                         'План', self.format.tb_tm_sh_title(set_bold=False, set_border=False))
                    self.worksheet.write(row_plan_fact_workers, col_comp + i * 2 + 1,
                                         'Факт', self.format.tb_tm_sh_title(set_bold=False, set_border=False))
                col_comp += 8
            else:
                """Сужаю по ширине столбцы"""
                self.worksheet.set_column(col_comp, col_comp + 3, width=7)
                self.worksheet.merge_range(row_name_comp, col_comp, row_name_comp, col_comp + 3,
                                           comp_and_work[0], self.format.tb_tm_sh_title())
                # name_work = comp_and_work[1] if len(comp_and_work) > 1 else 'Нет наименования работ'
                self.worksheet.merge_range(row_name_work, col_comp, row_name_work, col_comp + 3,
                                           comp_and_work[1], self.format.tb_tm_sh_title())

                # Сохраняю номер колонки для Подрядчика и наименования работ
                self.column_companies_work[(comp_and_work[0], comp_and_work[1])] = col_comp
                # Создаю счетчик для компании по сотрудникам План и Факт
                if not self._total_plan_fact_companies.get(comp_and_work[0]):
                    self._total_plan_fact_companies[comp_and_work[0]] = {"План": 0, "Факт": 0}


                for i, title in zip(range(0, 2), titles_2):
                    self.worksheet.merge_range(row_titles_workers, col_comp + i * 2, row_titles_workers,
                                               col_comp + i * 2 + 1,
                                               title, self.format.tb_tm_sh_title(set_bold=True))
                    self.worksheet.write(row_plan_fact_workers, col_comp + i * 2,
                                         'План', self.format.tb_tm_sh_title(set_bold=False, set_border=False))
                    self.worksheet.write(row_plan_fact_workers, col_comp + i * 2 + 1,
                                         'Факт', self.format.tb_tm_sh_title(set_bold=False, set_border=False))
                col_comp += 4

        self._last_colm_workers = col_comp
        self.worksheet.merge_range(row_name_work, col_comp, row_titles_workers, col_comp+1, 'ИТОГО',
                                   self.format.tb_tm_sh_title(set_bold=True))
        self.worksheet.write(row_plan_fact_workers, col_comp,
                             'План', self.format.tb_tm_sh_title(set_bold=False, set_border=True))
        self.worksheet.write(row_plan_fact_workers, col_comp + 1,
                             'Факт', self.format.tb_tm_sh_title(set_bold=False, set_border=True))

    def write_builds_st_lv_tb(self, data_from_db: list):
        """
        Заполнение строк Этап Здание Этаж Ген Подрядчик
        """
        self.rows_stage_build_work = {}
        row = self.cur_row + 7
        self._summ_row_start = row
        grey_color = cycle([False, True])
        cols = [0, 1, 2, 3]
        # Для рисования линий разделения этапов работы
        for_line = {}
        for line in data_from_db:
            color = next(grey_color)
            if line[0] not in for_line:
                for_line[line[0]] = 0
                format_cell = self.format.tb_cell_write(grey=color, set_top_line=True)
                format_cell_b = self.format.tb_cell_write(grey=color, set_top_line=True, set_bold=True)
                format_cell_r = self.format.tb_cell_write(grey=color, set_top_line=True,
                                                          set_right_line=True, set_bold=True)
                format_cell_r_b = self.format.tb_cell_write(grey=color, set_top_line=True,
                                                            set_right_line_b=True, set_bold=True)
                self.worksheet.write(row, cols[3], line[3], self.format.tb_cell_write(grey=color,
                                                                                      set_right_line=True,
                                                                                      set_top_line=True))
                num_a = 1
                for i in range(4, self._last_colm_workers + 2):
                    if num_a == 8:
                        self.worksheet.write(row, i, '', format_cell_r_b)
                        num_a = 0
                    elif num_a == 4:
                        self.worksheet.write(row, i, '', format_cell_r_b)
                    elif num_a % 2 == 0:
                        self.worksheet.write(row, i, '', format_cell_r)
                    else:
                        self.worksheet.write(row, i, '', format_cell)
                    num_a += 1
            else:
                format_cell = self.format.tb_cell_write(grey=color)
                format_cell_b = self.format.tb_cell_write(grey=color, set_bold=True)
                format_cell_r = self.format.tb_cell_write(grey=color, set_right_line=True, set_bold=True)
                format_cell_r_b = self.format.tb_cell_write(grey=color, set_right_line_b=True, set_bold=True)
                self.worksheet.write(row, cols[3], line[3], self.format.tb_cell_write(grey=color,
                                                                                      set_right_line=True))
                num_a = 1
                for i in range(4, self._last_colm_workers + 2):
                    if num_a == 8:
                        self.worksheet.write(row, i, '', format_cell_r_b)
                        num_a = 0
                    elif num_a == 4:
                        self.worksheet.write(row, i, '', format_cell_r_b)
                    elif num_a % 2 == 0:
                        self.worksheet.write(row, i, '', format_cell_r)
                    else:
                        self.worksheet.write(row, i, '', format_cell)
                    num_a += 1
            self.worksheet.write(row, cols[0], int(line[0]), format_cell)
            self.worksheet.write(row, cols[1], line[1], format_cell)
            self.worksheet.write(row, cols[2], line[2], format_cell)
            self.rows_stage_build_work[(int(line[0]), line[1], line[2], line[3])] = [row, format_cell_b, format_cell_r, format_cell_r_b]
            row += 1

        for i in range(0, self._last_colm_workers + 2):
            self.worksheet.write(row, i, '', self.format.tb_cell_write(grey=True, set_bold=True, set_bold_border=True))
            self.worksheet.write(row + 1, i, '', self.format.tb_cell_write(set_bold=True, set_bold_border=True))

        self.worksheet.merge_range(row, 0, row, 3,
                                   'ИТОГО', self.format.tb_cell_write(grey=True, set_bold=True, set_bold_border=True))
        self._summ_row_finish = row - 1
        self._result_row = row
        self.worksheet.merge_range(row + 1, 0, row + 1, 3,
                                   'ДЕФИЦИТ',
                                   self.format.tb_cell_write(set_bold=True, red_font=True, set_bold_border=True))

    def write_nums_workers(self, lns_form_nums_worker: list):
        """
        Заполнение ячеек Рабочие/ИТР/Охрана/Дежурный значениями
        lns_form_nums_worker запрос с БД с рабочими"""

        for line in lns_form_nums_worker:
            row = self.rows_stage_build_work[(line[0], line[1], line[2], line[3])][0]
            form_cell = self.rows_stage_build_work[(line[0], line[1], line[2], line[3])][1]
            form_cell_r = self.rows_stage_build_work[(line[0], line[1], line[2], line[3])][2]
            form_cell_r_b = self.rows_stage_build_work[(line[0], line[1], line[2], line[3])][3]
            columns = self.column_companies_work[(line[4], line[5])]
            numbers = line[6:14]
            numbers_2 = line[10:14]

            if bool(line[14]):
                """ Если строчка ГП, то заполнять 4 поля иначе 2  """
                for nums, col, num_col in zip(numbers, range(columns, columns + 8), range(1, 9)):
                    if num_col % 2 == 1:
                        self._total_plan_fact_companies[line[4]]['План'] += nums
                    else:
                        self._total_plan_fact_companies[line[4]]['Факт'] += nums
                    if num_col == 8 or num_col == 4:
                        self.worksheet.write(row, col, nums if nums != 0 else '', form_cell_r_b)
                    elif num_col % 2 == 0:
                        self.worksheet.write(row, col, nums if nums != 0 else '', form_cell_r)
                    else:
                        self.worksheet.write(row, col, nums if nums != 0 else '', form_cell)
            else:
                for nums, col, num_col in zip(numbers_2, range(columns, columns + 4), range(1, 5)):
                    if num_col % 2 == 1:
                        self._total_plan_fact_companies[line[4]]['План'] += nums
                    else:
                        self._total_plan_fact_companies[line[4]]['Факт'] += nums
                    if num_col == 4:
                        self.worksheet.write(row, col, nums if nums != 0 else '', form_cell_r_b)
                    elif num_col % 2 == 0:
                        self.worksheet.write(row, col, nums if nums != 0 else '', form_cell_r)
                    else:
                        self.worksheet.write(row, col, nums if nums != 0 else '', form_cell)


    def write_results_formulas_bottom(self):
        """ Формулы в строке ИТОГО внизу таблицы """
        row_formula = self._result_row + 1
        row_for_st = self._summ_row_start + 1
        row_for_fn = self._summ_row_finish + 1
        for i in range(4, self._last_colm_workers):
            lt = self.letters_excel[i]
            self.worksheet.write_formula(f'{lt}{row_formula}', f'=SUM({lt}{row_for_st}:{lt}{row_for_fn})', self.format.tb_cell_write(set_bold=True, set_bold_border=True))

    def write_results_formulas_right(self):
        """ Формулы в правом столбце ИТОГО """
        # Столбец куда записывать формулу ИТОГО План
        col_formula = self._last_colm_workers
        # Столбец начала заполнения значениями кол-ва работников
        col_st = 4
        # Столбец для записывания ИТОГО Факт
        col_fn = self._last_colm_workers - 1
        # Строка План Факт
        row_workers_plan = self._row_plan_workers + 1
        # Строки начала подсчёта работников и конец для СУММ
        row_for_st = self._summ_row_start + 1
        row_for_fn = self._summ_row_finish + 1
        lt_plan = self.letters_excel[col_formula]
        lt_fact = self.letters_excel[col_formula + 1]
        for i in range(row_for_st, row_for_fn + 1):
            lt_st = self.letters_excel[col_st]
            lt_fn = self.letters_excel[col_fn]
            self.worksheet.write_formula(f'{lt_plan}{i}', f'SUMIF({lt_st}{row_workers_plan}:{lt_fn}{row_workers_plan},'
                                                          f'"План",{lt_st}{i}:{lt_fn}{i})',
                                         self.format.tb_cell_write(set_bold=True, set_bold_border=True))
            self.worksheet.write_formula(f'{lt_fact}{i}', f'SUMIF({lt_st}{row_workers_plan}:{lt_fn}{row_workers_plan},'
                                                          f'"Факт",{lt_st}{i}:{lt_fn}{i})',
                                         self.format.tb_cell_write(set_bold=True, set_bold_border=True))
        res_row = self._result_row + 1
        self.worksheet.write_formula(f'{lt_plan}{res_row}', f"=SUM({lt_plan}{row_for_st}:{lt_plan}{row_for_fn})",
                                     self.format.tb_cell_write(set_bold=True, set_bold_border=True))
        self.worksheet.write_formula(f'{lt_fact}{res_row}', f"=SUM({lt_fact}{row_for_st}:{lt_fact}{row_for_fn})",
                                     self.format.tb_cell_write(set_bold=True, set_bold_border=True))

    def create_table_header(self, cont: str, stages_db: list, num_comps: int):
        """ Создание заголовка таблциы, наименоване листа, даты и шапки для таблицы подрядчиков """
        self._add_worksheet(cont)
        self._write_title_work(num_comps, stages_db)
        self._write_date_work()
        self._write_title_table_companies()

# #
# from data_base.db_commands import CommandsDB
#
# aa = ExcelWriter('First_doc')
# # ID ГП для поиска
# contractor_id = 2
# contractor_name = 'ЛИИС'
#
# stages = CommandsDB.get_stages_today_from_form(contractor_id)
# comps_and_work = CommandsDB.get_names_work_companies_from_form(contractor_id)
# aa.create_table_header(contractor_name, stages, len(comps_and_work))
# # Заполнение Этап, Здание, Этаж, Ген подрядчик
# lns_from_form_with_contactor = CommandsDB.get_all_str_from_form_with_cont(contractor_id)
# aa.write_companies_to_tb(comps_and_work)
# aa.write_title_tb_tm_sh()
# aa.write_title_companies_tb(comps_and_work)
# aa.write_builds_st_lv_tb(lns_from_form_with_contactor)
# aa.write_nums_workers(lns_from_form_with_contactor)
# aa.write_results_formulas_bottom()
# aa.write_results_formulas_right()
# aa.write_total_nums_works_to_tb(comps_and_work)
# aa.close()

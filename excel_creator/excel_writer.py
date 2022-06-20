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
                      set_bold_border: bool = False):
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
        tb_plan.set_font_size(18)
        return tb_plan

class ExcelWriter:
    __path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    __excel_creator_dir = 'excel_creator'
    __time_sheet_xls_dir = 'time_sheet_xls'
    __path_to_dir = os.path.join(__path, __excel_creator_dir, __time_sheet_xls_dir)

    def __init__(self, name_document: str, contractors: list):
        self.date = datetime.datetime.today().date()
        self.name = f"{name_document}_{self.date}.xlsx"
        self.gen_contractor = contractors
        self.workbook = xlsxwriter.Workbook(os.path.join(self.__path_to_dir, self.name))
        self.format = ExcelFormat(self.workbook)
        self.cur_row = 6
        self._result_row = 0
        self._summ_row_start = 0
        self._summ_row_finish = 0
        self._last_colm_workers = 0
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

    def close(self):
        self.workbook.close()

    def _write_title_work(self, count_companies: int):
        """ Заполнение оглавления табеля (Численность персонала, задействованного...) """
        len_title = 4 + count_companies * 4 + 2
        row_title = 1
        a = 'Численность персонала, задействованного на 2, 13, 15 этапах по Обустройству МФК "Лахта центр'
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
        col_comp, col_pl, col_f, col_def = 0, 4, 6, 8
        num_0 = 0
        for name in nms_comps:
            self.worksheet.merge_range(self.cur_row, col_comp, self.cur_row, col_comp + 3,
                                       name, self.format.companies_format(set_bold=False))
            self.worksheet.merge_range(self.cur_row, col_pl, self.cur_row, col_pl + 1,
                                       num_0, self.format.tb_plan_format(set_bold=False, set_border=False))
            self.worksheet.merge_range(self.cur_row, col_f, self.cur_row, col_f + 1,
                                       num_0, self.format.companies_format(set_bold=False))
            self.worksheet.merge_range(self.cur_row, col_def, self.cur_row, col_def + 1,
                                       num_0, self.format.companies_format(set_bold=False))
            self.cur_row += 1

        self.worksheet.merge_range(self.cur_row, col_comp, self.cur_row, col_comp + 3,
                                   "Итого", self.format.companies_format(set_border=True))
        self.worksheet.merge_range(self.cur_row, col_pl, self.cur_row, col_pl + 1,
                                   num_0, self.format.tb_plan_format(set_border=True))
        self.worksheet.merge_range(self.cur_row, col_f, self.cur_row, col_f + 1,
                                   num_0, self.format.companies_format(set_border=True))
        self.worksheet.merge_range(self.cur_row, col_def, self.cur_row, col_def + 1,
                                   ' ', self.format.companies_format(set_border=True))

    def write_title_tb_tm_sh(self):
        """ Оглавление таблицы Этап Здание Этаж Подрядчик"""
        row = self.cur_row + 4
        for i in range(0, 4):
            """ Растягиваю по высоте строки"""
            self.worksheet.set_row(row + i, height=25)
        self.worksheet.merge_range(row, 0, row + 2, 0, 'Этап', self.format.tb_tm_sh_title())
        self.worksheet.merge_range(row, 1, row + 2, 1, 'Здание', self.format.tb_tm_sh_title())
        self.worksheet.merge_range(row, 2, row + 2, 2, 'Этаж', self.format.tb_tm_sh_title())
        self.worksheet.set_column(3, 3, width=14)
        self.worksheet.merge_range(row, 3, row + 2, 3, 'Основной\nподрядчик', self.format.tb_tm_sh_title())

    def write_title_companies_tb(self, companies_and_work: list):
        """ Заполнение подрядчиками и наименованиями работ оглавления таблицы табеля времени"""
        self.column_companies_work = {}
        row_name_comp = self.cur_row + 3
        row_name_work = row_name_comp + 1
        row_titles_workers = row_name_work + 1
        row_plan_fact_workers = row_titles_workers + 1
        col_comp = 4
        for comp_and_work in companies_and_work:
            """Сужаю по ширине столбцы"""
            self.worksheet.set_column(col_comp, col_comp + 7, width=6)
            self.worksheet.merge_range(row_name_comp, col_comp, row_name_comp, col_comp + 7,
                                       comp_and_work[0], self.format.tb_tm_sh_title())
            self.column_companies_work[comp_and_work[0]] = {}

            name_work = comp_and_work[1] if len(comp_and_work) > 1 else 'Нет наименования работ'
            self.worksheet.merge_range(row_name_work, col_comp, row_name_work, col_comp + 7,
                                       name_work, self.format.tb_tm_sh_title())
            self.column_companies_work[comp_and_work[0]][name_work] = {}

            titles = ['Охрана', "Дежурный", "Рабочие", "ИТР ПТО"]
            # Сохраняю номер колонки для Подрядчика и наименования работ
            self.column_companies_work[comp_and_work[0]][name_work] = col_comp

            for i, title in zip(range(0, 5), titles):
                self.worksheet.merge_range(row_titles_workers, col_comp + i * 2, row_titles_workers,
                                           col_comp + i * 2 + 1,
                                           title, self.format.tb_tm_sh_title(set_bold=True))
                self.worksheet.write(row_plan_fact_workers, col_comp + i * 2,
                                     'План', self.format.tb_tm_sh_title(set_bold=False, set_border=False))
                self.worksheet.write(row_plan_fact_workers, col_comp + i * 2 + 1,
                                     'Факт', self.format.tb_tm_sh_title(set_bold=False, set_border=False))
            col_comp += 8
        self._last_colm_workers = col_comp
        self.worksheet.merge_range(row_name_work, col_comp, row_titles_workers, col_comp+1, 'ИТОГО',
                                   self.format.tb_tm_sh_title(set_bold=True))
        self.worksheet.write(row_plan_fact_workers, col_comp,
                             'План', self.format.tb_tm_sh_title(set_bold=False, set_border=False))
        self.worksheet.write(row_plan_fact_workers, col_comp + 1,
                             'Факт', self.format.tb_tm_sh_title(set_bold=False, set_border=False))

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
                self.worksheet.set_row(row, 28, self.format.tb_cell_write(grey=color, set_top_line=True))
            else:
                self.worksheet.set_row(row, 28, self.format.tb_cell_write(grey=color))
            self.worksheet.write(row, cols[0], int(line[0]))
            self.worksheet.write(row, cols[1], line[1])
            self.worksheet.write(row, cols[2], line[2])
            self.worksheet.write(row, cols[3], line[3])
            self.rows_stage_build_work[(int(line[0]), line[1], line[2], line[3])] = row
            row += 1

        self.worksheet.set_row(row, 25, self.format.tb_cell_write(grey=True, set_bold=True, set_bold_border=True))
        self.worksheet.set_row(row + 1, 25, self.format.tb_cell_write(set_bold=True, set_bold_border=True))
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
            row = self.rows_stage_build_work[(line[0], line[1], line[2], line[3])]
            columns = self.column_companies_work[line[4]][line[5]]
            numbers = line[6::]
            for nums, col in zip(numbers, range(columns, columns + 8)):
                self.worksheet.write(row, col, nums)

    def write_results_formulas_bottom(self):
        """ Формулы в строке ИТОГО внизу таблицы """
        row_formula = self._result_row + 1
        row_for_st = self._summ_row_start + 1
        row_for_fn = self._summ_row_finish + 1
        for i in range(4, self._last_colm_workers):
            lt = self.letters_excel[i]
            self.worksheet.write_formula(f'{lt}{row_formula}', f'=SUM({lt}{row_for_st}:{lt}{row_for_fn})')

    def write_results_formulas_right(self):
        """ Формулы в правом столбце ИТОГО """
        # СУММЕСЛИ SUMMIF
        row_formula = self._result_row + 1
        row_for_st = self._summ_row_start + 1
        row_for_fn = self._summ_row_finish + 1
        for i in range(4, self._last_colm_workers):
            lt = self.letters_excel[i]
            self.worksheet.write_formula(f'{lt}{row_formula}', f'=SUM({lt}{row_for_st}:{lt}{row_for_fn})')

    def create_table_header(self, cont: str):
        """ Создание заголовка таблциы, наименоване листа, даты и шапки для таблицы подрядчиков """
        self._add_worksheet(cont)
        self._write_title_work(8)
        self._write_date_work()
        self._write_title_table_companies()


from data_base.db_commands import CommandsDB

contractors = CommandsDB.get_contractors_today_from_form()
aa = ExcelWriter('First_doc', contractors)
for contractor in contractors:
    aa.create_table_header(contractor)
    comps = CommandsDB.get_names_all_users(without_admin=True)
    comps_and_work = CommandsDB.get_names_work_companies_from_form()
    # Запрос Этап, Здание, Этаж, Ген подрядчик
    lns_from_form_with_contactor = CommandsDB.get_all_str_from_form_with_cont(contractor)
    aa.write_companies_to_tb(comps)
    aa.write_title_tb_tm_sh()
    aa.write_title_companies_tb(comps_and_work)
    aa.write_builds_st_lv_tb(lns_from_form_with_contactor)
    aa.write_nums_workers(lns_from_form_with_contactor)
    aa.write_results_formulas_bottom()
aa.close()

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

    def tb_tm_sh_title(self, set_bold: bool = True):
        tb_time_sheet = self.work_book.add_format()
        tb_time_sheet.set_font("Times New Roman")
        if set_bold:
            tb_time_sheet.set_bold()
        tb_time_sheet.set_border(1)
        tb_time_sheet.set_align('vcenter')
        tb_time_sheet.set_align('center')
        tb_time_sheet.set_text_wrap()
        tb_time_sheet.set_font_size(11)
        return tb_time_sheet

    def tb_cell_write(self, set_bold: bool = False, grey: bool = False,
                      top_line: bool = False, red_font: bool = False, set_bold_border: bool = False):
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
        if top_line:
            tb_cell.set_top(5)
        if red_font:
            tb_cell.set_font_color('red')
        if set_bold_border:
            tb_cell.set_border(2)
        else:
            tb_cell.set_border(1)
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

    def __init__(self, name_document: str, contractor: str):
        self.date = datetime.datetime.today().date()
        self.name = f"{name_document}_{self.date}.xlsx"
        self.gen_contractor = contractor
        self.workbook = xlsxwriter.Workbook(os.path.join(self.__path_to_dir, self.name))
        self.format = ExcelFormat(self.workbook)
        self.cur_row = 6

    def get_path_to_file(self):
        return os.path.join(self.__path_to_dir, self.name)

    def _add_worksheet(self):
        self.worksheet = self.workbook.add_worksheet(name=self.gen_contractor)

    def close(self):
        self.workbook.close()

    def _write_title_work(self, count_companies: int):
        len_title = 4 + count_companies * 4 + 2
        row_title = 1
        a = 'Численность персонала, задействованного на 2, 13, 15 этапах по Обустройству МФК "Лахта центр'
        self.worksheet.merge_range(row_title, 0, row_title, len_title, a, self.format.title_format())

    def _write_date_work(self):
        row = 3
        date = self.date.strftime('%d.%m.%Y')
        self.worksheet.merge_range(row, 0, row, 3, date, self.format.date_format())

    def _write_title_table_companies(self):
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
                                   "Итого", self.format.companies_format())
        self.worksheet.merge_range(self.cur_row, col_pl, self.cur_row, col_pl + 1,
                                   num_0, self.format.tb_plan_format(set_border=False))
        self.worksheet.merge_range(self.cur_row, col_f, self.cur_row, col_f + 1,
                                   num_0, self.format.companies_format())
        self.worksheet.merge_range(self.cur_row, col_def, self.cur_row, col_def + 1,
                                   ' ', self.format.companies_format())

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

    def write_title_companies_tb(self, companies: list):
        """ Заполнение подрядчиками и наименованиеями работ оглавления таблицы"""
        row_name_comp = self.cur_row + 3
        row_name_work = row_name_comp + 1
        row_titles_workers = row_name_work + 1
        row_plan_fact_workers = row_titles_workers + 1
        col_comp = 4
        for comp in companies:
            """Сужаю по ширине столбцы"""
            self.worksheet.set_column(col_comp, col_comp + 7, width=5)
            self.worksheet.merge_range(row_name_comp, col_comp, row_name_comp, col_comp + 7,
                                       comp, self.format.tb_tm_sh_title())
            self.worksheet.merge_range(row_name_work, col_comp, row_name_work, col_comp + 7,
                                       'Наименование работ', self.format.tb_tm_sh_title())
            titles = ['Охрана', "Дежурный", "Рабочие", "ИТР ПТО"]
            for i, title in zip(range(0, 5), titles):
                self.worksheet.merge_range(row_titles_workers, col_comp + i*2, row_titles_workers, col_comp + i*2 + 1,
                                           title, self.format.tb_tm_sh_title(set_bold=False))
                self.worksheet.write(row_plan_fact_workers, col_comp + i*2,
                                     'План', self.format.tb_tm_sh_title(set_bold=False))
                self.worksheet.write(row_plan_fact_workers, col_comp + i*2 + 1,
                                     'Факт', self.format.tb_tm_sh_title(set_bold=False))
            col_comp += 8

    def write_builds_st_lv_tb(self, data_from_db: list):
        row = self.cur_row + 7
        grey_color = cycle([False, True])
        cols = [0, 1, 2, 3]
        data_in_table = {}
        for line in data_from_db:
            color = next(grey_color)
            if line[0] not in data_in_table:
                data_in_table[line[0]] = 0

            self.worksheet.set_row(row, 28, self.format.tb_cell_write(grey=color))
            self.worksheet.write(row, cols[0], int(line[0]), self.format.tb_cell_write(grey=color))
            self.worksheet.write(row, cols[1], line[1], self.format.tb_cell_write(grey=color))
            self.worksheet.write(row, cols[2], line[2], self.format.tb_cell_write(grey=color))
            self.worksheet.write(row, cols[3], line[3], self.format.tb_cell_write(grey=color))
            row += 1
        self.worksheet.set_row(row, 25, self.format.tb_cell_write(grey=True, set_bold=True, set_bold_border=True))
        self.worksheet.set_row(row + 1, 25, self.format.tb_cell_write(set_bold=True, set_bold_border=True))
        self.worksheet.merge_range(row, 0, row, 3,
                                   'ИТОГО', self.format.tb_cell_write(grey=True, set_bold=True, set_bold_border=True))
        self.worksheet.merge_range(row + 1, 0, row + 1, 3,
                                   'ДЕФИЦИТ', self.format.tb_cell_write(set_bold=True, red_font=True, set_bold_border=True))


    def create_xlsx(self):
        self._add_worksheet()
        self._write_title_work(8)
        self._write_date_work()
        self._write_title_table_companies()


# aa = ExcelWriter('First_doc', 'ЕСТ')
# aa.create_xlsx()
# comps = ['ЛИИС/АМР', 'ЕСТ', "Термолайн", "АПА", "ПТК Спорт", "СГК", "Результат"]
# lines = [('2', 'Б1', 'L15', 'ЕСТ'),
#          ('2', 'Б1', 'L13', 'ЕСТ'),
#          ('2', 'Б1', 'L12', 'ЕСТ'),
#          ('2', 'Б1', 'L11', 'ЕСТ'),
#          ('5', 'Б1', 'L10', 'ЕСТ'),
#          ('5', 'Б2', 'L58', 'ЕСТ'),
#          ('13', 'Офис', 'L1', 'ЕСТ'),
#          ('13', 'Стилбат', 'L6', 'ЕСТ')]
# aa.write_companies_to_tb(comps)
# aa.write_title_tb_tm_sh()
# aa.write_title_companies_tb(comps)
# aa.write_builds_st_lv_tb(lines)
# aa.close()

# name_xls = 'lala.xlsx'
# workbook = xlsxwriter.Workbook(os.path.join(__path_to_dir, name_xls))
# worksheet = workbook.add_worksheet(name='Ген_Подрядчик(Имя)')
#
# a = 'Численность персонала, задействованного на 2, 13, 15 этапах по Обустройству МФК "Лахта центр'
#
# # Форматы
# title = workbook.add_format()
# title.set_font("Times New Roman")
# title.set_font_size(26)
# title.set_bold()
# title.set_align('center')
#
# data_format = workbook.add_format()  # {'border': 5}
# data_format.set_font("Times New Roman")
# data_format.set_bold()
# data_format.set_border(1)
# data_format.set_align('centre')
# data_format.set_font_size(18)
#
# company_format = workbook.add_format()
# company_format.set_font("Times New Roman")
# company_format.set_border(1)
# company_format.set_align('centre')
# company_format.set_font_size(18)
#
# # Дата
# worksheet.merge_range('A4:D4', "24.03.2022", data_format)
# # Оглавление
# worksheet.merge_range(1, 0, 1, 45, a, title)
#
# # Шапка таблицы подрядчиков
#
# table_header_companies = ['Подрядчик', 'План', 'Факт', "Дефицит"]
#
# row = 5
# col = 0
#
# col_plan = 4
# col_def = 8
#
# worksheet.merge_range(row, col, row, col + 3, 'Подрядчик', data_format)
# worksheet.merge_range(row, col_plan, row, col_plan + 1, 'План', data_format)
# worksheet.merge_range(row, col_plan + 2, row, col_plan + 3, 'Факт', data_format)
# worksheet.merge_range(row, col_def, row, col_def + 1, 'Дефицит', data_format)
#
# companies = ['ЕСТ', 'ЛИИС/АМР', 'Термолайн', 'АПА', ]
#
# row = 6
# col = 0
# for comp in companies:
#     worksheet.merge_range(row, col, row, col + 3, comp, company_format)
#     row += 1
#
# workbook.close()

import calendar
import datetime

import openpyxl


def get_data_about_employees(fio: list):
    days_count = calendar.mdays[datetime.date.today().month]  # Получаем количество дней в месяце
    employees_data_dict = dict()
    days_of_duty_list = list()
    start_day = 1
    for item in fio:
        for day in range(start_day, days_count + 1, 3):
            days_of_duty_list.append(day)
        if '/' in item:  # Если в смену заступает 2 контролёра
            for name in item.split('/'):
                employees_data_dict[name] = days_of_duty_list
        else:
            employees_data_dict[item] = days_of_duty_list  # Создаем словарь с днями дежурств - нормализованный график
        days_of_duty_list = []
        start_day += 1

    return employees_data_dict


def get_fio_of_employees(info_str: str):  # Функция, которая возвращает список ФИО сотрудников - РАБОТА БД
    info_list = info_str.split(',')
    return info_list


def set_data_of_employees_in_report_card(fio_dct: dict):
    book = openpyxl.Workbook()
    sheet = book.active
    row_count = 1
    col_count = 2
    for day in range(1, calendar.mdays[datetime.date.today().month] + 1):
        sheet.cell(row=row_count, column=col_count).value = day
        col_count += 1
    for fio, dates in fio_dct.items():
        sheet.cell(row=row_count + 1, column=1).value = fio
        for date in dates:
            sheet.cell(row=row_count + 1, column=int(date) + 1).value = 22
        row_count += 1

    book.save('static/excel_files/table.xls')
    book.close()

import calendar
import datetime


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

    return employees_data_dict  # Преобразуем к JSON - формату для удобной передачи данных


def get_fio_of_employees(info_str: str):  # Функция, которая возвращает список ФИО сотрудников - РАБОТА БД
    info_list = info_str.split(',')
    return info_list


def set_data_of_employees_in_report_card(
        fio_dct: dict):  # Сюда положить старую функцию, которая вносит данные с пробелами
    pass

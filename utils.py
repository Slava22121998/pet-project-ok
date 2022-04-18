import calendar
import datetime
import json


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

    return json.dumps(employees_data_dict)  # Преобразуем к JSON - формату для удобной передачи данных


# print(get_data_about_employees(['Ivanov/Petrov', 'Sidorov/Glebov', 'Nepran/Kungurov']))
# print(get_data_about_employees(['Ivanov', 'Sidorov', 'Nepran']))


def set_info_about_employees(force: str, fio: list):
    employees_data = dict()
    employees_data[force] = fio
    return json.dumps(employees_data)

# print(set_info_about_employees('OP Berezovka', ['Ivanov', 'Petrov']))

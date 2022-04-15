import calendar
import datetime


def show_duty_days(fio: list):
    duty_table = dict()
    days_list_temp = list()
    start_day = 1
    days_count = calendar.mdays[datetime.date.today().month]

    for name in fio:
        for day in range(start_day, days_count + 1, 3):
            days_list_temp.append(day)
        start_day += 1
        duty_table[name] = days_list_temp
        days_list_temp = []

    return duty_table


def get_work_times(fio: list):
    full_time = list()
    night_time = list()
    result_times_dict = dict()
    for k, v in show_duty_days(fio).items():
        for day in range(v[-1]):
            if day in v:
                full_time.insert(day, 22)
                night_time.insert(day, 8)
            else:
                full_time.insert(day, '')
                night_time.insert(day, '')
            result_times_dict[k] = {'day': full_time, 'night': night_time}
        full_time = []
        night_time = []

    return result_times_dict



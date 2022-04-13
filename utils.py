import calendar
import datetime

from docx import Document
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT


def show_duty_days(fio: list):
    duty_table = dict()
    days_list_temp = list()
    start_day = 1

    days_count = calendar.mdays[datetime.date.today().month]

    for name in fio:
        days_list_temp.append(name)
        for day in range(start_day, days_count + 1, 3):
            days_list_temp.append(day)
        duty_table[start_day] = days_list_temp
        start_day += 1
        days_list_temp = []

    return duty_table


def create_words_file(lst, name_file):
    # создание пустого документа
    doc = Document()
    # данные таблицы без названий колонок
    items = show_duty_days(lst)
    # добавляем таблицу с одной строкой
    # для заполнения названий колонок
    table = doc.add_table(1, len(items[1]))
    # определяем стиль таблицы
    table.style = 'Table Grid'
    # Получаем строку с колонками из добавленной таблицы
    head_cells = table.rows[0].cells
    # добавляем названия колонок
    for i, item in enumerate(['ФИО', 'Даты дежурств']):
        p = head_cells[i].paragraphs[0]
        # название колонки
        p.add_run(item).bold = True
        # выравниваем посередине
        p.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    # добавляем данные к существующей таблице
    for row in items.values():
        # добавляем строку с ячейками к объекту таблицы
        cells = table.add_row().cells
        for i, item in enumerate(row):
            # вставляем данные в ячейки
            cells[i].text = str(item)
            # если последняя ячейка
            if i == 2:
                # изменим шрифт
                cells[i].paragraphs[0].runs[0].font.name = 'Arial'
    doc.save(f'static/word_files/{name_file}.docx')

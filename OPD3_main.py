# Улучшить программу таким образом, чтобы она записывала считанные данные в файл Excel
# Улучшить программу таким образом, чтобы она записывала считанные данные в файл Excel

import datetime  # библиотека для отслеживания даты и времени
import requests  # http библиотека для запросов.
import pickle  # для записи и чтении в файл/из файла объектов в неизменном виде
import xlsxwriter  # библиотека для того, чтобы записывать данные в файл фомрамата excel
# import re
from bs4 import BeautifulSoup


# вывод словаря столбиком
def print_dict(river_temp):
    for item in river_temp:
        print(item, ":\t", river_temp[item])


# Запись в файл.
def write(data_struction, file_name):
    with open(file_name, 'wb') as f_write:
        pickle.dump(data_struction, f_write)
    f_write.close()


# Чтение из файла.
def read(file_name):
    with open(file_name, 'rb') as f_read:
        data_struction = pickle.load(f_read)
    f_read.close()
    return data_struction


# ф-ция, возвразающая словарь, в котором ключ 'река river_name' и значение 'temperature'
def rivers_temp_funct():
    url = 'https://pogoda1.ru/katalog/sverdlovsk-oblast/temperatura-vody/'
    r = requests.get(url)

    # открытие страницы, которая сохранена в файле
    with open('test.html', 'w') as output_file:
        output_file.write(r.text)

    # используем конструктор BeautifulSoup(), чтобы поместить текст ответа в переменную
    soup = BeautifulSoup(r.text, features="html.parser")

    # заголовок
    # header = soup.find('div', class_ = 'panel-heading' ).text
    # print (header + "\n")

    # словарь с информацией о водоемах
    rivers_temp_dict = {}

    # поиск строчек в файле навзания рек и их температура,  с последующей записью в файл
    river_data = soup.find_all('div', class_="x-row")
    for item in river_data:
        rivers_temp_dict[item.find('a').text] = float(item.find('div', class_="x-cell x-cell-water-temp").text.strip())

    return rivers_temp_dict


print_dict(rivers_temp_funct())

# открываем новый файл на запись
workbook = xlsxwriter.Workbook('rivers_data.xlsx')

# создаем там "лист"
worksheet = workbook.add_worksheet()

# устанавливаем и записываем дату
worksheet.write(0, 0, 'Дата:')
worksheet.write(0, 1, str(datetime.date.today()))

# название колонок
worksheet.write(2, 0, 'Название')
worksheet.write(2, 1, 'Температура')

# словарь с навзаниями рек и их температурами
rivers_data = rivers_temp_funct()

# нужные переменные
row = 3
col = 0

# цикл который добавляет назавние реки и её температуру
for item in rivers_data:
    worksheet.write(row, col, item)
    worksheet.write(row, col + 1, rivers_data[item])
    row += 1

# сохраняем и закрываем
workbook.close()

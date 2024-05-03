import os
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

# Автономно открывает браузер и считывает данные со страницы
with webdriver.Chrome(service=Service(ChromeDriverManager().install())) as driver:
    # Ссылка на любую из таблиц. ВАЖНО: русские буквы не поддерживаются, вставлять на криптидском
    driver.get("https://vk.com/pages?oid=-198054285&p=")
    time.sleep(5)
    soup = BeautifulSoup(driver.page_source, 'html.parser')

table1 = soup.find("table")

# Сборник названий всех столбцов
headers = []
for i in table1.find("tr"):
    title = i.text
    headers.append(title)

# Создание фрейма данных и его заполнение
frame = pd.DataFrame(columns=headers)

for j in table1.find_all("tr")[1:]:
    row_data = j.find_all("td")
    row = [i.text for i in row_data]
    length = len(frame)
    frame.loc[length] = row

# Вырезка лишних столбцов
frame.drop(columns='Способность ', inplace=True)
frame.drop(columns='Комментарии ', inplace=True)
frame.reset_index(inplace=True, drop=True)

# При необходимости увидеть датафрейм:
# print(frame)

# Счетчик:

made, reserve, free = 0, 0, 0

# Кто забронировал - индекс 1; Имя персонажа - индекс 0
for i in range(frame.shape[0]):
    var = frame.iat[i, 1]
    if var.find('(+)') != -1:
        made += 1
    elif var.find('Никто') != -1:
        free += 1
    else:
        reserve += 1

# Заголовок таблицы
head = soup.find('div', {'class': 'wk_header'})

print("{}\nЗакончено {} \t Забронировано {} \t Свободно {}".format(head.text, made, reserve, free))

import re
import os
import csv

import environ
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait


BASE_DIR = Path(__file__).resolve().parent
env = environ.Env(
    DEBUG=(bool, False)
)
environ.Env.read_env(BASE_DIR / '.env')


driver = webdriver.Firefox()
driver.get(env("BASE_URL"))

wait = WebDriverWait(driver, 5)


def concatenation_numbers(numbers_str):
    result = []  # Список для хранения объединенных чисел
    current_number = ''  # Строка для построения текущего числа

    for item in numbers_str:

        if item == ' ' and current_number:  # Если элемент - пробел и текущее число не пустое
            result.append(int(current_number))  # Преобразуем текущую строку в число и добавляем в результат
            current_number = ''  # Сбрасываем текущее число


        elif isinstance(int(item), int):  # Если элемент - это число
            current_number += str(item)  # Добавляем число к текущему числу

    # Добавляем последнее число, если оно есть
    if current_number:
        result.append(int(current_number))

    return result[-1]


def extract_product_info(text: str) -> dict:
    lines = text.splitlines()  # Разбиваем текст на строки

    # Поиск строки с названием товара
    product_name = None
    for i, line in enumerate(lines):
        if line.startswith("Бренд:"):
            product_name = lines[i + 1].strip()
            break

    # Извлечение кода товара
    code_match = re.search(r'Код товара: (\S+)', text)
    product_code = code_match.group(1) if code_match else None

    # Поиск обычной и акционной цены
    regular_price_match = re.search(r'Цена:(\s+)?(\d[\d\s]*)₽', text)
    promo_price_match = re.search(r'Цена по акции:\s*(\d[\d\s,]*)₽', text)

    # Преобразуем цены, убирая пробелы между цифрами
    regular_price = regular_price_match.group(2).replace(" ", "") if regular_price_match else None
    promo_price = promo_price_match.group(1).replace(" ", "") if promo_price_match else None

    # Формируем результат
    result = {
        'product_name': product_name,
        'product_code': product_code,
        'price': regular_price,
        'promo_price': promo_price if promo_price else None  # Присваиваем None, если акционная цена отсутствует
    }

    return result


def create_directories(category, subcategory, sub_sub_category):
    path = os.path.join(category, subcategory, sub_sub_category)
    os.makedirs(path, exist_ok=True)
    return path


def save_to_csv(path, data: dict, sub_sub_category):
    csv_file = os.path.join(path, f'{sub_sub_category}.csv')
    file_exists = os.path.isfile(csv_file)

    # Проверяем, существует ли файл. Если нет, создаем его с заголовком.
    fieldnames = [key for key in data.keys()]
    mode = 'a' if file_exists else 'w'

    with open(csv_file, mode, newline='', encoding='utf-8-sig') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        if not file_exists:
            writer.writeheader()

        writer.writerow(data)

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

from utils import (concatenation_numbers, extract_product_info,
                   create_directories, save_to_csv, wait, driver)





def found_links_categories() -> dict:
    """
    Находит ссылки на категории на главной странице каталога.

    Returns:
        dict: Словарь с названиями категорий в качестве ключей и их URL в качестве значений.
    """
    links = {}

    try:
        all_categories = wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".section_info .name"))
        )

        for category in all_categories:
            try:
                name = category.text.strip().replace(' ', '_')
                href = category.find_element(By.CSS_SELECTOR, "a.dark_link").get_attribute("href")
                links[name] = href
            except NoSuchElementException:
                print(f"Не удалось найти ссылку для категории: {category.text}")

        print(f"Найдено {len(links)} категорий")

    except TimeoutException:
        print("Тайм-аут при ожидании элементов категорий")
    except Exception as e:
        print(f"Неожиданная ошибка при поиске категорий: {e}")

    return links


def found_links_subcategories(link: str) -> dict:
    """
    Находит ссылки на категории на главной странице каталога.

    Returns:
        dict: Словарь с названиями категорий в качестве ключей и их URL в качестве значений.
    """
    links = {}

    driver.get(link)
    try:
        all_subcategories = wait.until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "col-md-2"))
        )
        for subcategory in all_subcategories:
            try:
                name = subcategory.text.strip().replace(' ', '_')
                href = (subcategory.find_element(By.CLASS_NAME, "dark_link")).get_attribute("href")
                links[name] = href
            except NoSuchElementException:
                print(f"Не удалось найти ссылку для категории: {subcategory.text}")

        print(f"Найдено {len(links)} элементов категорий")
    except (TimeoutException, Exception) as e:
        if isinstance(e, TimeoutException):
            print("Тайм-аут при ожидании элементов подкатегории")
        else:
            print(f"Неожиданная ошибка при поиске элементов подкатегории: {e}")
    return links


def find_categories_links_in_subcategory(link: str) -> dict:
    """
        Функция для поиска ссылок в подкатегориях.

        :param link: URL подкатегории
        :return: Словарь с названиями подкатегорий в качестве ключей и ссылками в качестве значений
        """
    links = {}

    driver.get(link)
    try:
        subcategories = wait.until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "col-md-2"))
        )
        for subcategory in subcategories:
            thumb_element = subcategory.find_element(By.CLASS_NAME, "thumb")
            href = thumb_element.get_attribute("href")

            # Заменяем пробелы в названии подкатегории на подчеркивания
            subcategory_name = subcategory.text.replace(' ', '_')
            links[subcategory_name] = href
    except TimeoutException as e:
        print(f"Неожиданная ошибка при поиске элементов подкатегории подкатегорий: {e}")
    except Exception as e:
        print(f"Неожиданная ошибка при поиске элементов подкатегории подкатегорий: {e}")
    return links


def found_all_goods(link: str):
    """
    Функция для поиска всех товаров на страницах категории.

    :param link: URL категории товаров
    :return: Список ссылок на товары
    """

    links = []
    driver.get(link)

    while True:
        try:
            all_goods = wait.until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "bth-card-element"))
            )

            for product in all_goods:
                href = (product.find_element(By.CLASS_NAME, "bth-card-img-link")).get_attribute("href")

                links.append(href)

            try:
                # Находим текущую активную страницу
                current_page = driver.find_element(By.CLASS_NAME, "nums")
                max_page_number = concatenation_numbers(current_page.text)

                for page in range(2, max_page_number + 1):
                    driver.get(f"{link}?PAGEN_1={page}")
                    all_goods = wait.until(
                        EC.presence_of_all_elements_located((By.CLASS_NAME, "bth-card-element"))
                    )

                    for product in all_goods:
                        href = (product.find_element(By.CLASS_NAME, "bth-card-img-link")).get_attribute("href")

                        links.append(href)

                break

            except (Exception, NoSuchElementException) as e:
                if isinstance(e, NoSuchElementException):
                    print("Кнопка следующей страницы не найдена")
                    break
                else:
                    print(f"Произошла ошибка: {str(e)}")
        except (TimeoutException, Exception) as e:
            if isinstance(e, TimeoutException):
                print("Ошибка: Таймаут при ожидании загрузки товаров")
                break
            else:
                print(f"Неожиданная ошибка при сборе ссылок на товаровы: {str(e)}")
    print(f"Найдено товаров {len(link)}")
    return links


def get_info_products(category: str, subcategory: str, sub_sub_category: str, link):
    """
    Получает информацию о продуктах с указанной страницы, сохраняет её в CSV файл.

    :param category: Название категории.
    :param subcategory: Название подкатегории.
    :param sub_subcategory: Название под-подкатегории.
    :param link: URL страницы с продуктами.
    """

    driver.get(link)

    try:
        all_information = wait.until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "card_detail__info-container"))
        )

        for info in all_information:
            title_product = info.find_element(By.CLASS_NAME, "card_detail__title").text.strip()

            try:
                regular_price = info.find_element(By.CLASS_NAME, "old-price").text.strip()
                sale_price = info.find_element(By.CLASS_NAME, "sale-price ").text.strip()
            except NoSuchElementException:
                # Если не нашли элементы акционной цены, ищем обычную цену
                regular_price = info.find_element(By.CLASS_NAME, "retail-price").text.strip()
                sale_price = "Нет акции"

            data = extract_product_info(title_product + '\n' + regular_price + '\n' + sale_price)

            directories = create_directories(category, subcategory, sub_sub_category)
            save_to_csv(directories, data, sub_sub_category)


    except Exception as e:
        print(f"Произошла ошибка при получении информации о продуктах: {e}")

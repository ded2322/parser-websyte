from utils import driver
from service import (found_links_categories, found_links_subcategories,
                     find_categories_links_in_subcategory, found_all_goods, get_info_products)


def parse_category(name_category: str, link_category: str) -> None:
    """
    Парсит все подкатегории и товары в данной категории.

    :param name_category: Название категории.
    :param link_category: Ссылка на категорию.
    """
    print(f"Парсит категорию: {name_category}")
    all_subcategories = found_links_subcategories(link_category)

    for name_subcategory, link_subcategory in all_subcategories.items():
        parse_subcategory(name_category, name_subcategory, link_subcategory)


def parse_subcategory(name_category: str, name_subcategory: str, link_subcategory: str) -> None:
    """
    Парсит все под-подкатегории и товары в данной подкатегории.

    :param name_category: Название категории.
    :param name_subcategory: Название подкатегории.
    :param link_subcategory: Ссылка на подкатегорию.
    """
    print(f"Парсит подкатегорию: {name_subcategory}")
    sub_subcategories = find_categories_links_in_subcategory(link_subcategory)

    for name_sub_subcategory, link_sub_subcategory in sub_subcategories.items():
        parse_sub_subcategory(name_category, name_subcategory, name_sub_subcategory, link_sub_subcategory)


def parse_sub_subcategory(name_category: str, name_subcategory: str, name_sub_subcategory: str,
                          link_sub_subcategory: str) -> None:
    """
    Парсит все товары в данной под-подкатегории.

    :param name_category: Название категории.
    :param name_subcategory: Название подкатегории.
    :param name_sub_subcategory: Название под-подкатегории.
    :param link_sub_subcategory: Ссылка на под-подкатегорию.
    """
    print(f"Парсит под-подкатегорию: {name_sub_subcategory}")
    links_goods = found_all_goods(link_sub_subcategory)

    for link_product in links_goods:
        get_info_products(name_category, name_subcategory, name_sub_subcategory, link_product)


if __name__ == "__main__":

    categories_links = found_links_categories()

    for name_category, link_category in categories_links.items():
        parse_category(name_category, link_category)

    driver.close()

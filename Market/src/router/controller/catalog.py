from aiogram.types import CallbackQuery
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from src.base.database import DATABASE
# from src.router.view.catalog import build_keyboard, product_nav_keyboard, product_caption


# Получение списка уникальных категорий каталога
async def get_categories():
    catalog_info = await DATABASE.get_catalog()
    catalogs = []
    for row in catalog_info:
        if row[6] not in catalogs:
            catalogs.append(row[6])
    return catalogs


# Получение подкатегорий для выбранной категории
async def get_subcategories(category):
    catalog_info = await DATABASE.get_catalog()
    subcategories = []
    for row in catalog_info:
        if row[6] == category and row[7] not in subcategories:
            subcategories.append(row[7])
    return subcategories


# Получение товаров по подкатегории
async def get_products_by_subcategory(subcategory):
    catalog_info = await DATABASE.get_catalog()
    return [row for row in catalog_info if row[8] == subcategory]


async def get_add_product_message(product_info, amount, basket_info, user_id):
    res = []
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Каталог", callback_data="catalog")],
    ])
    res.append(kb)

    try:
        amount = int(amount)
    except ValueError:
        reply_text = "Введите корректное количество, например 2."
        success = False
        res.append(reply_text)
        res.append(success)
        return res
    
    product_id = product_info[0]['id']
    in_basket = None
    for item in basket_info:
        if str(item['product']) == str(product_id):
            in_basket = item
            break

    if in_basket:
        await DATABASE.update_product(int(user_id), int(product_id), int(amount))
        text = f"Добавлено {amount} *{product_info[0]['name']}* в корзину!✅ (обновлено количество)"
    else:
        await DATABASE.add_product(int(user_id), int(product_id), int(amount))
        text = f"Добавлено {amount} *{product_info[0]['name']}* в корзину!✅"

    res.append(text)
    res.append(True)
    return res

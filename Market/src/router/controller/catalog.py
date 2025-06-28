from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from src.base.database import DATABASE


# Getting a list of unique catalog categories
async def get_categories():
    catalog_info = await DATABASE.get_table("catalog")
    catalogs = []
    for row in catalog_info:
        if row[6] not in catalogs:
            catalogs.append(row[6])
    return catalogs


# Getting subcategories for the selected category
async def get_subcategories(category):
    catalog_info = await DATABASE.get_table("catalog")
    subcategories = []
    for row in catalog_info:
        if row[6] == category and row[7] not in subcategories:
            subcategories.append(row[7])
    return subcategories


# Receiving products by subcategory
async def get_products_by_subcategory(subcategory):
    catalog_info = await DATABASE.get_table("catalog")
    return [row for row in catalog_info if len(row) > 7 and row[7] == subcategory]


async def get_add_product_message(product_info, amount, basket_info, user_id):
    kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Каталог", callback_data="catalog")]])
    try:
        amount = int(amount)
    except ValueError:
        return {
            "success": False,
            "message": "Введите корректное количество, например 2.",
            "markup": kb
        }

    product_id = product_info[0]['id']
    in_basket = next((item for item in basket_info if str(item['product']) == str(product_id)), None)
    
    if amount <= 0:
        return {
            "success": False,
            "message": "Введите положительное количество!",
            "markup": kb
        }
    
    if not product_info:
        return {
            "success": False,
            "message": "Продукт не найден!",
            "markup": kb
        }
    
    if amount > 100000:
        return {
            "success": False,
            "message": "Введите количевство не более 100 000!",
            "markup": kb
        }
    
    if in_basket:
        if basket_info[0]['pay'] == 1:
            await DATABASE.add_product(int(user_id), int(product_id), int(amount))
        await DATABASE.update_product(int(user_id), int(product_id), int(amount))
    else:
        await DATABASE.add_product(int(user_id), int(product_id), int(amount))

    return {
        "success": True,
        "message": f"Добавлено {amount} *{product_info[0]['name']}* в корзину!✅",
        "markup": kb
    }

async def state_get_amount(data, message):
    product_id = data["product_id"]
    product_info = await DATABASE.get_cb_for_id(int(product_id), "catalog")
    basket_info = await DATABASE.get_cb_for_id(message.from_user.id, "basket")
    amount = message.text
    return await get_add_product_message(product_info, amount, basket_info, message.from_user.id)

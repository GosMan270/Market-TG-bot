from aiogram import Router, F
from aiogram.types import CallbackQuery, Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters.command import Command

import src.router.controller.catalog as controller
from src.router.view.catalog import build_category_keyboard, build_subcategory_keyboard, product_nav_keyboard, \
	product_caption
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from src.base.database import DATABASE


async def basket_menu(user_id, kb=None):
	res = []
	basket_info = await DATABASE.get_cb_for_id(user_id, "basket")
	text = f"*Корзина*\n\n"
	summa = 0
	for i, item in enumerate(basket_info):
		product_id = item['product']
		quantity = item['quantity']
		product_info = await DATABASE.get_cb_for_id(product_id, "catalog")
		if product_info:
			prod = product_info[0]
			name = prod['name']
			price = prod['price']
			text += f"{i + 1}. {name} - {quantity} шт. - {int(price) * int(quantity)} руб.\n\n"
			summa += int(price) * int(quantity)
		else:
			text += f"{i + 1}. Товар не найден (id {product_id})\n"
	text += f"\n*Итого: {summa} руб.*"
	
	kb = InlineKeyboardMarkup(inline_keyboard=[
		[
			(InlineKeyboardButton(text="Удалить", callback_data="delite")),
			(InlineKeyboardButton(text="Оплатить", callback_data="buy"))
		],
		[
			
			(InlineKeyboardButton(text="Меню", callback_data="menu"))
		]
	])
	
	res.append(text)
	res.append(kb)
	return res


async def get_add_product_message(product_info, amount: int):
	res = []
	kb = InlineKeyboardMarkup(inline_keyboard=[
		[
			(InlineKeyboardButton(text="Каталог", callback_data=f"catalog")),
		],
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
	
	text = (f"Добавлено {amount} *{product_info[0]['name']}* в корзину!✅")
	res.append(text)
	res.append(True)
	return res



async def delite_product_message(user_id, amount):
    res = []
    kb = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="Каталог", callback_data="catalog")]]
    )
    res.append(kb)

    try:
        number = int(amount)
    except ValueError:
        reply_text = "Введите корректный номер булочки, например 2."
        success = False
        res.append(reply_text)
        res.append(success)
        return res

    basket_info = await DATABASE.get_cb_for_id(user_id, "basket")

    if 1 <= number <= len(basket_info):
        product_row = basket_info[number - 1]
        product_id = product_row["product"]
        await DATABASE.delite_product(user_id, product_id)
        reply_text = f"Булочка под номером {number} удалена ✅"
        success = True
    else:
        reply_text = "Булочки с таким номером нет в корзине!"
        success = False

    res.append(reply_text)
    res.append(success)
    return res
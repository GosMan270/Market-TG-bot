from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from src.router.view.catalog import build_category_keyboard, build_subcategory_keyboard, product_nav_keyboard, \
	product_caption
from src.base.database import DATABASE


async def basket_menu(user_id, kb = None, add = None):
	res = []
	basket_info = await DATABASE.get_cb_for_id(user_id, "basket")
	
	text = f"*Корзина*\n\n"
	summa = 0
	any_not_paid = False
	
	if not basket_info:
		text += "Ваша корзина пуста."
	else:
		for i, item in enumerate(basket_info):
			product_id = item['product']
			quantity = item['quantity']
			product_info = await DATABASE.get_cb_for_id(product_id, "catalog")
			if int(item['pay']) != 1:
				any_not_paid = True
				if product_info:
					prod = product_info[0]
					name = prod['name']
					price = prod['price']
					text += f"{i + 1}. {name} - {quantity} шт. - {int(price) * int(quantity)} руб.\n\n"
					summa += int(price) * int(quantity)
				else:
					text += f"{i + 1}. Товар не найден (id {product_id})\n\n"
			else:
				text += "*Уже оплачено!*\n"
				if product_info:
					prod = product_info[0]
					name = prod['name']
					price = prod['price']
					text += f"{i + 1}. {name} - {quantity} шт. - {int(price) * int(quantity)} руб.\n\n"
				else:
					text += f"{i + 1}. Товар не найден (id {product_id})\n"
	
	text += f"\n*Итого: {summa} руб.*"
	
	keyboard = []
	# Show "Delete" and "Pay" buttons only if there are unpaid items
	if any_not_paid:
		keyboard.append([
			InlineKeyboardButton(text="Удалить", callback_data="delite"),
			InlineKeyboardButton(text="Оплатить", callback_data="buy")
		])
	keyboard.append([
		InlineKeyboardButton(text="Меню", callback_data="menu")
	])
	kb = InlineKeyboardMarkup(inline_keyboard=keyboard)
	
	res.append(text)
	res.append(kb)
	res.append(summa)
	return res


async def delite_product_message(message):
	res = []
	res.append(InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Меню", callback_data="menu")]]))
	
	user_id = message.from_user.id
	amount = message.text
	
	try:
		number = int(amount)
	except ValueError:
		res.append("Введите корректный номер булочки, например 2.")
		res.append(False)
		return res
	
	# "basket_info" Getting the user's shopping cart
	basket_info = await DATABASE.get_cb_for_id(user_id, "basket")
	if 1 <= number <= len(basket_info):
		# Getting the product from the database. "-1 since it starts from 0"
		product_row = basket_info[number - 1]
		product_id = product_row["product"]
		await DATABASE.delite_product(user_id, product_id)
		res.append(f"Булочка под номером {number} удалена ✅")
		res.append(True)
	else:
		res.append("Булочки с таким номером нет в корзине!")
		res.append(False)
	return res
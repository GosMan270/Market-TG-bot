from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message



menu = InlineKeyboardMarkup(inline_keyboard=[
	[
		InlineKeyboardButton(text='Корзина 🛒', callback_data="cart"),
		InlineKeyboardButton(text='Каталог 🍞', callback_data="catalog")
	]
])
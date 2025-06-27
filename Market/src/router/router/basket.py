from aiogram import Router, F
from aiogram.types import CallbackQuery, Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

import src.router.controller.basket as controller

from src.router.view.catalog import build_category_keyboard, build_subcategory_keyboard, product_nav_keyboard, product_caption
from src.base.database import DATABASE

router = Router()


class States(StatesGroup):
	delite = State()


@router.message(Command('basket'))
async def open_basket_callback(message: Message):
	res = await controller.basket_menu(message.from_user.id, True)
	await message.answer(res[0], reply_markup=res[1], parse_mode="Markdown")


@router.callback_query(F.data == "basket")
async def open_basket_callback(callback: CallbackQuery):
	res = await controller.basket_menu(callback.from_user.id, True)
	await callback.message.edit_text(res[0], reply_markup=res[1], parse_mode="Markdown")


@router.callback_query(F.data == "delite")
async def open_delite_basket_callback(callback: CallbackQuery, state: FSMContext):
	menu = InlineKeyboardMarkup(inline_keyboard=[
		[
			(InlineKeyboardButton(text="Меню", callback_data="menu")),
		]
	])
	res = await controller.basket_menu(callback.from_user.id, True)
	await callback.message.delete()
	await callback.message.answer(f"{res[0]}\n\n*Введите номер выпечки которую хотите удалить:*", reply_markup=menu, parse_mode="Markdown")
	await state.set_state(States.delite)


@router.message(States.delite)
async def get_amount(message: Message, state: FSMContext):
	res = await controller.delite_product_message(message)
	if res:
		await message.answer(res[1], reply_markup=res[0], parse_mode="Markdown")
		await state.clear()




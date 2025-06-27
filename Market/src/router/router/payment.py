from aiogram import Router, F
from aiogram.types import CallbackQuery, Message, InlineKeyboardMarkup, InlineKeyboardButton
import re

import src.router.controller.payment as controller
import src.router.controller.basket as controller_basket

from src.router.view.catalog import build_category_keyboard, build_subcategory_keyboard, product_nav_keyboard, product_caption
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from src.base.database import DATABASE

router = Router()


class OrderStates(StatesGroup):
	wait_for_address = State()
	wait_for_phone = State()
	wait_for_name = State()
	wait_for_surname = State()
	wait_for_email = State()


def is_address_valid(address: str) -> bool:
	return bool(re.fullmatch(r"[A-Za-zА-Яа-я0-9 ,.\-]+", address.strip()))


def is_phone_valid(phone: str) -> bool:
	return bool(re.fullmatch(r"(\+7|8)[0-9]{10}", phone.strip()))


def is_name_valid(name: str) -> bool:
	return bool(re.fullmatch(r"[A-Za-zА-Яа-я\- ]+", name.strip()))


def is_surname_valid(surname: str) -> bool:
	return bool(re.fullmatch(r"[A-Za-zА-Яа-я\-]+", surname.strip()))


def is_email_valid(email: str) -> bool:
	return bool(re.fullmatch(r"[A-Za-z0-9_.+-]+@[A-Za-z0-9-]+\.[A-Za-z]+", email.strip()))


@router.callback_query(F.data == "buy")
async def start(callback: CallbackQuery, state: FSMContext):
	res = await controller.add_excel(callback.from_user.id, True)
	edit = InlineKeyboardMarkup(inline_keyboard=[
		[
			(InlineKeyboardButton(text="Да", callback_data="yes")),
			(InlineKeyboardButton(text="Нет", callback_data="no"))
		],
	])
	
	if res:
		await callback.message.answer(f"Найдены данные!\n\n*{res}*\n\nХотите изменить?", reply_markup=edit, parse_mode="Markdown")
		return
	await callback.message.answer("Введите адрес:")
	await state.set_state(OrderStates.wait_for_address)


@router.callback_query(F.data == "yes")
async def address_prompt(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Введите адрес:")
    await state.set_state(OrderStates.wait_for_address)


@router.message(OrderStates.wait_for_address)
async def address_handler(message: Message, state: FSMContext):
    if not is_address_valid(message.text):
        await message.answer(
            "Адрес содержит недопустимые символы! (разрешены буквы, цифры, пробел, , . -)\nВведите адрес еще раз:")
        return
    await state.update_data(address=message.text.strip())
    await message.answer("Введите телефон (например, +79991234567 или 89991234567):")
    await state.set_state(OrderStates.wait_for_phone)


@router.message(OrderStates.wait_for_phone)
async def phone_handler(message: Message, state: FSMContext):
	if not is_phone_valid(message.text):
		await message.answer("Введите корректный телефон (пример: +79991234567 или 89991234567):")
		return
	await state.update_data(phone=message.text.strip())
	await message.answer("Введите ваше имя:")
	await state.set_state(OrderStates.wait_for_name)


@router.message(OrderStates.wait_for_name)
async def name_handler(message: Message, state: FSMContext):
	if not is_name_valid(message.text):
		await message.answer("Имя должно содержать только буквы, пробел и дефис!\nВведите имя еще раз:")
		return
	await state.update_data(name=message.text.strip())
	await message.answer("Введите вашу фамилию (только буквы и дефис):")
	await state.set_state(OrderStates.wait_for_surname)


@router.message(OrderStates.wait_for_surname)
async def surname_handler(message: Message, state: FSMContext):
	if not is_surname_valid(message.text):
		await message.answer("Фамилия должна содержать только буквы и дефис!\nВведите фамилию еще раз:")
		return
	await state.update_data(surname=message.text.strip())
	await message.answer("Введите e-mail:")
	await state.set_state(OrderStates.wait_for_email)


@router.message(OrderStates.wait_for_email)
async def email_handler(message: Message, state: FSMContext):
	if not is_email_valid(message.text):
		await message.answer("Введите корректный e-mail!")
		return
	
	await state.update_data(email=message.text.strip())
	data = await state.get_data()
	print('FSM data:', data)
	
	res = await controller_basket.basket_menu(message.from_user.id)
	menu = InlineKeyboardMarkup(
		inline_keyboard=[
			[InlineKeyboardButton(text="Меню", callback_data="menu")]
		]
	)
	
	user = await DATABASE.get_cb_for_id(message.from_user.id, "users")
	if user:
		await DATABASE.update_user_info(
			data['address'], data['phone'], data['name'], data['surname'], data['email'], message.from_user.id)
	else:
		await DATABASE.new_user(
			message.from_user.id, data['address'], data['phone'], data['name'], data['surname'], data['email'])
	
	pay_url, label = controller.create_quickpay_link(res[2], message.from_user.id)
	
	if float(label.split('_')[2]) == 0:
		await message.answer("Ваша корзина *пуста!*", reply_markup=menu, parse_mode="Markdown")
		await state.clear()
		return
	
	await give_lable_message(message, res, pay_url, label)
	await state.clear()
	
	
@router.callback_query(F.data == "no")
async def give_lable(callback: CallbackQuery):
    res = await controller_basket.basket_menu(callback.from_user.id)
    pay_url, label = controller.create_quickpay_link(res[2], callback.from_user.id)
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=f"✨ Оплатить {res[2]}₽", url=pay_url)],
            [InlineKeyboardButton(text="✅ Я оплатил", callback_data=f"sub_check_{label}")],
            [InlineKeyboardButton(text="Меню", callback_data="menu")]
        ]
    )
    await callback.message.edit_text(
        "Нажимая на кнопку *Оплатить*, вы получите *ссылку* на оплату.\nЗатем нажмите *Я оплатил*\n"
        f"*{res[2]}₽* будет списано.",
        reply_markup=markup,
        parse_mode="Markdown"
    )
	
async def give_lable_message(message, res, pay_url, label):
	markup = InlineKeyboardMarkup(
		inline_keyboard=[
			[InlineKeyboardButton(text=f"✨ Оплатить {res[2]}₽", url=pay_url)],
			[InlineKeyboardButton(text="✅ Я оплатил", callback_data=f"sub_check_{label}")],
			[InlineKeyboardButton(text="Меню", callback_data="menu")]
		]
	)
	await message.answer(
		"Нажимая на кнопку *Оплатить*, вы получите *ссылку* на оплату.\nЗатем нажмите *Я оплатил*\n"
		f"*{res[2]}₽* будет списано.",
		reply_markup=markup,
		parse_mode="Markdown"
	)
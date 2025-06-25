from aiogram import Router, F
from aiogram.types import CallbackQuery, Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters.command import Command

import src.router.controller.payment as controller
import src.router.controller.basket as controller_basket

from src.router.view.catalog import build_category_keyboard, build_subcategory_keyboard, product_nav_keyboard, product_caption
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from src.base.database import DATABASE


class OrderStates(StatesGroup):
    wait_for_address = State()
    wait_for_phone = State()
	


router = Router()


@router.callback_query(F.data == "buy")
async def cmd_system(callback: CallbackQuery, state: FSMContext):
    res = await controller_basket.basket_menu(callback.from_user.id)
    
    pay_url, label = controller.create_quickpay_link(res[2], callback.from_user.id)
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=f"✨ Оплатить {res[2]}₽", url=pay_url)],
            [InlineKeyboardButton(text="✅ Я оплатил", callback_data=f"sub_check_{label}")],
            [InlineKeyboardButton(text="Меню", callback_data=f"menu")]
        ]
    )
    await callback.message.edit_text(
        "Нажимая на кнопку *Оплатить*, вы получите *ссылку* на оплату.\nЗатем нажмите *Я оплатил*\n"
        f"*{res[2]}₽* будет списано.",
        reply_markup=markup,
        parse_mode="Markdown"
    )
    
    
    
@router.callback_query(F.data.startswith("sub_check_"))
async def check_payment_handler(callback: CallbackQuery):
    label = callback.data[len("sub_check_"):]
    user_id = callback.from_user.id

    await callback.answer("⏳ Проверяем статус вашего платежа...")

    if await controller.check_yoomoney_payment(label):
        try:
            sum_from_label = float(label.split("_")[2])
        except Exception:
            sum_from_label = 0
        await DATABASE.update_user_info(user_id)
        await callback.message.answer(
            "✅ <b>Оплата успешна!</b>\n\n"
            "Ваша корзина успешно оплачена. Спасибо!",
            parse_mode="HTML"
        )
        await DATABASE.update_user_info(user_id)
    else:
        await callback.message.answer(
            "⚠️ <b>Платеж не найден или еще не обработан</b>\n\n"
            "Пожалуйста, убедитесь, что вы завершили оплату в YooMoney.\n"
            "Платеж может занять несколько минут.\n"
            "Попробуйте еще раз.\n"
            "Если проблема сохраняется, обратитесь в поддержку.",
            parse_mode="HTML"
        )

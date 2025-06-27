from aiogram import Router, F
from aiogram.types import CallbackQuery, Message, InlineKeyboardMarkup, InlineKeyboardButton, InlineQuery, InlineQueryResultArticle, InputTextMessageContent
from aiogram.filters.command import Command

from aiogram.fsm.state import State, StatesGroup

from src.base.database import DATABASE
import src.router.controller.faq as controller


router = Router()


@router.message(Command('help'))
async def welcome(message: Message):
    answer = (
        "<b>FAQ</b>\n"
        "Вы можете задать свой вопрос используя формат\n"
        "<code>@bulki_market_bot</code> ..."
        "Вместо <code>...</code> введите ваш вопрос!")
    await message.answer(answer, parse_mode = 'HTML')


@router.callback_query(lambda c: c.data == 'faq')
async def faq_callback(callback: CallbackQuery):
	answer = (
		"<b>FAQ</b>\n"
		"Ответы на часто задаваемые вопросы в формате инлайн режима с "
		"автоматическим дополнением вопроса.\n"
		"Попробуйте вызвать бота через <code>@bulki_market_bot</code> в любом чате!"
	)
	await callback.message.answer(answer, parse_mode="HTML")


@router.inline_query()
async def inline_faq(query: InlineQuery):
    user_query = query.query.lower()
    faqs = await controller.get_faq()
    results = []
    for idx, faq in enumerate(faqs):
        if user_query in faq["q"].lower():
            results.append(
                InlineQueryResultArticle(
                    id=str(idx),
                    title=faq["q"],
                    description=faq["a"],
                    input_message_content=InputTextMessageContent(
                        message_text=f"<b>{faq['q']}</b>\n{faq['a']}",
                        parse_mode="HTML"
                    )
                )
            )
    if not results:
        if not user_query.strip():
            for idx, faq in enumerate(faqs):
                results.append(
                    InlineQueryResultArticle(
                        id=str(idx),
                        title=faq["q"],
                        description=faq["a"],
                        input_message_content=InputTextMessageContent(
                            message_text=f"<b>{faq['q']}</b>\n{faq['a']}",
                            parse_mode="HTML"
                        )
                    )
                )
        else:
            results.append(
                InlineQueryResultArticle(
                    id='not_found',
                    title="Нет ответа",
                    description="Попробуйте изменить запрос.",
                    input_message_content=InputTextMessageContent(
                        message_text="К сожалению, FAQ по вашему запросу не найден."
                    )
                )
            )
    await query.answer(results, cache_time=1)
from aiogram import Router, F
from aiogram.types import CallbackQuery, Message, InlineKeyboardMarkup, InlineKeyboardButton, InlineQuery, InlineQueryResultArticle, InputTextMessageContent
from aiogram.filters.command import Command

import src.router.controller.catalog as controller
from src.router.view.catalog import build_category_keyboard, build_subcategory_keyboard, product_nav_keyboard, product_caption, menu
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from src.base.database import DATABASE

class States(StatesGroup):
    meaning = State()
    
router = Router()


@router.message(Command("menu"))
async def open_menu(message: Message):
    await message.answer("*Меню:*", reply_markup=menu, parse_mode="Markdown")


@router.callback_query(F.data == "menu")
async def open_menu_callback(callback: CallbackQuery):
    await callback.message.edit_text("*Меню:*", reply_markup=menu, parse_mode="Markdown")
    await callback.answer()
    
    
@router.callback_query(F.data == "catalog")
async def open_catalog_callback(callback: CallbackQuery):
    await callback.message.delete()
    categories = await controller.get_categories()
    kb = build_category_keyboard(categories, page=0)
    await callback.message.answer("*Каталог*\nВыберите категорию:", reply_markup=kb, parse_mode="Markdown")
    await callback.answer()


@router.callback_query(F.data.regexp(r"^page_(\d+)$"))
async def catalog_page_callback(callback: CallbackQuery):
    page = int(callback.data.split("_")[1])
    catalogs = await controller.get_categories()
    kb = build_category_keyboard(catalogs, page)
    await callback.message.edit_text("*Каталог*\nВыберите категорию:",reply_markup=kb,parse_mode="Markdown")
    await callback.answer()


@router.callback_query(F.data.startswith("category_"))
async def subcategory_callback(callback: CallbackQuery):
    category = callback.data.split("category_", 1)[1].replace('_', ' ')
    subcategories = await controller.get_subcategories(category)
    if not subcategories:
        await callback.answer("В этой категории нет подкатегорий!", show_alert=True)
        return
    kb = build_subcategory_keyboard(subcategories)
    await callback.message.edit_text(f"*{category}*\nВыберите подкатегорию:",reply_markup=kb,parse_mode="Markdown")
    await callback.answer()
    
    
@router.callback_query(F.data.startswith("subcategory_"))
async def show_products_in_subcategory(callback: CallbackQuery):
    subcategory = callback.data[len("subcategory_"):].replace("_", " ")
    products = await controller.get_products_by_subcategory(subcategory)
    if not products:
        await callback.answer("В этой подкатегории нет товаров!", show_alert=True)
        return
    kb = product_nav_keyboard(subcategory, 0, len(products), products[0])
    await callback.message.delete()
    await callback.message.answer_photo(photo=products[0][5], caption=product_caption(products[0]), reply_markup=kb, parse_mode="HTML")
    await callback.answer()


@router.callback_query(F.data.regexp(r"^prodpage_(.+)_(\d+)$"))
async def products_pagination(callback: CallbackQuery):
    subcategory, page = callback.data[len("prodpage_"):].rsplit("_", 1)
    subcategory = subcategory.replace("_", " ")
    page = int(page)
    products = await controller.get_products_by_subcategory(subcategory)
    kb = product_nav_keyboard(subcategory, page, len(products), products[page])
    await callback.message.delete()
    await callback.message.answer_photo(photo=products[page][5], caption=product_caption(products[page]), reply_markup=kb, parse_mode="HTML")
    await callback.answer()
    

@router.callback_query(F.data.startswith("add_basket_"))
async def add_basket(callback: CallbackQuery, state: FSMContext):
    product_id = callback.data.rsplit("add_basket_", 1)[1]
    await callback.message.delete()
    await callback.message.answer("*Введите количество выпечки к приобретению:*", parse_mode="Markdown")
    await state.update_data(product_id=product_id)
    await state.set_state(States.meaning)


@router.message(States.meaning)
async def get_amount(message: Message, state: FSMContext):
    data = await state.get_data()
    res = await controller.state_get_amount(data, message)

    await message.answer(res["message"], reply_markup=res["markup"], parse_mode="Markdown")

    if res["success"]:
        await state.clear()

        
        
     
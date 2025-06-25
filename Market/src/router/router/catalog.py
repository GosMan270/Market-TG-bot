from aiogram import Router, F
from aiogram.types import CallbackQuery, Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters.command import Command

import src.router.controller.catalog as controller
from src.router.view.catalog import build_category_keyboard, build_subcategory_keyboard, product_nav_keyboard, product_caption
router = Router()


@router.message(Command("menu"))
async def open_menu(message: Message):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            (InlineKeyboardButton(text="Каталог", callback_data=f"catalog")),
            (InlineKeyboardButton(text="Корзина", callback_data=f"basket"))
         ],
        
    ])
    await message.answer("*Меню:*", reply_markup=kb, parse_mode="Markdown")


@router.callback_query(F.data == "menu")
async def open_menu_callback(callback: CallbackQuery):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            (InlineKeyboardButton(text="Каталог", callback_data=f"catalog")),
            (InlineKeyboardButton(text="Корзина", callback_data=f"basket"))
         ],

    ])
    await callback.message.edit_text("*Меню:*", reply_markup=kb, parse_mode="Markdown")
    await callback.answer()
    
    
@router.callback_query(F.data == "catalog")
async def open_catalog_callback(callback: CallbackQuery):
    await callback.message.delete()
    categories = await controller.get_categories()
    kb = build_category_keyboard(categories, page=0)
    await callback.message.answer(
        "*Каталог*\nВыберите категорию:",
        reply_markup=kb,
        parse_mode="Markdown"
    )
    await callback.answer()


@router.callback_query(F.data.regexp(r"^page_(\d+)$"))
async def catalog_page_callback(callback: CallbackQuery):
    page = int(callback.data.split("_")[1])
    catalogs = await controller.get_categories()
    kb = build_category_keyboard(catalogs, page)
    await callback.message.edit_text(
        "*Каталог*\nВыберите категорию:",
        reply_markup=kb,
        parse_mode="Markdown"
    )
    await callback.answer()


@router.callback_query(F.data.startswith("category_"))
async def subcategory_callback(callback: CallbackQuery):
    category = callback.data.split("category_", 1)[1].replace('_', ' ')
    subcategories = await controller.get_subcategories(category)
    print(f"Категория: {category}; Подкатегории: {subcategories}")
    if not subcategories:
        await callback.answer("В этой категории нет подкатегорий!", show_alert=True)
        return
    kb = build_subcategory_keyboard(subcategories)
    await callback.message.edit_text(
        f"*{category}*\nВыберите подкатегорию:",
        reply_markup=kb,
        parse_mode="Markdown"
    )
    await callback.answer()
    
    
@router.callback_query(F.data.startswith("subcategory_"))
async def show_products_in_subcategory(callback: CallbackQuery):
    subcategory = callback.data[len("subcategory_"):].replace("_", " ")
    products = await controller.get_products_by_subcategory(subcategory)
    if not products:
        await callback.answer("В этой подкатегории нет товаров!", show_alert=True)
        return
    kb = product_nav_keyboard(subcategory, 0, len(products))
    await callback.message.delete()
    await callback.message.answer_photo(
        photo=products[0][5],
        caption=product_caption(products[0]),
        reply_markup=kb,
        parse_mode="HTML"
    )
    await callback.answer()


@router.callback_query(F.data.regexp(r"^prodpage_(.+)_(\d+)$"))
async def products_pagination(callback: CallbackQuery):
    # prodpage_Подкатегория_номер
    subcategory, page = callback.data[len("prodpage_"):].rsplit("_", 1)
    subcategory = subcategory.replace("_", " ")
    page = int(page)
    products = await controller.get_products_by_subcategory(subcategory)
    kb = product_nav_keyboard(subcategory, page, len(products))
    await callback.message.delete()
    await callback.message.answer_photo(
        photo=products[page][5],
        caption=product_caption(products[page]),
        reply_markup=kb,
        parse_mode="HTML"
    )
    await callback.answer()
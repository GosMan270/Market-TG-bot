import asyncio
from aiogram.filters.command import Command
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message
from aiogram import F, Router

from src.base.database import DATABASE
from src.router.catalog.keyboard import menu

router = Router()


# Команда меню
@router.message(Command("menu"))
async def open_menu(message: Message):
    await message.answer("*Меню:*", reply_markup=menu, parse_mode="Markdown")


@router.callback_query(F.data =="menu")
async def open_menu(callback: CallbackQuery):
    await callback.message.edit_text("*Меню:*", reply_markup=menu, parse_mode="Markdown")
    

# Кнопка "Каталог"
@router.callback_query(F.data == "catalog")
async def open_catalog_callback(callback: CallbackQuery):
    bulki_info = await DATABASE.get_bulki()
    keyboard = []
    for row in bulki_info:
        if row[6] not in keyboard:
            keyboard.append(row[6])

    kb = InlineKeyboardMarkup(inline_keyboard=[])
    for catalog in keyboard:
        kb.inline_keyboard.append([InlineKeyboardButton(text=catalog, callback_data=f"category_{catalog.replace(' ', '_')}")])
    kb.inline_keyboard.append([InlineKeyboardButton(text="Назад в меню🔑", callback_data="menu")])
    
    await callback.message.edit_text("*Подкаталог*\nВыберите категорию булочек:", reply_markup=kb, parse_mode="Markdown")
    await callback.answer()


# Нажатие на категорию
@router.callback_query(F.data.startswith("category_"))
async def subcategory_callback(callback: CallbackQuery):
    category = callback.data.split("category_", 1)[1].replace('_', ' ')
    bulki_info = await DATABASE.get_bulki()
    
    keyboard = []
    for row in bulki_info:
        if row[6] == category and row[7] not in keyboard:
            keyboard.append(row[7])

    kb = InlineKeyboardMarkup(inline_keyboard=[])
    for sub in keyboard:
        kb.inline_keyboard.append([
            InlineKeyboardButton(text=sub, callback_data=f"subcategory_{sub.replace(' ', '_')}")])
    kb.inline_keyboard.append([InlineKeyboardButton(text="Назад в каталог🔑", callback_data="catalog")])
    await callback.message.edit_text(f"*{category}*\nВыберите подкатегорию:", reply_markup=kb, parse_mode="Markdown")
    await callback.answer()
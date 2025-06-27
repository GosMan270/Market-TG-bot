from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

PAGE_SIZE = 4


def build_category_keyboard(categories, page=0):
    start = page * PAGE_SIZE
    end = start + PAGE_SIZE
    kb = InlineKeyboardMarkup(inline_keyboard=[])
    for item in categories[start:end]:
        kb.inline_keyboard.append([
            InlineKeyboardButton(
                text=item,
                callback_data=f"category_{item.replace(' ', '_')}"
            )
        ])
    nav_btns = []
    if page > 0:
        nav_btns.append(InlineKeyboardButton(text="◀️ Назад", callback_data=f"page_{page-1}"))
    if end < len(categories):
        nav_btns.append(InlineKeyboardButton(text="Вперёд ▶️", callback_data=f"page_{page+1}"))
    if nav_btns:
        kb.inline_keyboard.append(nav_btns)
        
    kb.inline_keyboard.append([InlineKeyboardButton(text="Назад в меню🔑", callback_data="menu")])
    return kb


def build_subcategory_keyboard(subcategories):
    kb = InlineKeyboardMarkup(inline_keyboard=[])
    for sub in subcategories:
        kb.inline_keyboard.append([
            InlineKeyboardButton(
                text=sub,
                callback_data=f"subcategory_{sub.replace(' ', '_')}"
            )
        ])
    kb.inline_keyboard.append([InlineKeyboardButton(text="Назад в каталог🔑", callback_data="catalog")])
    return kb


def product_nav_keyboard(subcategory, page, total, product_info):
    nav = []
    if page > 0:
        nav.append(InlineKeyboardButton(text="◀️ Назад", callback_data=f"prodpage_{subcategory}_{page-1}"))
    if page < total - 1:
        nav.append(InlineKeyboardButton(text="Вперёд ▶️", callback_data=f"prodpage_{subcategory}_{page+1}"))
    kb = []
    if nav:
        kb.append(nav)

    kb.append([InlineKeyboardButton(text="Добавить в корзину", callback_data=f"add_basket_{product_info[0]}")])
    kb.append([InlineKeyboardButton(text="Назад в каталог🔑", callback_data="catalog")])
    return InlineKeyboardMarkup(inline_keyboard=kb)


def product_caption(row):
    return (
        f"<b>{row[1]}</b>\n\n"
        f"{row[2]}\n\n"
        f"<b>Цена:</b> {row[3]} руб.\n"
        f"<b>Калорий:</b> {row[4]}"
    )


menu = InlineKeyboardMarkup(inline_keyboard=[
    [
        (InlineKeyboardButton(text="Каталог", callback_data=f"catalog")),
        (InlineKeyboardButton(text="Корзина", callback_data=f"basket"))
    ],
])




from src.base.database import DATABASE
# from src.router.view.catalog import build_keyboard, product_nav_keyboard, product_caption


# Получение списка уникальных категорий каталога
async def get_categories():
    catalog_info = await DATABASE.get_catalog()
    catalogs = []
    for row in catalog_info:
        if row[6] not in catalogs:
            catalogs.append(row[6])
    return catalogs


# Получение подкатегорий для выбранной категории
async def get_subcategories(category):
    catalog_info = await DATABASE.get_catalog()
    subcategories = []
    for row in catalog_info:
        if row[6] == category and row[7] not in subcategories:
            subcategories.append(row[7])
    return subcategories


# Получение товаров по подкатегории
async def get_products_by_subcategory(subcategory):
    catalog_info = await DATABASE.get_catalog()
    return [row for row in catalog_info if row[8] == subcategory]
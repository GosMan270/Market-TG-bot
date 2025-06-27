# src/router/controller/faq.py

from src.base.database import DATABASE

async def get_faq():
    res = await DATABASE.get_table("faq")
    result = []
    for row in res:
        result.append({"q": row["question"], "a": row["answer"]})
    return result
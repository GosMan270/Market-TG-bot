import os
import time
import logging
from decimal import Decimal
from urllib.parse import urlencode, quote
import aiohttp

from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, Message
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from dotenv import load_dotenv

from src.base.database import DATABASE

router = Router()
logger = logging.getLogger(__name__)

class SetState(StatesGroup):
    sum = State()

class sum:
    sum = 20

SUM = sum()

dotenv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), 'run', 'config.env')
print(f"Dotenv path: {dotenv_path} - exists: {os.path.exists(dotenv_path)}")
load_dotenv(dotenv_path)

yoomoney_access_token = str(os.getenv('yoomoney_access_token'))
yoomoney_receiver = str(os.getenv('yoomoney_receiver'))
yoomoney_scopes = str(os.getenv('yoomoney_scopes'))
yoomoney_redirect_url = str(os.getenv('yoomoney_redirect_url'))
yoomoney_client_id = str(os.getenv('yoomoney_client_id'))
debug_yoomoney_mode = str(os.getenv('debug_yoomoney_mode'))

print(yoomoney_access_token)
print(yoomoney_receiver)
print(yoomoney_scopes)
print(yoomoney_redirect_url)
print(yoomoney_client_id)



def create_quickpay_link(amount, user_id):
    label = f"payment_{user_id}_{amount:.2f}_{int(time.time())}"
    params = {
        "receiver": yoomoney_receiver,
        "quickpay-form": "shop",
        "targets": f"Пополнение {amount}",
        "paymentType": "AC",
        "sum": f"{amount:.2f}",
        "label": label,
        "successURL": ""
    }
    encoded = urlencode(params, quote_via=quote)
    url = f"https://yoomoney.ru/quickpay/confirm.xml?{encoded}"
    print(url, label)
    print("yoomoney_scopes =", yoomoney_scopes)

    return url, label
    
async def check_yoomoney_payment(label: str):
    if debug_yoomoney_mode:
        print("[DEMO] YooMoney check is always successful for label:", label)
        return True  # Симуляция успешной оплаты
    else:
        headers = {
            "Authorization": f"Bearer {yoomoney_access_token}",
            "Content-Type": "application/x-www-form-urlencoded",
        }
        data = {
            "label": label,
            "records": 10,
            "type": "deposition"
        }
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(yoomoney_scopes, headers=headers, data=data) as resp:
                    if resp.status == 200:
                        result = await resp.json()
                        for op in result.get("operations", []):
                            if op.get("label") == label and op.get("status") == "success":
                                return True
                    else:
                        logger.error(f"YooMoney API error: {resp.status} {await resp.text()}")
            except Exception as e:
                logger.exception(f"Error while checking payment in YooMoney: {e}")
        return False



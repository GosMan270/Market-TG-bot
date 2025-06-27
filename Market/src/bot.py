import aiogram
import asyncio
import os

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from dotenv import load_dotenv

# from router.basket import BASKET
from src.router.router.catalog import router as catalog_router
from src.router.router.basket import router as basket_router
from src.router.router.payment import router as payment_router
from src.router.controller.payment import router as payment_router_2
from src.router.router.faq import router as faq_router

from src.base.database import DATABASE
from src.base.utils import check_sub


class Bot:
	def __init__(self):
		dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'run', 'config.env')
		load_dotenv(dotenv_path)
		self.tg_bot_key = str(os.getenv('tg_bot_key'))
		
		self.db_host = str(os.getenv('database_host'))
		self.db_port = str(os.getenv('database_port'))
		self.db_user = str(os.getenv('database_user'))
		self.db_password = str(os.getenv('database_password'))
		self.db_database = str(os.getenv('database_database'))
		
		self.channel_id = int(os.getenv('channel_id'))
		self.group_id = int(os.getenv('group_id'))
		self.link_channel = str(os.getenv('link_channel'))
		
		self.yoomoney_access_token = str(os.getenv('yoomoney_access_token'))
		self.yoomoney_receiver = str(os.getenv('yoomoney_receiver'))
		self.yoomoney_scopes = str(os.getenv('yoomoney_scopes'))
		self.yoomoney_redirect_url = str(os.getenv('yoomoney_redirect_url'))
		self.yoomoney_client_id = str(os.getenv('yoomoney_client_id'))
		
		self.exel_name = str(os.getenv('exel_name'))
		self.bot: Bot = None
		self.dispatch: Dispatcher = None
		self._shutdown_event = asyncio.Event()
	
	async def run(self):
		await DATABASE.open_connection(
			self.db_host,
			self.db_port,
			self.db_user,
			self.db_password,
			self.db_database
		)
		
		self.bot = aiogram.Bot(self.tg_bot_key)
		self.dispatch = aiogram.Dispatcher()
		
		self.dispatch.include_router(basket_router)
		self.dispatch.include_router(catalog_router)
		self.dispatch.include_router(payment_router)
		self.dispatch.include_router(payment_router_2)
		self.dispatch.include_router(faq_router)
		self.register_handlers()
		
		await self.dispatch.start_polling(self.bot)
	
	def register_handlers(self):
		@self.dispatch.message(Command("start"))
		async def start_command(message: types.Message):
			dotenv_path = os.path.join(os.path.dirname(__file__), 'run', 'config.env')
			load_dotenv(dotenv_path)
			
			user_id = message.from_user.id
			channel_id = int(os.getenv('channel_id'))
			group_id = int(os.getenv('group_id'))
			link_channel = os.getenv('link_channel')
			print(user_id)
			result = await check_sub(self.bot, user_id, channel_id, group_id, link_channel)
			await message.answer(result)


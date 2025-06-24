import sys
import asyncio
import logging

from src.bot import Bot

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


if __name__ == "__main__":
	
	try:
		bot = Bot()
		asyncio.run(bot.run())
	except KeyboardInterrupt:
		logging.info("Bot is shutdown")
	except Exception as e:
		logging.exception("An error occurred during bot execution:")
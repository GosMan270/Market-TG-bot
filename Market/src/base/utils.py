from aiogram.exceptions import TelegramForbiddenError, TelegramBadRequest
from aiogram import Bot


async def check_sub(bot: Bot, user_id: int, channel_id: int, group_id: int, link_channel: str, link_group: str):
	try:
		channel_member = await bot.get_chat_member(channel_id, user_id)
		in_channel = channel_member.status in ['member', 'creator', 'administrator']
	
	
		group_member = await bot.get_chat_member(group_id, user_id)
		in_group = group_member.status in ['member', 'creator', 'administrator']
		
		
		if in_channel and in_group:
			return 'Добро пожаловать!\nПропишите - /menu.'
		elif not in_channel and not in_group:
			return (f'Вы не подписаны на канал и не состоите в группе!\n'
			        f'Подпишитесь: {link_channel}\nВступите в группу: {link_group}\n'
			        f'для доступа к магазину')
		elif not in_channel:
			return (f'Вы не подписаны на канал!\n'
			        f'Подпишитесь: {link_channel}\nдля доступа к магазину')
		elif not in_group:
			return (f'Вы не состоите в группе!\n'
			        f'Вступите: {link_group}\nдля доступа к магазину')
	except TelegramForbiddenError as e:
		return 'Ошибка: бот не может проверить вашу подписку. Проверьте права доступа бота к каналу и группе.'
	except TelegramBadRequest as e:
		return 'Ошибка запроса к Telegram. Возможно, вы забанены или возникла другая проблема.'
	except Exception as e:
		print(e)
		return 'Произошла неизвестная ошибка при проверке подписки. Попробуйте позже.'

# Пример вызова:
# message = await check_sub(bot, user_id, channel_id, group_id, link_channel, link_group)
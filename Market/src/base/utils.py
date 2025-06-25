from aiogram.exceptions import TelegramForbiddenError, TelegramBadRequest
from aiogram import Bot

async def check_sub(bot: Bot, user_id: int, channel_id: int, group_id: int, link_channel: str):
    try:
        member = await bot.get_chat_member(channel_id, user_id)
        if member.status in ['member', 'creator', 'administrator']:
            return 'Добро пожаловать!\nПропишите - /menu.'
        else:
            return f'Вы не подписаны на канал!\nПодпишитесь: {link_channel} для доступа к магазину'
    except TelegramForbiddenError:
        return 'Ошибка: бот не может проверить вашу подписку на канал. Проверьте настройки канала или дайте боту права администратора.'
    except TelegramBadRequest:
        return 'Ошибка запроса к Telegram. Возможно, вы забанены в канале или возникла другая проблема.'
    except Exception as e:
        print(e)
        return 'Произошла неизвестная ошибка при проверке подписки. Попробуйте позже.'
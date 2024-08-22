import asyncio
import logging
from typing import Union

from aiogram import Bot
from aiogram import exceptions


async def send_image(
        bot: Bot,
        user_id: Union[int, str],
        img
) -> None:
    try:
        b=0
        await bot.send_photo(
            user_id,
            img,
            caption="Изображение из файла на компьютере"
        )
    except exceptions.TelegramBadRequest as e:
        logging.error("Telegram server says - Bad Request: chat not found")
    except exceptions.TelegramForbiddenError:
        logging.error(f"Target [ID:{user_id}]: got TelegramForbiddenError")
    except exceptions.TelegramRetryAfter as e:
        logging.error(
            f"Target [ID:{user_id}]: Flood limit is exceeded. Sleep {e.retry_after} seconds."
        )
        await asyncio.sleep(e.retry_after)
        return await send_image(
            bot, user_id, img
        )  # Recursive call
    except exceptions.TelegramAPIError:
        logging.exception(f"Target [ID:{user_id}]: failed")
    else:
        logging.info(f"Target [ID:{user_id}]: success")
        return True
    return False

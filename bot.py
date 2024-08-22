import asyncio
import datetime
import logging
import queue
import multiprocessing
from threading import Thread

from aiogram.types import FSInputFile
from diffusers import DiffusionPipeline
import torch
from PIL import Image


import time

import betterlogging as bl
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import RedisStorage, DefaultKeyBuilder

from tgbot.config import load_config, Config
from tgbot.handlers import routers_list
from tgbot.middlewares.config import ConfigMiddleware
from tgbot.services import broadcaster, sender_image


my_qq = multiprocessing.Queue()

# Create the diffusion pipeline
pipe = DiffusionPipeline.from_pretrained(
    "playgroundai/playground-v2-1024px-aesthetic",
    torch_dtype=torch.float16,
    use_safetensors=True,
    add_watermarker=False,
    variant="fp16"
)
pipe.to("cuda")

# Generate the image
# prompt = "Small kitten playing wich cotton ball, warm color palette, muted colors, detailed, 8k"
# image = pipe(prompt=prompt, guidance_scale=3.0).images[0]
# #save picture
# save_path = "C:\\Users\\Nikola\\Pictures\\Saved Pictures\\generated_image.png"
# image.save(save_path)



def generate_image(prompt:str):
    # Generate the image
    # prompt = "Small kitten playing wich cotton ball, warm color palette, muted colors, detailed, 8k"
    image = pipe(prompt=prompt, guidance_scale=3.0).images[0]
    # #save picture
    # save_path = "C:\\Users\\Nikola\\Pictures\\Saved Pictures\\generated_image.png"
    return image
    # image.save(save_path)


async def on_startup(bot: Bot, admin_ids: list[int]):
    await broadcaster.broadcast(bot, admin_ids, "Бот был запущен")

async def send_image(bot: Bot, id: int, img):
    await sender_image.send_image(bot, id, img)


def register_global_middlewares(dp: Dispatcher, config: Config, session_pool=None):
    """
    Register global middlewares for the given dispatcher.
    Global middlewares here are the ones that are applied to all the handlers (you specify the type of update)

    :param dp: The dispatcher instance.
    :type dp: Dispatcher
    :param config: The configuration object from the loaded configuration.
    :param session_pool: Optional session pool object for the database using SQLAlchemy.
    :return: None
    """
    middleware_types = [
        ConfigMiddleware(config),
        # DatabaseMiddleware(session_pool),
    ]

    for middleware_type in middleware_types:
        dp.message.outer_middleware(middleware_type)
        dp.callback_query.outer_middleware(middleware_type)


def setup_logging():
    """
    Set up logging configuration for the application.

    This method initializes the logging configuration for the application.
    It sets the log level to INFO and configures a basic colorized log for
    output. The log format includes the filename, line number, log level,
    timestamp, logger name, and log message.

    Returns:
        None

    Example usage:
        setup_logging()
    """
    log_level = logging.INFO
    bl.basic_colorized_config(level=log_level)

    logging.basicConfig(
        level=logging.INFO,
        format="%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s",
    )
    logger = logging.getLogger(__name__)
    logger.info("Starting bot")


def get_storage(config):
    """
    Return storage based on the provided configuration.

    Args:
        config (Config): The configuration object.

    Returns:
        Storage: The storage object based on the configuration.

    """
    if config.tg_bot.use_redis:
        return RedisStorage.from_url(
            config.redis.dsn(),
            key_builder=DefaultKeyBuilder(with_bot_id=True, with_destiny=True),
        )
    else:
        return MemoryStorage()


async def main():
    # global my_q
    setup_logging()

    config = load_config(".env")
    storage = get_storage(config)

    # my_q=config.qq.qq

    bot = Bot(token=config.tg_bot.token, parse_mode="HTML")
    bot1 = Bot(token=config.tg_bot.token, parse_mode="HTML")
    dp = Dispatcher(storage=storage)

    dp.include_routers(*routers_list)

    register_global_middlewares(dp, config)
    Thread(target=run_tread, args=(bot1,)).start()

    await on_startup(bot, config.tg_bot.admin_ids)
    await dp.start_polling(bot, my_que=my_qq)

def run_bot():
    asyncio.run(main())

def run_tread(bot: Bot):
    asyncio.run(queue_reader(bot))


async def queue_reader(bot: Bot):
    print('к чтению приступил')
    while True:
        # Без этого загрузка процессора улетает в плеху.
        # А так получается пауза между опросами - 1 секунда
        time.sleep(1)
        if not my_qq.empty():
            full = my_qq.get()
            image = generate_image(full['prompt'])
            image.save('image.png')

            # Это гарантированно рабочий способ, но файл надо предварительно сохранить на диск (на пк локально директорию указать?)
            # image_from_pc = open('C:/Users/Nikola/Pictures/image.png', 'rb')
            image_from_pc = FSInputFile("image.png")
            await send_image(bot, full['id'], image_from_pc)
            print(f'было передано {my_qq.get()}')


if __name__ == "__main__":
    try:
        # Thread(target=queue_reader).start()

        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.error("Бот был остановлен!")

import multiprocessing
import queue

from aiogram import types, Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.utils.markdown import hcode
from aiogram.filters import Command

from tgbot.config import Config

# import bot

diffusion_router = Router()

@diffusion_router.message(Command("create"))
async def bot_echo(message: types.Message, my_que:multiprocessing.Queue):
    text1 = message.text[7:].lstrip()
    text = [text1]
    # data["config"]
    q = my_que
    full = {'id': message.chat.id, 'prompt': text}
    q.put(full)
    # text = ["Эхо без состояния.", "Сообщение:", message.text]

    await message.answer("Задание поставлено в очередь:\n".join(text))


@diffusion_router.message(F.text)
async def bot_echo_all(message: types.Message, state: FSMContext):
    state_name = await state.get_state()
    text = [
        f"Ехо в состоянии {hcode(state_name)}",
        "Текст сообщения:",
        hcode(message.text),
    ]
    await message.answer("\n".join(text))

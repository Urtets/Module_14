import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import text
from config import *
from keyboards import *

logging.basicConfig(level=logging.INFO)
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer(f"Добро пожаловать, {message.from_user.username}! " +text.start, reply_markup=start_kb)


# message.answer_photo
# message.answer_video
# message.answer_file


@dp.message_handler(text='О нас')
async def price(message: types.Message):
    with open('pictures/room-clipart-md.png', 'rb') as img:
        await message.answer_photo(img, text.about, reply_markup=start_kb)


@dp.message_handler(text='Стоимость')
async def info(message: types.Message):

    await message.answer("Что вас интересует?", reply_markup=catalog_kb)


@dp.callback_query_handler(text = "medium")
async def buy_m(call):
    await call.message.answer(text.Mgame, reply_markup=buy_kb)
    await call.answer()


@dp.callback_query_handler(text = "big")
async def buy_l(call):
    await call.message.answer(text.Lgame, reply_markup=buy_kb)
    await call.answer()


@dp.callback_query_handler(text = "mega")
async def buy_xl(call):
    await call.message.answer(text.XLgame, reply_markup=buy_kb)
    await call.answer()


@dp.callback_query_handler(text = "other")
async def buy_other(call):
    await call.message.answer(text.other, reply_markup=buy_kb)
    await call.answer()


@dp.callback_query_handler(text = "back_to_catalog")
async def back(call):
    await call.message.answer("Что вас интересует?", reply_markup=catalog_kb)
    await call.answer()


if __name__ == '__main__':
    executor.start_polling(dp)

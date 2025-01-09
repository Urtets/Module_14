import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
import asyncio
from sales_bot.api_token import api_token
from keayboards_m_14 import *
from product_text import *

logging.basicConfig(level=logging.INFO)
api = api_token
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

# kb = ReplyKeyboardMarkup([[KeyboardButton(text='Рассчитать'), KeyboardButton(text='Информация')]], resize_keyboard=True)
# inkb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories'),
#                                               InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')]])

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dp.message_handler(text='Рассчитать')
async def main_menu(message: types.Message):
    await message.answer('Выберите опцию', reply_markup=option_inkb)


@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.message.answer('для мужчин: 10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5 \n'
                              'для женщин: 10 x вес (кг) + 6,25 x рост (см) – 5 x возраст (г) – 161')


@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer(f'Привет, {message["from"]["first_name"]}!'
                         f'Я бот, помогающий твоему здоровью. '
                         f'Выбери одну из кнопок: ', reply_markup=start_kb)



@dp.message_handler(text='Информация')
async def inform(message):
    await message.answer('Информация о боте')


@dp.callback_query_handler(text='calories')
async def set_age(call):
    await call.message.answer("Введите свой возраст")
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer("Введите свой рост:")
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer("Введите свой вес:")
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    age = int(data['age'])
    weight = int(data['weight'])
    growth = int(data['growth'])
    print(age, weight, growth)
    result = (10 * weight) + (6.25 * growth) - (5 * age) + 5
    await message.answer(f"Ваша норма калорий: {result} в день")
    await state.finish()


@dp.message_handler(text='Купить')
async def get_buying_list(message: types.Message):
    with open('imgs/Luminous Capsule Presentation.jpeg', 'rb') as img:
        await message.answer_photo(img, stomach_reducer)
    with open('imgs/Turbotext AI Image 5998295.png', 'rb') as img:
        await message.answer_photo(img, butt_reducer)
    with open('imgs/Clear Plastic Bottle with Capsules.jpeg', 'rb') as img:
        await message.answer_photo(img, side_reducer)
    with open('imgs/Wellness Supplements Assortment on Wooden Backdrop.jpeg', 'rb') as img:
        await message.answer_photo(img, arm_reducer, reply_markup=inline_menu)


@dp.callback_query_handler(text='product_buying')
async def send_confirm_message(call: types.CallbackQuery):
    await call.message.answer('Вы успешно приобрели продукт!')


@dp.message_handler()
async def any_text(message):
    await message.answer(f'Добрый день, {message["from"]["first_name"]}!')
    await message.answer(f'Чтобы начать пользоваться услугами бота, пожалуйста, '
                         f'введите слово "/start"')


if __name__ == '__main__':
    executor.start_polling(dp)
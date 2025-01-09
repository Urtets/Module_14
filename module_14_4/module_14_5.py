import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from sales_bot.api_token import api_token
from keayboards_m_14 import *
from product_text import *
import crud_functions

logging.basicConfig(level=logging.INFO)
api = api_token
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


class RegistrationState(StatesGroup):
    username = State()
    email = State()
    age = State()
    balance = State(state='1000')

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
    product_list = crud_functions.get_all_products()
    for i in range(len(reducer_list)):
        with open(img_list[i], 'rb') as img:
            reducer = product_list[i]
            some_text = f'Название: {reducer.title} | Описание: {reducer.description} | Стоимость: {reducer.price}'
            await message.answer_photo(img, some_text)
    await message.answer('Какой продукт для покупки Вас заинтересовал?', reply_markup=inline_menu)


@dp.callback_query_handler(text='product_buying')
async def send_confirm_message(call: types.CallbackQuery):
    await call.message.answer('Вы успешно приобрели продукт!')


@dp.message_handler(text='Регистрация')
async def sign_up(message: types.Message):
    await message.answer("Введите имя пользователя (только латинский алфавит):")
    await RegistrationState.username.set()


@dp.message_handler(state=RegistrationState.username)
async def set_username(message: types.Message, state):
    username = message.text
    if crud_functions.is_included(username):
        await message.answer("Пользователь существует, введите другое имя")
        await RegistrationState.username.set()
    else:
        await state.update_data(username=message.text)
        await message.answer("Введите свой email:")
        await RegistrationState.email.set()


@dp.message_handler(state=RegistrationState.email)
async def set_email(message: types.Message, state):
    await state.update_data(email=message.text)
    await message.answer("Введите свой возраст:")
    await RegistrationState.age.set()


@dp.message_handler(state=RegistrationState.age)
async def set_age(message: types.Message, state):
    await state.update_data(age=message.text)
    data = await state.get_data()
    username, email, age = data['username'], data['email'], data['age']
    print(f'{username}, {email}, {age}')
    crud_functions.add_user(username, email, age)
    await state.finish()


@dp.message_handler()
async def any_text(message):
    await message.answer(f'Добрый день, {message["from"]["first_name"]}!')
    await message.answer(f'Чтобы начать пользоваться услугами бота, пожалуйста, '
                         f'введите слово "/start"')


if __name__ == '__main__':
    executor.start_polling(dp)
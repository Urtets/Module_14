from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

start_kb = ReplyKeyboardMarkup(
    [
        [KeyboardButton(text='Рассчитать'), KeyboardButton(text='Информация')],
        [KeyboardButton(text='Купить')]
    ],
    resize_keyboard=True
)

option_inkb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories'),
     InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')]
])

inline_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Product1', callback_data='product_buying'),
     InlineKeyboardButton(text='Product2', callback_data='product_buying'),
     InlineKeyboardButton(text='Product3', callback_data='product_buying'),
     InlineKeyboardButton(text='Product4', callback_data='product_buying')]
])

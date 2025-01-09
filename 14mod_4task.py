""" Домашнее задание по теме "План написания админ панели"  Часть 1"""

"""_______блок подключения фрейворков, библиотек и пр._______________________________________________________________"""

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import asyncio
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from crud_functions import *


"""_______блок подключение бота______________________________________________________________________________________"""

api = "7648874159:AAECVpuMkZJmamg6UhqB4RMnDVW9TyDskM4"  # необходимо скрывать, КТ (token to access the HTTP API).
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())


"""_______блок подключения клавиатур_________________________________________________________________________________"""

kb = ReplyKeyboardMarkup(resize_keyboard=True)
button1 = KeyboardButton(text='Информация')
button2 = KeyboardButton(text='Рассчитать')
button3 = KeyboardButton(text='Купить')
kb.insert(button1)
kb.insert(button2)
kb.add(button3)
# kb.add - стандарт,  kb.row    kb.insert   -   об этом позже подробнее...

kb_IL = InlineKeyboardMarkup()
button_IL1 = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
button_IL2 = InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')
kb_IL.insert(button_IL1)
kb_IL.insert(button_IL2)

kb_IL_F = types.InlineKeyboardMarkup(row_width=4) # меняю стандартное количество столбцов клавиатуры
button_IL_F1 = InlineKeyboardButton(text='Продукт 1', callback_data='product_buying')
button_IL_F2 = InlineKeyboardButton(text='Продукт 2', callback_data='product_buying')
button_IL_F3 = InlineKeyboardButton(text='Продукт 3', callback_data='product_buying')
button_IL_F4 = InlineKeyboardButton(text='Продукт 4', callback_data='product_buying')
kb_IL_F.insert(button_IL_F1)
kb_IL_F.insert(button_IL_F2)
kb_IL_F.insert(button_IL_F3)
kb_IL_F.insert(button_IL_F4)


"""_______блок основных хендлеров____________________________________________________________________________________"""


@dp.message_handler(commands=['start'])
async def start_message(message):
    print("Реакция на команду /start")
    await message.answer(f'Привет {message.from_user.username}! Я бот помогающий твоему здоровью.', reply_markup=kb)


@dp.message_handler(text=['Информация'])
async def set_age(message):
    await message.answer("Могу рассчитать твою суточную норму потребления каллорий")


@dp.message_handler(text=['Рассчитать'])
async def set_age(message):
    await message.answer("Выберите опцию:", reply_markup=kb_IL)


@dp.message_handler(text=['Купить'])
async def get_buying_list(message):
    d_p = get_all_products()
    for i in range(1, 5):
        await message.answer(f'Название: {d_p[i - 1][1]} | {d_p[i - 1][2]} | Цена: {d_p[i - 1][3]}руб')   # описание пр-та
        with open(f'Img{i}.png', "rb") as j:
            await message.answer_photo(j, f'{d_p[0][1]}') # направляем изображение продукта, с его номером
    await message.answer("Выберите продукт для покупки:", reply_markup=kb_IL_F)


@dp.callback_query_handler(text='product_buying')
async def get_formulas(call):
    await call.message.answer("Вы успешно приобрели продукт!")
    await call.answer()


@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.message.answer("для мужчин: 10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5")
    await call.message.answer("для женщин: 10 x вес (кг) + 6,25 x рост (см) – 5 x возраст (г) – 161")
    await call.answer()


"""_______блок хендлеров "машины состояний"__________________________________________________________________________"""


class UserState (StatesGroup):  # создание класса состояний
    age = State()
    growth = State()
    weight = State()


@dp.callback_query_handler(text='calories')
async def set_age(call):
    await call.message.answer("Введите свой возраст, г:")
    await call.answer()
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer("Введите свой рост, см:")
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer("Введите свой вес, кг:")
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    await message.answer(f"Cуточная норма для мужчин: "
                         f"{10 * int(data['weight']) + 6.25 * int(data['growth']) - 5 * int(data['age']) + 5} ккал")
    await message.answer(f"Cуточная норма для женщин: "
                         f"{10 * int(data['weight']) + 6.25 * int(data['growth']) - 5 * int(data['age']) - 161} ккал"
                         , reply_markup=kb)
    await state.finish()


"""_______блок дополнительных хендреров______________________________________________________________________________"""


@dp.message_handler()
async def urban_message(message):
    print("Реакция на другие сообщения")
    await message.answer("Введите команду /start, чтобы начать общение")


"""_______блок запуска бота__________________________________________________________________________________________"""

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

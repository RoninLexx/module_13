from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
import asyncio

api = ""
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


# Создаем клавиатуру
keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
button_calculate = types.KeyboardButton(text="Рассчитать")
button_info = types.KeyboardButton(text="Информация")
keyboard.add(button_calculate, button_info)


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.reply("Привет! Выберите действие:", reply_markup=keyboard)


@dp.message_handler(lambda message: message.text.lower() == "рассчитать")
async def main_menu(message: types.Message):
    inline_keyboard = types.InlineKeyboardMarkup()
    button_calories = types.InlineKeyboardButton(text="Рассчитать норму калорий", callback_data='calories')
    button_formulas = types.InlineKeyboardButton(text="Формулы расчёта", callback_data='formulas')
    inline_keyboard.add(button_calories, button_formulas)
    await message.reply("Выберите опцию:", reply_markup=inline_keyboard)


@dp.callback_query_handler(lambda call: call.data == 'formulas')
async def get_formulas(call: types.CallbackQuery):
    formula_text = "Формула Миффлина-Сан Жеора для мужчин:\n10 * вес + 6.25 * рост - 5 * возраст + 5"
    await call.message.reply(formula_text)
    await call.answer()


@dp.callback_query_handler(lambda call: call.data == 'calories')
async def set_age(call: types.CallbackQuery):
    await call.message.reply("Введите свой возраст:")
    await call.answer()
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message: types.Message, state: FSMContext):
    await state.update_data(age=int(message.text))
    await message.reply("Введите свой рост:")
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message: types.Message, state: FSMContext):
    await state.update_data(growth=int(message.text))
    await message.reply("Введите свой вес:")
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message: types.Message, state: FSMContext):
    await state.update_data(weight=int(message.text))

    data = await state.get_data()

    # Выбор формулы, например для мужчин:
    age = data.get('age')
    growth = data.get('growth')
    weight = data.get('weight')

    # Формула Миффлина - Сан Жеора для мужчин
    calories = 10 * weight + 6.25 * growth - 5 * age + 5

    await message.reply(f"Ваша норма калорий: {calories}")

    # Завершаем состояния
    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

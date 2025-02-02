from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import asyncio

api = ""
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

@dp.message_handler(text = ['Urban', 'ff'])
async def urban_message(message):
    print("Urban message")
    await message.answer("Urban message" + " - " + message.text)

@dp.message_handler(commands=['start'])
async def start_message(message):
    print("Start message")
    await message.answer("Привет! Я тренировочный бот")

@dp.message_handler(commands=['help'])
async def help_message(message):
    print("Help message")
    await message.answer("Help on the way!")

@dp.message_handler(commands=['stop'])
async def stop_message(message):
    print("Stop message")
    await message.answer("Ну нееее! Я ещё не устал!")

@dp.message_handler()
async def all_message(message):
    print("Введите команду /start, чтобы начать общение.")
    await message.answer(message.text + " - " + "Я ещё этого не понимаю")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

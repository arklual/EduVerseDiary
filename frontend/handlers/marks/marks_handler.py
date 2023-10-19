from aiogram import types
import middleware
from frontend.keyboards import main as keyboard_main

async def marks(message: types.Message):
    messages = await middleware.marks(message.from_id)
    for i in messages:
        await message.answer(i)

async def finals(message: types.Message):
    messages = await middleware.finals(message.from_id)
    for i in messages:
        await message.answer(i)

async def setup(dp):
    print('Register marks handler...', end='')
    dp.register_message_handler(marks, lambda message: message.text == "🧮 Оценки" or message.text == "/get_marks")
    #dp.register_message_handler(finals, lambda message: message.text == "🧮 Итоговые" or message.text == "/finals")
    print('Succsess')
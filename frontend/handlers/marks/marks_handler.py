from aiogram import types
import middleware

async def marks(message: types.Message):
    marks = await middleware.marks(message.from_id)
    await message.answer(str(marks))

async def setup(dp):
    print('Register marks handler...', end='')
    dp.register_message_handler(marks, lambda message: message.text == "Оценки" or message.text == "/get_marks")
    print('Succsess')
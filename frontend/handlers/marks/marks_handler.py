from aiogram import types
import middleware
from middleware import send_new_marks as um

async def marks(message: types.Message):
    messages = await middleware.marks(message.from_id)
    for i in messages:
        await message.answer(i)

### TEMP
async def update_marks(message: types.Message):
    await um(message.bot)
###

async def setup(dp):
    print('Register marks handler...', end='')
    dp.register_message_handler(marks, lambda message: message.text == "🧮 Оценки" or message.text == "/get_marks")
    ###temp
    dp.register_message_handler(update_marks, lambda message: message.text == "up" or message.text == "/update_marks")
    ###
    print('Succsess')
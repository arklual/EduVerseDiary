from aiogram import types
import middleware

async def marks(message: types.Message):
    await message.answer('Упс, официальный журнал не доступен.')
    '''
    messages = await middleware.marks(message.from_id)
    for i in messages:
        await message.answer(i)'''


async def setup(dp):
    print('Register marks handler...', end='')
    dp.register_message_handler(marks, lambda message: message.text == "🧮 Оценки" or message.text == "/get_marks")
    print('Succsess')
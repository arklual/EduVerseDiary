from aiogram import types

async def marks(message: types.Message):
    # TODO get marks
    # TODO send gotten marks
    pass

async def setup(dp):
    dp.register_message_handler(marks, lambda message: message.text == "Домашнее задание" or message.text == "/get_homework")

from aiogram import types
from aiogram.utils.markdown import hbold
from . import keyboards
from frontend.keyboards import main as main_keyboard
import middleware

async def notes_menu(message: types.Message):
    notes = await middleware.notes()
    await message.answer("По какому предмету Вы хотите получить конспекты?", reply_markup=keyboards.subjects(notes))

async def notes(callback_query: types.CallbackQuery):
    subject = callback_query.data[7:]
    id = callback_query.from_user.id
    await bot.send_message(id, f'Записи по предмету {subject}:', reply_markup=main_keyboard())
    await bot.answer_callback_query(callback_query.id)
    notes = await middleware.notes()
    to_send = []
    for note in notes:
        if subject == note.subject:
            to_send += [note.files]
    for n in to_send:
        media = types.MediaGroup()
        for file in n:
            media.attach_photo(file['file']['url'])
        await bot.send_media_group(id, media)     

async def setup(dp, b):
    print('Register notes handler...', end='')
    dp.register_message_handler(notes_menu, lambda message: message.text == "Конспекты" or message.text == "/get_notes")
    dp.register_callback_query_handler(notes, lambda c: c.data and c.data.startswith('subject'))
    global bot
    bot = b
    print('Succsess')

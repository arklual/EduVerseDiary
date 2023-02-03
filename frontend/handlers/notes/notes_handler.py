from aiogram import types
from aiogram.utils.markdown import hbold
from . import keyboards
from frontend.keyboards import main as main_keyboard
import middleware

async def notes_menu(message: types.Message):
    notes = await middleware.notes()
    await message.answer("По какому предмету Вы хотите получить конспекты?", reply_markup=keyboards.subjects(notes))

async def notes(call: types.CallbackQuery):
    subject = call.data[7:]
    id = call.from_user.id
    await call.message.answer(f'Записи по предмету {subject}:', reply_markup=main_keyboard())
    await call.answer()
    notes = await middleware.notes()
    to_send = []
    for note in notes:
        if subject == note.subject:
            to_send += [note.files]
    for n in to_send:
        media = types.MediaGroup()
        for file in n:
            media.attach_photo(file['file']['url'])
        await call.message.answer_media_group(media)     

async def setup(dp):
    print('Register notes handler...', end='')
    dp.register_message_handler(notes_menu, lambda message: message.text == "Конспекты" or message.text == "/get_notes")
    dp.register_callback_query_handler(notes, lambda c: c.data and c.data.startswith('subject'))
    print('Succsess')

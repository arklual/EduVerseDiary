from aiogram import types
from aiogram.utils.markdown import hbold
from . import keyboards
from frontend.keyboards import main as main_keyboard
import middleware

async def notes_menu(message: types.Message):
    notes = await middleware.notes()
    await message.answer("По какому предмету Вы хотите получить конспекты?", reply_markup=keyboards.subjects(notes))

async def subject_menu(call: types.CallbackQuery):
    subject = call.data[7:]
    await call.message.answer(f'Выбери тему конспекта:', reply_markup=main_keyboard())
    notes = await middleware.notes()
    themes = []
    for note in notes:
        if subject == note.subject:
            themes += [note.theme]
    messege = ''
    for i in range(len(themes)):
        messege += f'{i+1}. {themes[i]}\n'
    await call.message.answer(messege, reply_markup=keyboards.themes(subject, len(themes)))  
    await call.answer()   

async def notes(call: types.CallbackQuery):
    subject = call.data.split('|')[1][7:]
    theme_id = int(call.data.split('|')[0][5:])
    notes = await middleware.notes()
    i = 0
    for note in notes:
        if subject == note.subject:
            if i==theme_id:
                media = types.MediaGroup()
                for file in note.files:
                    media.attach_photo(file['file']['url'])
                await call.message.answer_media_group(media) 
                break    
            i += 1
    await call.answer()

async def setup(dp):
    print('Register notes handler...', end='')
    dp.register_message_handler(notes_menu, lambda message: message.text == "Конспекты" or message.text == "/get_notes")
    dp.register_callback_query_handler(subject_menu, lambda c: c.data and c.data.startswith('subject'))
    dp.register_callback_query_handler(notes, lambda c: c.data and c.data.startswith('theme'))
    print('Succsess')

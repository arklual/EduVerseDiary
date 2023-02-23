from . import keyboards
from frontend.keyboards import main as keyboard_main
from aiogram import types
from aiogram.utils.markdown import hbold
import datetime
import middleware
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from backend.databases.database import Database
import edutypes

WEEKDAYS = [
    'Понедельник',
    'Вторник',
    'Среда',
    'Четверг',
    'Пятница',
    'Суббота',
    'Воскресенье',
]

class HomeworkChoose(StatesGroup):
    homework = State()

async def homework_menu(message: types.Message):
    await message.answer("На какой день Вы хотите получить д/з?", reply_markup=keyboards.week())

async def homework(call: types.CallbackQuery):
    code = call.data[-1]
    if code.isdigit():
        code = int(code)
    id = call.from_user.id
    weekday = datetime.date.today().weekday()
    date = datetime.date.today()
    if code == weekday:
        hws = await middleware.homework(date, call.from_user.id)
    else:
        date = datetime.date.today() + datetime.timedelta(days=1)
        while date.weekday() != code:
            date += datetime.timedelta(days=1)
        hws = await middleware.homework(date + datetime.timedelta(days=7), call.from_user.id) #TODO EDIT BEFORE RELEASE

    
    await call.message.answer('Домашнее задание: '+WEEKDAYS[date.weekday()], reply_markup=keyboard_main())
    if hws == []:
        await call.message.answer('Домашнего задания на этот день ещё нет.', reply_markup=keyboard_main())
    await call.answer()
    for hw in hws:
        db = await Database.setup()
        is_done = await db.is_homework_done(hw, await db.get_student_by_id(id))
        await db.close_connection()
        await call.message.answer(hbold("Предмет: ")+hw.subject+hbold("\nЗадание: ")+hw.task, reply_markup=keyboards.is_done_checkbox(hw, is_done))
        for file in hw.files:
            if file['name'].split('.')[-1] == 'jpg':   
                await call.message.answer_photo(photo=file['file']['url'], )
            else:
                f = types.InputFile.from_url(file['file']['url'])
                await call.message.answer_document(id, f)

async def is_done_changed(call: types.CallbackQuery):
    hw_id = call.data.replace('isdone', '')
    hw = edutypes.Homework('','','','',hw_id)
    db = await Database.setup()
    is_done = await db.is_homework_done(hw, await db.get_student_by_id(call.from_user.id))
    is_done = not is_done
    await db.change_homework_done(hw, await db.get_student_by_id(call.from_user.id), is_done)
    await db.close_connection()
    await call.answer()
    await call.message.edit_reply_markup(reply_markup=keyboards.is_done_checkbox(hw, is_done))

async def setup(dp):
    print('Register homework handler...', end='')
    dp.register_message_handler(homework_menu, lambda message: message.text == "📚 Домашнее задание" or message.text == "/get_homework")
    dp.register_callback_query_handler(homework, lambda c: c.data and c.data.startswith('homework'))
    dp.register_callback_query_handler(is_done_changed, lambda c: c.data and c.data.startswith('isdone'))
    print('Succsess')


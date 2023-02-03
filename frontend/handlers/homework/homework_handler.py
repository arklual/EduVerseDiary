from . import keyboards
from frontend.keyboards import main as keyboard_main
from aiogram import types
from aiogram.utils.markdown import hbold
import datetime
import middleware

WEEKDAYS = [
    'Понедельник',
    'Вторник',
    'Среда',
    'Четверг',
    'Пятница',
    'Суббота',
    'Воскресенье',
]

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
        hws = await middleware.homework(date)
    else:
        date = datetime.date.today() + datetime.timedelta(days=1)
        while date.weekday() != code:
            date += datetime.timedelta(days=1)
        hws = await middleware.homework(date)

    
    await call.message.answer('Домашнее задание: '+WEEKDAYS[date.weekday()], reply_markup=keyboard_main())
    if hws == []:
        await call.message.answer('Домашнего задания на этот день ещё нет.', reply_markup=keyboard_main())
    for hw in hws:
        await call.message.answer(hbold("Предмет: ")+hw.subject+hbold("\nЗадание: ")+hw.task, reply_markup=keyboard_main())
        for file in hw.files:
            if file['name'].split('.')[-1] == 'jpg':   
                await call.message.answer_photo(photo=file['file']['url'], )
            else:
                f = types.InputFile.from_url(file['file']['url'])
                await call.message.answer_document(id, f)
    await call.answer()

async def setup(dp):
    print('Register homework handler...', end='')
    dp.register_message_handler(homework_menu, lambda message: message.text == "Домашнее задание" or message.text == "/get_homework")
    dp.register_callback_query_handler(homework, lambda c: c.data and c.data.startswith('homework'))
    print('Succsess')


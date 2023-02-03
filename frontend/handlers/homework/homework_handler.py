from . import keyboards
from frontend.keyboards import main as keyboard_main
from aiogram import types
from aiogram.utils.markdown import hbold
import datetime
import middleware

bot = None
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

async def homework(callback_query: types.CallbackQuery):
    code = callback_query.data[-1]
    if code.isdigit():
        code = int(code)
    id = callback_query.from_user.id
    weekday = datetime.date.today().weekday()
    date = datetime.date.today()
    if code == weekday:
        hws = await middleware.homework(date)
    else:
        date = datetime.date.today() + datetime.timedelta(days=1)
        while date.weekday() != code:
            date += datetime.timedelta(days=1)
        hws = await middleware.homework(date)

    
    await bot.send_message(id, 'Домашнее задание: '+WEEKDAYS[date.weekday()], reply_markup=keyboard_main())
    if hws == []:
        await bot.send_message(id, 'Домашнего задания на этот день ещё нет.', reply_markup=keyboard_main())
    for hw in hws:
        await bot.send_message(id, hbold("Предмет: ")+hw.subject+hbold("\nЗадание: ")+hw.task, reply_markup=keyboard_main())
        for file in hw.files:
            if file['name'].split('.')[-1] == 'jpg':   
                await bot.send_photo(id, photo=file['file']['url'], )
            else:
                f = types.InputFile.from_url(file['file']['url'])
                await bot.send_document(id, f)
    await bot.answer_callback_query(callback_query.id)

async def setup(dp, b):
    print('Register homework handler...', end='')
    dp.register_message_handler(homework_menu, lambda message: message.text == "Домашнее задание" or message.text == "/get_homework")
    dp.register_callback_query_handler(homework, lambda c: c.data and c.data.startswith('homework'))
    global bot
    bot = b
    print('Succsess')


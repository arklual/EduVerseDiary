from aiogram.utils.markdown import hbold
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import datetime
from frontend import keyboards
from aiogram.utils.exceptions import ChatNotFound
from backend.databases.database import Database


class Attantion(StatesGroup):
    message = State()

async def start(message: types.Message):
    db = await Database.setup()
    first_name = (await db.get_student_by_id(message.from_user.id)).first_name
    await db.close_connection()
    await message.answer(f'Привет, {first_name}. Ты уже прочитал описание и знаешь, чем я могу тебе помочь.\n' 
    + 'Если вдруг ты не прочитал описание, то я твой электронный дневник, но только в телеграмме и более крутой. \n\n ' +
    "📍 " + hbold(' Что я могу?') + '\n'+
    '🚩 Присылать твои оценки в данном триместре по запросу.\n' +
    '🚩 Присылать тебе новые оценки в тот момент, когда ты их получаешь.\n' + 
    '🚩 Отправлять тебе конспекты.\n' + 
    '🚩 Присылать тебе домашнее задание, хранить что ты уже сделал.\n' + 
    '🚩 Отправлять тебе расписание звонков на текущий день.\n\n' + 
    'С помощью меня ты сможешь понять, что у тебя получается лучше, а что хуже.\n\n'
    '🆘\nСправка: /help\nНовости, информация о проекте, голосования о новых функцих: https://t.me/eduverse_official', parse_mode='HTML', reply_markup=keyboards.main('685823428'==str(message.from_user.id))
    )

async def help(message: types.Message):
    await message.answer(
    """Вот команды, которые доступны нашему боту.
    /get_marks - узнать о твоих текущих оценках в этом триместре
    /get_schedule - узнать расписание звонков на текущий день
    /get_homework - узнать домашнее задание
    /get_notes - получить конспекты""", 
    reply_markup=keyboards.main('685823428'==str(message.from_user.id)))

async def attention(message: types.Message, state: FSMContext):
    await message.answer('Отправь текст объявления', reply_markup=keyboards.main('685823428'==str(message.from_user.id)))
    await state.set_state(Attantion.message.state)
    #TODO: option to choose students

async def send_attention(message: types.Message, state: FSMContext):
    await state.update_data(message=message.text)
    db = await Database.setup()
    students = await db.get_students()
    students = list(filter(lambda x: str(x.telegram_id) != str(message.from_user.id), students))
    await db.close_connection()
    not_sended_to = []
    for student in students:
        try:
            at = await message.bot.send_message(student.telegram_id, message.text, reply_markup=keyboards.main('685823428'==str(message.from_user.id)))
            await message.bot.pin_chat_message(message.chat.id, message_id=at.message_id)
        except ChatNotFound:
            not_sended_to.append(student.last_name)
            print('Unable to send: ', student.telegram_id, student.last_name)
    await state.finish()
    not_sended_to = str(not_sended_to).replace('[', '').replace(']', '').replace(', ', '\n').replace("'", "")
    if not_sended_to != []:
        await message.answer('Объявление разослано всему классу, кроме (у них нет чата с EduVerse Diary): ', reply_markup=keyboards.main('685823428'==str(message.from_user.id)))
        await message.answer(not_sended_to, reply_markup=keyboards.main('685823428'==str(message.from_user.id)))
    else:
        await message.answer('Объявление разослано всему классу.', reply_markup=keyboards.main('685823428'==str(message.from_user.id)))

async def schedule(message: types.Message):
    await message.answer("""Расписание звонков сегодня:""")
    if datetime.date.today().isoweekday() == 1 or datetime.date.today().isoweekday() == 6:
        await message.answer("1. 8.00-8.40\n2. 8.45-9.25\n3. 9.35-10.15\n4. 10.30-11.10\n5. 11.25-12.05\n6. 12.20-13.00\n7. 13.10-13.50", reply_markup=keyboards.main('685823428'==str(message.from_user.id)))
    elif datetime.date.today().isoweekday() != 7:
        await message.answer("1. 8.30-9.15\n2. 9.25-10.10\n3. 10.25-11.10\n4. 11.25-12.10\n5. 12.25-13.10\n6. 13.20-14.05\n7. 14.15-14.55", reply_markup=keyboards.main('685823428'==str(message.from_user.id)))

async def setup(dp):
    print('Register general handler...', end='')
    dp.register_message_handler(start, commands=['start'])
    dp.register_message_handler(help, commands=['help'])
    dp.register_message_handler(attention, commands=['attention'], state="*")
    dp.register_message_handler(send_attention,  state=Attantion.message)
    dp.register_message_handler(schedule, lambda message: message.text == "⏰ Расписание звонков" or message.text == "/get_schedule")
    print('Succsess')
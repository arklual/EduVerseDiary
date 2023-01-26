from aiogram.utils.markdown import hbold
from aiogram import types
import datetime


async def start(message: types.Message):
    await message.answer(f'Привет, {message.from_user.first_name}. Ты уже прочитал описание и знаешь, чем я могу тебе помочь.\n' 
    + 'Если вдруг ты не прочитал описание, то я твой электронный дневник, но только в телеграмме и более крутой. \n\n ' +
    "📍 " + hbold(' Что я могу?') + '\n'
    + '🚩 Присылать твои оценки в данном триместре по запросу (но актуальные, в отличие от официального дневника)' + '\n' +
    '🚩 Присылать тебе новые оценки в тот момент, когда ты их получаешь.\n' + 
    '🚩 Отправлять тебе конспекты.\n\n' + 
    '🚩 Присылать тебе домашнее задание.\n' + 
    '🚩 Отправлять тебе расписание звонков на текущий день.\n\n' + 
    'С помощью меня ты сможешь понять, что у тебя получается лучше,  а что хуже.\n\n'
    '🆘\nСправка: /help', parse_mode='HTML'
    )

async def help(message: types.Message):
    await message.answer("""Вот команды, которые доступны нашему боту.
    /get_marks - узнать о твоих текущих оценках в этом триместре
    /get_schedule - узнать расписание звонков на текущий день
    /get_homework - узнать домашнее задание
    /get_notes - получить конспекты""")

async def schedule(message: types.Message):
    await message.answer("""Расписание звонков сегодня:""")
    if datetime.date.today().isoweekday() == 1 or datetime.date.today().isoweekday() == 6:
        await message.answer("1. 8.00-8.40\n2. 8.45-9.25\n3. 9.35-10.15\n4. 10.30-11.10\n5. 11.25-12.05\n6. 12.20-13.00\n7. 13.10-13.50")
    elif datetime.date.today().isoweekday() != 7:
        await message.answer("1. 8.30-9.15\n2. 9.25-10.10\n3. 10.25-11.10\n4. 11.25-12.10\n5. 12.25-13.10\n6. 13.20-14.05\n7. 14.15-14.55")

async def setup(dp):
    dp.register_message_handler(start, commands=['start'])
    dp.register_message_handler(help, commands=['help'])
    dp.register_message_handler(schedule, lambda message: message.text == "Расписание звонков" or message.text == "/get_schedule")
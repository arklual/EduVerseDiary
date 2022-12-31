from api.settings import TELEGRAM_TOKEN, LAST_NAMES, WEEK_DAYS
from api.school33api import School33Api
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.utils.markdown import hbold, hunderline
import aioschedule
import asyncio
import copy
from collections import Counter
import datetime
from aiogram.utils.exceptions import ChatNotFound
import homeworks
from notes import get_notes

bot = Bot(token=TELEGRAM_TOKEN, parse_mode='HTML')
dp = Dispatcher(bot)
api = School33Api(skip_update_marks=False)

def round_number(num, cnt = 0):
    z = 1 if num > 0 else -1
    num *= z
    k = 10**cnt
    num *= k*10
    if num%10 >= 5:
        num = num + 10
    num = int(num/10)
    return num/k*z

def get_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_1 = types.KeyboardButton(text="Оценки")
    keyboard.add(button_1)
    button_2 = "Домашнее задание"
    keyboard.add(button_2)
    button_3 = "Расписание звонков"
    keyboard.add(button_3)
    button_4 = "Конспекты"
    keyboard.add(button_4)
    return keyboard

def prettify_marks(marks):
    marks = str(marks)
    marks = marks.replace('[', '')
    marks = marks.replace(']', '')
    marks = marks.replace('5', '5️⃣')
    marks = marks.replace('4', '4️⃣')
    marks = marks.replace('3', '3️⃣')
    marks = marks.replace('2', '2️⃣')
    marks = marks.replace('1', '1️⃣')
    marks = marks.replace(', ', '')
    return marks

@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.answer(f'Привет, {message.from_user.first_name}. Ты уже прочитал описание и знаешь, чем я могу тебе помочь.\n' 
    + 'Если вдруг ты не прочитал описание, то я твой электронный дневник, но только в телеграмме и более крутой. \n\n ' +
    "📍 " + hbold(' Что я могу?') + '\n'
    + '🚩 Присылать твои оценки в данном триместре по запросу (но актуальные, в отличие от официального дневника)' + '\n' +
    '🚩 Присылать тебе новые оценки в тот момент, когда ты их получаешь.\n' + 
    '🚩 Отправлять тебе конспекты.\n\n' + 
    '🚩 Присылать тебе домашнее задание.\n' + 
    '🚩 Отправлять тебе расписание звонков на текущий день.\n\n' + 
    'С помощью меня ты сможешь понять, что у тебя получается лучше,  а что хуже.\n\n'
    '🆘\nСправка: /help', parse_mode='HTML', reply_markup=get_keyboard()
    )

@dp.message_handler(commands=['help'])
async def help_user(message: types.Message):
    await message.answer("""Вот команды, которые доступны нашему боту.
    /get_marks - узнать о твоих текущих оценках в этом триместре
    /get_schedule - узнать расписание звонков на текущий день
    /get_homework - узнать домашнее задание
    /get_notes - получить конспекты""", reply_markup=get_keyboard())

@dp.message_handler(lambda message: message.text == "Оценки" or message.text == "/get_marks")
async def send_marks(message: types.Message):
    last_name = LAST_NAMES[str(message.from_id)]
    for st in api.students:
        if st.name.split(' ')[1] == last_name:
            await message.answer('Твои оценки:')
            for subject in st.subjects:
                if subject.marks != []:
                    marks = prettify_marks(subject.marks)
                    sign = ''
                    prediction = int(round_number(float(subject.average_mark)))
                    if prediction == 5:
                        sign = '🟢'
                    elif prediction == 4:
                        sign = '🔵'
                    elif prediction == 3:
                        sign = '🟡'
                    elif prediction == 2:
                        sign = '🔴'
                    await message.answer(f'{subject.name} {sign}{subject.average_mark} {marks}', reply_markup=get_keyboard())

@dp.message_handler(lambda message: message.text == "Расписание звонков" or message.text == "/get_schedule")
async def send_schedule(message: types.Message):
    await message.answer("""Расписание звонков сегодня:""")
    if datetime.date.today().isoweekday() == 1 or datetime.date.today().isoweekday() == 6:
        await message.answer("1. 8.00-8.40\n2. 8.45-9.25\n3. 9.35-10.15\n4. 10.30-11.10\n5. 11.25-12.05\n6. 12.20-13.00\n7. 13.10-13.50", reply_markup=get_keyboard())
    elif datetime.date.today().isoweekday() != 7:
        await message.answer("1. 8.30-9.15\n2. 9.25-10.10\n3. 10.25-11.10\n4. 11.25-12.10\n5. 12.25-13.10\n6. 13.20-14.05\n7. 14.15-14.55", reply_markup=get_keyboard())

@dp.message_handler(lambda message: message.text == "Конспекты" or message.text == "/get_notes")
async def send_notes(message: types.Message):
    buttons = []
    subjects = []
    notes = await get_notes()
    for note in notes:
        if note is None:
            continue
        subject = note['subject']
        if subject not in subjects:
            subjects.append(subject)
            buttons.append(types.InlineKeyboardButton(subject, callback_data=f'subject{subject}'))
    inline_kb1 = types.InlineKeyboardMarkup().add(*buttons)
    await message.answer("По какому предмету Вы хотите получить конспекты?", reply_markup=inline_kb1)

@dp.callback_query_handler(lambda c: c.data and c.data.startswith('subject'))
async def process_callback_notes(callback_query: types.CallbackQuery):
    subject = callback_query.data[7:]
    id = callback_query.from_user.id
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(id, f'Записи по предмету {subject}:', reply_markup=get_keyboard())
    notes = await get_notes()
    to_send = []
    for note in notes:
        if note is None:
            continue
        if subject == note['subject'] and note['is_new']:
            to_send += [note['files']]
    for n in to_send:
        media = types.MediaGroup()
        for file in n:
            media.attach_photo(file['file']['url'])
        await bot.send_media_group(id, media)     

@dp.message_handler(lambda message: message.text == "Домашнее задание" or message.text == "/get_homework")
async def send_homework(message: types.Message):
    isoweekday = datetime.date.today().isoweekday()
    buttons = []
    if isoweekday != 7:
        buttons.append(types.InlineKeyboardButton('Сегодня', callback_data=f'homework{isoweekday}'))
    if isoweekday == 6 or isoweekday == 7:
        for i in range(1, 7):
            buttons.append(types.InlineKeyboardButton(WEEK_DAYS[i], callback_data=f'homework{i}'))
    else:
        for i in range(isoweekday+1, 7):
            buttons.append(types.InlineKeyboardButton(WEEK_DAYS[i], callback_data=f'homework{i}'))
    inline_kb1 = types.InlineKeyboardMarkup().add(*buttons)
    await message.answer("На какой день Вы хотите получить д/з?", reply_markup=inline_kb1)

@dp.callback_query_handler(lambda c: c.data and c.data.startswith('homework'))
async def process_callback_homework(callback_query: types.CallbackQuery):
    code = callback_query.data[-1]
    if code.isdigit():
        code = int(code)
    id = callback_query.from_user.id
    isoweekday = datetime.date.today().isoweekday()
    await bot.answer_callback_query(callback_query.id)
    hws = []
    date = datetime.date.today()
    if code == isoweekday:
        hws = await homeworks.get_homework(datetime.date.today())
    else:
        date = datetime.date.today() + datetime.timedelta(days=1)
        while date.isoweekday() != code:
            date += datetime.timedelta(days=1)
        hws = await homeworks.get_homework(date)
    await bot.send_message(id, 'Домашнее задание: '+WEEK_DAYS[date.isoweekday()], reply_markup=get_keyboard())
    if hws == []:
        await bot.send_message(id, 'Домашнего задания на этот день ещё нет.', reply_markup=get_keyboard())
    for hw in hws:
        await bot.send_message(id, hbold("Предмет: ")+hw['subject']+hbold("\nЗадание: ")+hw['task'], reply_markup=get_keyboard())
        for file in hw['files']:
            if file['name'][-4:] == '.jpg':   
                await bot.send_photo(id, photo=file['file']['url'], )
            else:
                await bot.send_document(id, document=file['file']['url'])

async def send_if_new_marks():
    students = copy.deepcopy(api.students)
    await api.update_marks()
    for i in range(len(api.students)):
        if students[i].subjects != api.students[i].subjects:
            last_name = students[i].name.split(' ')[1]
            id = list(LAST_NAMES.keys())[list(LAST_NAMES.values()).index(last_name)]
            for j in range(len(students[i].subjects), len(api.students[i].subjects)):
                if api.students[i].subjects[j].marks != []:
                    try:
                        await bot.send_message(id, f"У тебя новые оценки по предмету {api.students[i].subjects[j].name}: {prettify_marks(api.students[i].subjects[j].marks)}")
                    except ChatNotFound:
                        print(f"Can't send to {id} {last_name}")
                        break
        for j in range(len(students[i].subjects)):
            if students[i].subjects[j].marks != api.students[i].subjects[j].marks:
                last_name = students[i].name.split(' ')[1]
                id = list(LAST_NAMES.keys())[list(LAST_NAMES.values()).index(last_name)]
                try:
                    res = list((Counter(api.students[i].subjects[j].marks) - Counter(students[i].subjects[j].marks)).elements())
                    if res != []:
                        await bot.send_message(id, f"У тебя новые оценки по предмету {api.students[i].subjects[j].name}: {prettify_marks(res)}")
                except ChatNotFound:
                    print(f"Can't send to {id} {last_name}")
                    break

async def scheduler():
    aioschedule.every(10).minutes.do(send_if_new_marks)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)

async def on_startup(_):
    asyncio.create_task(scheduler())

if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)

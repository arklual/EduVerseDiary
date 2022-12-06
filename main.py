from api.settings import TELEGRAM_TOKEN, LAST_NAMES
from api.school33api import School33Api
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.utils.markdown import hbold, hunderline
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import aioschedule
import asyncio
import copy

bot = Bot(token=TELEGRAM_TOKEN, parse_mode='HTML')
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
api = School33Api()
@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.answer(f'Привет, {message.from_user.first_name}. Ты уже прочитал описание и знаешь, чем я могу тебе помочь.\n' 
    + 'Если вдруг ты не прочитал описание, то я твой электронный дневник, но только в телеграмме и более крутой. \n\n ' +
    "📍 " + hbold(' Что я могу?') + '\n'
    + '🚩 К сожелению, пока только присылать твои оценки в данном триместре по запросу (но актуальные, в отличие от официального дневника)' + '\n' +
    '🚩 Но скоро я смогу присылать тебе новые оценки в тот момент, когда ты их получаешь и ' + hunderline('много чего ещё') + ' (пока сохраним это в интриге). ' + 
    'С помощью меня ты сможешь понять, что у тебя получается лучше,  а что хуже.\n\n'
    '🆘\nСправка: /help', parse_mode='HTML'
    )

@dp.message_handler(commands=['help'])
async def help_user(message: types.Message):
    await message.answer("""Вот команды, которые доступны нашему боту.
    /get_marks - узнать о твоих текущих оценках в этом триместре""")

@dp.message_handler(commands=['get_marks'])
async def send_marks(message: types.Message):
    last_name = LAST_NAMES[str(message.from_id)]
    await message.answer('Загружаем твои отметки, подождите (процесс может занять 1 минуту)')
    for st in api.students:
        if st.name.split(' ')[1] == last_name:
            await message.answer('Твои оценки:')
            for subject in st.subjects:
                if subject.marks != []:
                    await message.answer(f'{subject.name} {subject.average_mark} {subject.marks}')

async def send_if_new_marks():
    students = copy.deepcopy(api.students)
    api.update_marks()
    if students != api.students:
        for j in range(0, len(api.students[7].subjects)):
            if j >= len(students[7].subjects):
                await bot.send_message('685823428', f'Новый оценки по предмету {api.students[7].subjects[j].name}:', api.students[7].subjects[j].marks)
            elif len(api.students[7].subjects[j].marks) > len(students[7].subjects[j].marks):
                await bot.send_message('685823428', f'Новый оценки по предмету {api.students[7].subjects[j].name}:', api.students[7].subjects[j].marks[len(students[7].subjects[j].marks):len(api.students[7].subjects[j].marks)])

async def scheduler():
    aioschedule.every(2).minutes.do(send_if_new_marks)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)

async def on_startup(_):
    asyncio.create_task(scheduler())

if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)

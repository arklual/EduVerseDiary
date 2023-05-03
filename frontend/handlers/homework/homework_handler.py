from . import keyboards
from frontend.keyboards import main as keyboard_main
from aiogram import types, Dispatcher
from aiogram.utils.markdown import hbold
import datetime
import middleware
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from backend.databases.database import Database
from backend import homework_api
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

class AddHomework(StatesGroup):
    subject = State()
    task = State()
    

async def get_deadline_weekday(s):
    a = [
        [
            'Русский',
            'Литература',
            'История',
            'ОБЖ',
            'Английский'
        ],
        [
            'Физика',
            'Алгебра',
            'Информатика'
        ],
        [
            'Обществознание',
            'Литература',
            'Физика',
            'Английский',
            'Геометрия'
        ],
        [
            'Обществознание',
            'Биология',
            'Алгебра'
        ],
        [
            'Информатика',
            'Химия',
            'Английский',
            'Биология'
        ],
        [
            'Физика',
            'Литература',
            'Родной язык'
        ]
    ]
    n = datetime.date.today().weekday()
    for i in range(n+1, len(a)):
        if s in a[i]:
            for j in a[i]:
                if j == s:
                    return i

    for i in range(len(a)):
        if s in a[i]:
            for j in a[i]:
                if j == s:
                    return i

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
        hws = await middleware.homework(date, call.from_user.id)

    
    await call.message.answer('Домашнее задание: '+WEEKDAYS[date.weekday()], reply_markup=keyboard_main('685823428'==str(call.from_user.id)))
    if hws == []:
        await call.message.answer('Домашнего задания на этот день ещё нет.', reply_markup=keyboard_main('685823428'==str(call.from_user.id)))
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
    await call.answer()
    await call.message.edit_reply_markup(reply_markup=keyboards.is_done_checkbox(hw, is_done))
    await db.change_homework_done(hw, await db.get_student_by_id(call.from_user.id), is_done)
    await db.close_connection()

async def add_homework(message: types.Message, state: FSMContext):
    await message.answer('Выберите предмет', reply_markup=keyboards.add_subjects())
    await state.set_state(AddHomework.subject.state)

async def add_homework_subject_set(message: types.Message, state: FSMContext):
    await state.update_data(subject = message.text)
    await message.answer('Введите задание')
    await state.set_state(AddHomework.task.state)

async def add_homework_task_set(message: types.Message, state: FSMContext):
    await state.update_data(task = message.text)
    data = await state.get_data()
    await state.finish()
    code = await get_deadline_weekday(data['subject'])
    weekday = datetime.date.today().weekday() +1 
    date = datetime.date.today() + datetime.timedelta(days=1)
    if code == weekday:
        pass
    else:
        date = datetime.date.today() + datetime.timedelta(days=1)
        while date.weekday() != code:
            date += datetime.timedelta(days=1)
    data['deadline'] = str(date)
    await middleware.add_homework(data)
    await message.answer('Отправлено ✅', reply_markup=keyboard_main('685823428'==str(message.from_user.id)))

async def inline_homework(inline_query: types.InlineQuery):
    date = datetime.date.today() + datetime.timedelta(days=1)
    if date.isoweekday() == 7:
        date += datetime.timedelta(days=1) 
    hws = await homework_api.get_homework(date)
    result = [types.InlineQueryResultArticle(
        id=i,
        title=hw['subject'],
        description=hw['task'],
        input_message_content=types.InputTextMessageContent(
            message_text=f"<b>{hw['subject']}</b>\n{hw['task']}",
            parse_mode="HTML"
        )) for i, hw in enumerate(hws) if hw['files'] == []]
    result += [
        types.InlineQueryResultPhoto(
            id=i,
            title=f"{hw['subject']}",
            caption=f"<b>{hw['subject']}</b>\n{hw['task']}",
            thumb_url=hw['files'][0]['file']['url'],
            photo_url=hw['files'][0]['file']['url']
        ) for i, hw in enumerate(hws) if hw['files'] != []
    ]
    await inline_query.answer(result, switch_pm_text='Перейти в бота', switch_pm_parameter='go', cache_time=3600)

async def setup(dp: Dispatcher):
    print('Register homework handler...', end='')
    dp.register_message_handler(homework_menu, lambda message: message.text == "📚 Домашнее задание" or message.text == "/get_homework")
    dp.register_callback_query_handler(homework, lambda c: c.data and c.data.startswith('homework'))
    dp.register_callback_query_handler(is_done_changed, lambda c: c.data and c.data.startswith('isdone'))
    dp.register_message_handler(add_homework, lambda message: message.text == "/add_homework" or message.text == 'Загрузить д/з', state="*")
    dp.register_message_handler(add_homework_subject_set, state=AddHomework.subject)
    dp.register_message_handler(add_homework_task_set, state=AddHomework.task)
    dp.register_inline_handler(inline_homework)
    print('Succsess')


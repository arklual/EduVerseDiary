from backend import homework_api, notes_api, marks_api
from edutypes import Homework, Note, Mark
from backend.databases.database import Database
from collections import Counter
from aiogram.utils.exceptions import ChatNotFound
from aiogram import Bot
from backend.marks_api import update_marks
import middleware

def prettify_marks(marks):
    marks = str(marks)
    marks = marks.replace('5', '5️⃣')
    marks = marks.replace('4', '4️⃣')
    marks = marks.replace('3', '3️⃣')
    marks = marks.replace('2', '2️⃣')
    marks = marks.replace('1', '1️⃣')
    marks = marks.replace('+', '✝️')
    return marks

def round_number(num, cnt = 0):
    z = 1 if num > 0 else -1
    num *= z
    k = 10**cnt
    num *= k*10
    if num%10 >= 5:
        num = num + 10
    num = int(num/10)
    return num/k*z

async def homework(date, telegram_id):
    hws = []
    data = await homework_api.get_homework(date)
    db = await Database.setup()
    for hw in data:
        if not hw is None:
            hws.append(Homework(subject=hw['subject'], task=hw['task'], files=hw['files'], deadline=date, task_id=hw['id']))
            hw = hws[len(hws)-1]
            student = await db.get_student_by_id(telegram_id)
            if not await db.hw_exists(hw, student):
                await db.add_homework(hw, student)
            else:
                hws[len(hws)-1].is_done = await db.is_homework_done(hw, student)
    await db.close_connection()
    return hws

async def add_homework(data):
    await homework_api.send_homework(data['subject'], data['task'], data['deadline'])

async def notes():
    notes = []
    data = await notes_api.get_notes()
    for note in data:
        if not note is None:
            notes.append(Note(subject=note['subject'], files=note['files'], theme=note['theme'], date=note['date']))
    notes = sorted(notes, key=lambda x: x.date)
    return notes

async def get_themes_of_notes(subject):
    themes = []
    notes = await middleware.notes()
    for note in notes:
        if subject == note.subject:
            themes += [note.theme]
    return themes

async def marks(telegram_id):
    db = await Database.setup()
    student = await db.get_student_by_id(telegram_id)
    tmarks = await db.get_students_marks(student)
    await db.close_connection()
    messages = []
    tmarks = sorted(tmarks, key=lambda x: x.subject.id)
    last_subject = 0
    for mark in tmarks:
        if mark.subject.id != last_subject:
            messages.append(f'{mark.subject.name}: ')
            last_subject = mark.subject.id
        messages[len(messages)-1] += f'{mark.mark}'
    for i, message in enumerate(messages):
        messages[i] = prettify_marks(message)
        message = messages[i]
        marks_row = message.split(': ')[1]
        marks = []
        for mark in marks_row:
            if mark.isnumeric():
                marks.append(int(mark))
        average_mark = round(sum(marks)/len(marks), 3)
        sign = ''
        prediction = int(round_number(float(average_mark)))
        if prediction == 5:
            sign = '🟢'
        elif prediction == 4:
            sign = '🔵'
        elif prediction == 3:
            sign = '🟡'
        elif prediction == 2:
            sign = '🔴'
        average_mark = round(sum(marks)/len(marks), 2)
        messages[i] = message.split(': ')[0] + f' {sign}{average_mark}: ' + message.split(': ')[1]
    return messages

class Sender:
    def __init__(self, bot) -> None:
        self.bot = bot
    
    
    async def send_new_marks(self):
        db = await Database.setup()
        old_marks = []
        students = await db.get_students()
        for student in students:
            old_student_marks = await db.get_students_marks(student)
            old_marks += old_student_marks
        await db.close_connection()
        t_new_marks = await update_marks()
        new_marks = []
        for row in t_new_marks:
            new_marks += row
        new_marks = sorted(new_marks, key=lambda x: x.student.telegram_id)
        old_marks = sorted(old_marks, key=lambda x: x.student.telegram_id)
        if str(old_marks) == str(new_marks):
            print('Marks aren\'t changed')
        else:
            print('Marks are changed')
            for mark in old_marks:
                try:
                    new_marks.remove(mark)
                except:
                    pass
            for mark in new_marks:
                try:
                    await self.bot.send_message(mark.student.telegram_id, f"У тебя новая отметка по предмету {mark.subject.name}: {prettify_marks(mark.mark)}")
                except ChatNotFound:
                    print(f"Can't send to {mark.student.telegram_id} {mark.student.last_name}")
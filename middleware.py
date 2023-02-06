from backend import homework_api, notes_api
from edutypes.homework import Homework
from edutypes.notes import Note
from backend.databases.database import Database
import middleware

async def marks():
    pass

async def homework(date):
    hws = []
    data = await homework_api.get_homework(date)
    for hw in data:
        hws.append(Homework(subject=hw['subject'], task=hw['task'], files=hw['files'], deadline=date))
    return hws

async def notes():
    notes = []
    data = await notes_api.get_notes()
    for note in data:
        if not note is None and note['is_new']:
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
    marks = await db.get_students_marks(student)
    await db.close_db()
    return marks
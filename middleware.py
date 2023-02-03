from backend import homework_api, notes_api
from edutypes.homework import Homework
from edutypes.notes import Note

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
            notes.append(Note(subject=note['subject'], files=note['files']))
    return notes
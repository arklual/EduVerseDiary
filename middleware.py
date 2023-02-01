from backend import homework_api
from edutypes.homework import Homework

async def marks():
    pass

async def homework(date):
    hws = []
    data = await homework_api.get_homework(date)
    for hw in data:
        hws.append(Homework(subject=hw['subject'], task=hw['task'], files=hw['files'], deadline=date))
    return hws

async def notes():
    pass
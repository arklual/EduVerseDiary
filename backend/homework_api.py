import aiohttp
import datetime
import json
from backend.databases.database import Database

database_id = '8b2cb4fdac3044f09ae3187392132482'

hash = {}

async def get_homework(date):
    if hash.get(date.isoformat()) is not None:
        return hash.get(date.isoformat())
    db = await Database.setup()
    token = await db.get_notion_token()
    await db.close_connection()
    url = f'https://api.notion.com/v1/databases/{database_id}/query'
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers={
            "Authorization": f"Bearer {token}",
            "Notion-Version": "2021-08-16"
        }) as r:
            result_dict = await r.json()
            homework_list_result = result_dict['results']
            if date.isoweekday() == 7:
                date += datetime.timedelta(days=1)
            homeworks = []
            for homework in homework_list_result:
                homework_dict = await map_notion_result_to_homework(homework)
                if homework_dict['deadline'] == str(date):
                    homeworks.append(homework_dict)
            hash[date.isoformat()] = homeworks
            return homeworks


async def map_notion_result_to_homework(result):
    properties = result['properties']
    subject = properties['Предмет']['multi_select'][0]['name']
    task = properties['Задание']['title'][0]['text']['content']
    deadline = properties['Deadline']['date']['start']
    files = properties['Приложения']['files']
    id = result['id']
    return {
        'subject': subject,
        'task': task,
        'deadline': deadline,
        'files': files,
        'id': id
    }

async def send_homework(subject, task, deadline):
    db = await Database.setup()
    token = await db.get_notion_token()
    await db.close_connection()
    async with aiohttp.ClientSession() as session:
        await session.post(
            'https://api.notion.com/v1/pages', 
            headers ={
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json',
                'Notion-Version': '2022-06-28'
            },
            data=json.dumps({
                'parent': { "type": "database_id", "database_id": database_id },
                'properties' : {
                "Предмет": {
                    "type": "multi_select",
                    "multi_select": [{"name": subject}]
                },
                "Задание": {
                    "type": "title",
                    "title": [{"text": {"content": task}}]
                },
                "Deadline": {
                    "type": "date",
                    "date": { "start": deadline }
                }
                }
            }
        )
)

async def update_hash():
    global hash
    hash = {}
    date = datetime.date.today()
    for i in range(8):
        hash[date.isoformat()] = await get_homework(date)
        date += datetime.timedelta(days=1)
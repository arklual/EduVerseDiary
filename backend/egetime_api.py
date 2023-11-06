import aiohttp
import datetime
import json
from backend.databases.database import Database

database_id = '73dcd75c58da413ca6e29ffd0a84b9e9'


async def get_egetime(date):
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
            egetime_list_result = result_dict['results']
            egetimes = []
            for egetime in egetime_list_result:
                egetime_dict = await map_notion_result_to_egetime(egetime)
                if egetime_dict['date'] == str(date):
                    egetimes.append(egetime_dict)
            return egetimes


async def map_notion_result_to_egetime(result):
    properties = result['properties']
    task = properties['Task']['rich_text'][0]['text']['content']
    is_test = properties['Is test']['checkbox']
    date = properties['Date']['date']['start']
    photo = properties['Photo']['files']
    try:
        answers =[
            properties['Answer 1']['rich_text'][0]['text']['content'],
            properties['Answer 2']['rich_text'][0]['text']['content'],
            properties['Answer 3']['rich_text'][0]['text']['content'],
            properties['Answer 4']['rich_text'][0]['text']['content'],
            properties['Answer 5']['rich_text'][0]['text']['content'],
            properties['Answer 6']['rich_text'][0]['text']['content'],
        ]
    except:
        answers = []
    return {
        'task': task,
        'date': date,
        'photo': photo,
        'is_test': is_test,
        'answers': answers,
        'id': id
    }
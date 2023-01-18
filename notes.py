import aiohttp
import asyncio

token = 'secret_TObnT0Zb9Qb55PHwIdymijzdmNrFJCZnal3hwYYBuoc'
database_id = 'ae3b7c2c64084722a2a903eb84c16d5c'

async def get_notes():
    url = f'https://api.notion.com/v1/databases/{database_id}/query'
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers={
            "Authorization": f"Bearer {token}",
            "Notion-Version": "2021-08-16"
        }) as r:
            result_dict = await r.json()
            note_list_result = result_dict['results']
            notes = []
            for note in note_list_result:
                note_dict = await map_notion_result_to_note(note)
                notes.append(note_dict)
            return notes


async def map_notion_result_to_note(result):
    properties = result['properties']
    subject = properties['Предмет']['multi_select'][0]['name']
    date = properties['Дата конспекта']['date']['start']
    files = properties['Конспект']['files']
    is_new = properties['Новая тема?']['checkbox']
    theme = properties['Тема']['title'][0]['plain_text']
    return {
        'subject': subject,
        'date': date,
        'is_new': is_new,
        'files': files,
        'theme': theme,
    }
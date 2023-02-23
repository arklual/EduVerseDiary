import aiohttp
from backend.databases.database import Database

database_id = 'ae3b7c2c64084722a2a903eb84c16d5c'

async def get_notes():
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
            note_list_result = result_dict['results']
            notes = []
            for note in note_list_result:
                note_dict = await map_notion_result_to_note(note)
                notes.append(notes.append(note_dict))
            return notes


async def map_notion_result_to_note(result):
    properties = result['properties']
    subject = properties['Предмет']['multi_select'][0]['name']
    theme = properties['Тема']['title'][0]['text']['content']
    date = properties['Дата конспекта']['date']['start']
    files = properties['Конспект']['files']
    is_new = properties['Новая тема?']['checkbox']
    return {
        'subject': subject,
        'theme': theme,
        'date': date,
        'files': files,
    }
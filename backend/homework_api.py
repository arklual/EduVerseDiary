import aiohttp
import datetime

token = 'secret_TObnT0Zb9Qb55PHwIdymijzdmNrFJCZnal3hwYYBuoc'
database_id = '8b2cb4fdac3044f09ae3187392132482'


async def get_homework(date):
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
            return homeworks


async def map_notion_result_to_homework(result):
    properties = result['properties']
    subject = properties['Предмет']['multi_select'][0]['name']
    task = properties['Задание']['title'][0]['text']['content']
    deadline = properties['Deadline']['date']['start']
    files = result['properties']['Приложения']['files']
    return {
        'subject': subject,
        'task': task,
        'deadline': deadline,
        'files': files
    }

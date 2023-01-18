import aiohttp
import asyncio

token = 'secret_TObnT0Zb9Qb55PHwIdymijzdmNrFJCZnal3hwYYBuoc'
database_id = '8d115f1e8a824a5583fc4ba8926feea2'

async def get_training():
    url = f'https://api.notion.com/v1/databases/{database_id}/query'
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers={
            "Authorization": f"Bearer {token}",
            "Notion-Version": "2021-08-16"
        }) as r:
            result_dict = await r.json()
            training_list_result = result_dict['results']
            trainings = []
            for t in training_list_result:
                t_dict = await map_notion_result_to_training(t)
                trainings.append(t_dict)
            return trainings


async def map_notion_result_to_training(result):
    properties = result['properties']
    task = properties['Цепочка']['files']
    solution = properties['Решение']['files']
    return {
        'task': task,
        'solution': solution,
    }
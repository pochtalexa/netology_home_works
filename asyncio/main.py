import psycopg2
import aiohttp
import asyncio
from pprint import pprint
from more_itertools import chunked
import models
from models import Session, engine, Base, People

BASE_URL = 'https://swapi.dev/api/'


async def make_request(resource):
    async with aiohttp.ClientSession() as session:
        async with session.get(f'{BASE_URL}{resource}/') as response:
            result = await response.json()
            status_code = response.status

    return status_code, result


async def get_resources_count(resource):
    status_code, result = await make_request(resource)
    resources_count = result.get('count')

    return resources_count


async def cook_data_for_db(data, ind):
    people = models.People(
        id=ind,
        birth_year=data.get('birth_year'),
        eye_color=data.get('eye_color'),
        films=','.join(data.get('films')),
        gender=data.get('gender'),
        hair_color=data.get('hair_color'),
        height=data.get('height'),
        homeworld=data.get('homeworld'),
        mass=data.get('mass'),
        name=data.get('name'),
        skin_color=data.get('skin_color'),
        species=','.join(data.get('species')),
        starships=','.join(data.get('starships')),
        vehicles=','.join(data.get('vehicles'))
    )

    return people


async def save_resource(resource, resource_index):
    status_code, result = await make_request(f'{resource}/{resource_index}/')

    if status_code != 200:
        return False

    print(resource_index)
    pprint(result)
    print()

    data_db = await cook_data_for_db(result, resource_index)
    session = Session()
    session.add(data_db)
    session.commit()
    session.close()

    return True


async def main():
    Base.metadata.drop_all(bind=engine, tables=[People.__table__])
    models.create_tables()
    resources_count = await get_resources_count('people')
    resources_indexes = range(1, resources_count + 2)
    for resources_indexes_chunk in chunked(resources_indexes, 15):
        save_resource_tasks = [asyncio.create_task(save_resource('people', ind)) for ind in resources_indexes_chunk]
        await asyncio.gather(*save_resource_tasks)


if __name__ == '__main__':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())

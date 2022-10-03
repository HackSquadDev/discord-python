import aiohttp
from typing import Dict
from wrappers.api_thingies import hacksquad_endpoint

async def leaderboard_wrapper() -> Dict:
    async with aiohttp.ClientSession() as session:
        async with session.get(f'{hacksquad_endpoint}api/leaderboard') as resp:
            if resp.status == 200:
                data = await resp.json()
                return data['teams']
            else:
                raise Exception('Error fetching data from the API')

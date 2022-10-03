import aiohttp


async def leaderboard_wrapper():
    async with aiohttp.ClientSession() as session:
        async with session.get('https://www.hacksquad.dev/api/leaderboard') as resp:
            if resp.status == 200:
                data = await resp.json()
                return data['teams']
            else:
                raise Exception('Error fetching data from the API')

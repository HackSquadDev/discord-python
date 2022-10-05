import asyncio

import aiohttp


class ResponseError(Exception):
    """Something went wrong with the response"""

    pass


async def get_leaderboard():
    async with aiohttp.ClientSession() as session:
        async with session.get("https://www.hacksquad.dev/api/leaderboard") as response:
            if response.status == 200:
                response = await response.json()
                return response.get("teams")
            else:
                raise ResponseError


async def get_team(slug):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://www.hacksquad.dev/api/team/?id={slug}") as response:
            if response.status == 200:
                response = await response.json()
                return response.get("team")
            else:
                raise ResponseError


async def get_contributors():
    async with aiohttp.ClientSession() as session:
        async with session.get("https://contributors.novu.co/contributors") as response:
            if response.status == 200:
                response = await response.json()
                return response.get("list")
            else:
                raise ResponseError


async def get_contributors_mini():
    # I do not think that we would get much of a performance benefit from this but leaving it here all the same
    async with aiohttp.ClientSession() as session:
        async with session.get("https://contributors.novu.co/contributors-mini") as response:
            if response.status == 200:
                response = await response.json()
                return response.get("list")
            else:
                raise ResponseError

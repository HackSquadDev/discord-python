import aiohttp
import asyncio
import json

async def teams():
    async with aiohttp.ClientSession() as session:
        async with session.get('https://www.hacksquad.dev/api/leaderboard') as response:
            if response.status == 200:
                response = await response.text()
                response = json.loads(response)
                teams = response.get("teams")
                return teams

            else:
                return None

async def team(slug):
    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://www.hacksquad.dev/api/team/?id={slug}') as response:
            if response.status == 200:
                response = await response.text()
                response = json.loads(response)
                team = response.get("team")
                return team

            else:
                return None
import aiohttp
import asyncio
import json
from discord import Interaction, Embed
from discord.ext.paginator import paginator

async def get_leaderboard():
    async with aiohttp.ClientSession() as session:
        async with session.get('https://www.hacksquad.dev/api/leaderboard') as response:
            if response.status == 200:
                response = await response.text()
                response = json.loads(response)
                teams = response.get("teams")
                return teams

            else:
                return None

async def get_team(slug):
    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://www.hacksquad.dev/api/team/?id={slug}') as response:
            if response.status == 200:
                response = await response.text()
                response = json.loads(response)
                team = response.get("team")
                return team

            else:
                return None

async def get_contributors():
    async with aiohttp.ClientSession() as session:
        async with session.get('https://contributors.novu.co/contributors') as response:
            if response.status == 200:
                response = await response.text()
                response = json.loads(response)
                contributors = response.get("list")
                return contributors

            else:
                return None

async def get_contributors_mini():
    # I do not think that we would get much of a performance benefit from this but leaving it here all the same
    async with aiohttp.ClientSession() as session:
        async with session.get('https://contributors.novu.co/contributors-mini') as response:
            if response.status == 200:
                response = await response.text()
                response = json.loads(response)
                contributors = response.get("list")
                return contributors

            else:
                return None

class MyPaginator(paginator.Paginator):
    async def get_page_count(self, interaction: Interaction) -> int:
        return len(self.client.guilds)
    
    async def get_page_content(self, interaction: Interaction, page: int):
        guild = self.client.guilds[page]
        return {
            "embed": Embed(
                title=guild.name,
                description=f"This guild has {guild.member_count} members."
            ),
            "ephemeral": True
        }

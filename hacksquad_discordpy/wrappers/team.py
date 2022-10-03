import aiohttp
from objects.Team import Team
from objects.User import User


async def team_wrapper(slug: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://www.hacksquad.dev/api/team?id={slug.strip()}') as resp:
            if resp.status == 200:
                data = await resp.json()
                data = data['team']
                users = []
                for user in data['users']:
                    users.append(vars(User(user.get('id'), user.get('name'), user.get('email'), user.get('emailVerified'), user.get('image'), user.get(
                        'moderator'), user.get('handle'), user.get('teamId'), user.get('disqualified'), user.get('github_user_id'))))

                return Team(data.get('id'), data.get('name'), data.get('slug'), data.get('score'), data.get('owner_id'), data.get('prs'), data.get('github_team_id'), data.get('allow_auto_assign'), data.get('disqualified'), users)
            elif resp.status == 500:
                raise ValueError('Team not found')
            else:
                raise Exception('Error fetching data from the API')

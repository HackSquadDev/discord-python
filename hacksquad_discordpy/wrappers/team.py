import aiohttp
from objects.Team import Team
from objects.User import User
from wrappers.api_thingies import hacksquad_endpoint

async def team_wrapper(slug: str) -> Team:
    async with aiohttp.ClientSession() as session:
        async with session.get(f'{hacksquad_endpoint}team?id={slug.strip()}') as resp:
            if resp.status == 200:
                data = await resp.json()
                data = data['team']
                users = []
                for user in data['users']:
                    usery: User = {"id": user['id'], "name": user['name'], "email": user['email'], "email_verified": user['emailVerified'], "image": user['image'], "moderator": user['moderator'], "handle": user['handle'], "team_id": user['teamId'], "disqualified": user['disqualified'], "github_user_id": user['githubUserId']}
                    users.append(usery)
                return {"id": data['id'], "name": data['name'], "slug": data['slug'], "score": data['score'], "owner_id": data['ownerId'], "prs": data['prs'], "github_team_id": data['githubTeamId'], "allow_auto_assign": data['allowAutoAssign'], "disqualified": data['disqualified'], "users": users}
            elif resp.status == 500:
                raise ValueError('Team not found')
            else:
                raise Exception('Error fetching data from the API')

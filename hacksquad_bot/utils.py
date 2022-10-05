from datetime import datetime
from typing import Any, List, Optional, TypedDict, Dict
import aiohttp


class ResponseError(Exception):
    """Something went wrong with the response"""

    pass


class User(TypedDict):
    id: str
    "Unique ID of the user"

    name: str
    "The name of the user"

    email: str
    "The email of the user"

    email_verified: bool
    "If the user's email has been verified"

    image: str
    "An URL to the user's GitHub's image"

    moderator: bool
    "If the user is a moderator of the event"

    handle: str
    "The GitHub handle/name"

    team_id: str
    "ID of team the user has joined"

    disqualified: bool
    "If the user has been disqualified during the event"

    github_user_id: Optional[Any]
    "An unknown value"


class PartialTeam(TypedDict):
    id: str
    "The team's unique ID"

    name: str
    "The team's name"

    score: int
    "The team's score/total PRs"

    slug: str
    "The unique slug of the team"


class PR(TypedDict):
    id: str
    "ID of pull request in HackSquad"

    created_at: datetime
    "When the PR has been created"

    title: str
    "The PR's title"

    url: str
    "The PR's URL"


class Team(PartialTeam):
    owner_id: str
    "The ID of the owner of the team"

    owner: Optional[User]
    "The owner, as a User object. Can be optional."

    prs: List[PR]
    "The PRs realized by the team"

    github_team_id: Optional[Any]
    "An unknown value"

    allow_auto_assign: bool
    "If the team allows auto assignement of members"

    disqualified: bool
    "If the team has been disqualified during the event"


leaderboard: Dict[PartialTeam, datetime] = {}
team: Dict[Team, datetime] = {}
contributors: Dict[List[str], datetime] = {}
contributors_mini: Dict[List[str], datetime] = {}


async def gen_leaderboard_cache():
    now = datetime.now()
    lb = await fetch_leaderboard()
    global leaderboard
    leaderboard = [lb, now]


async def update_leaderboard_cache():
    if leaderboard:
        if datetime.datetime.now() - leaderboard[1] > datetime.timedelta(minutes=30):
            await gen_leaderboard_cache()
    else:
        await gen_leaderboard_cache()


async def fetch_leaderboard() -> List[PartialTeam]:
    async with aiohttp.ClientSession() as session:
        async with session.get("https://www.hacksquad.dev/api/leaderboard") as response:
            if response.status != 200:
                raise ResponseError()
            response = await response.json()
    return [
        PartialTeam(id=info["id"], name=info["name"], score=info["score"], slug=info["slug"])
        for info in response["teams"]
    ]


async def get_leaderboard() -> List[PartialTeam]:
    await update_leaderboard_cache()
    return leaderboard[0]


async def gen_team_cache(slug: str):
    now = datetime.now()
    t = await fetch_team(slug)
    global team
    team = [t, now]


async def update_team_cache(slug: str):
    if slug in team:
        if datetime.datetime.now() - team[slug][1] > datetime.timedelta(minutes=30):
            await gen_team_cache(slug)
    else:
        await gen_team_cache(slug)


async def fetch_team(slug: str) -> Team:
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://www.hacksquad.dev/api/team/?id={slug}") as response:
            if response.status != 200:
                raise ResponseError()
            response = await response.json()
    info = response["team"]

    owner = None
    for user in info["users"]:
        if user["id"] == info["ownerId"]:
            owner = User(
                id=user["id"],
                name=user["name"],
                email=user["email"],
                email_verified=user["emailVerified"],
                image=user["image"],
                moderator=user["moderator"],
                handle=user["handle"],
                team_id=user["teamId"],
                disqualified=user["disqualified"],
                github_user_id=user["githubUserId"],
            )

    prs = [
        PR(
            id=pr["id"],
            created_at=datetime.fromisoformat(pr["createdAt"]),
            title=pr["title"],
            url=pr["url"],
        )
        for pr in info["prs"]
    ]

    return Team(
        id=info["id"],
        name=info["name"],
        score=info["score"],
        slug=info["slug"],
        owner_id=info["ownerId"],
        owner=owner,
        prs=prs,
        github_team_id=info["githubTeamId"],
        allow_auto_assign=info["allowAutoAssign"],
        disqualified=info["disqualified"],
    )


async def get_team(slug: str) -> Team:
    await update_team_cache(slug)
    return team[slug][0]


async def gen_contributors_cache():
    now = datetime.now()
    contrib = await fetch_contributors()
    global contributors
    contributors = [contrib, now]


async def update_contributors_cache():
    if contributors:
        if datetime.datetime.now() - contributors[1] > datetime.timedelta(minutes=30):
            await gen_contributors_cache()
    else:
        await gen_contributors_cache()


async def fetch_contributors():
    async with aiohttp.ClientSession() as session:
        async with session.get("https://contributors.novu.co/contributors") as response:
            if response.status != 200:
                raise ResponseError()
            response = await response.json()
    return response["list"]


async def get_contributors():
    await update_contributors_cache()
    return contributors[0]


async def gen_contributors_mini_cache():
    now = datetime.now()
    contrib = await fetch_contributors_mini()
    global contributors_mini
    contributors_mini = [contrib, now]


async def update_contributors_mini_cache():
    if contributors_mini:
        if datetime.datetime.now() - contributors_mini[1] > datetime.timedelta(minutes=30):
            await gen_contributors_mini_cache()
    else:
        await gen_contributors_mini_cache()


async def fetch_contributors_mini():
    # I do not think that we would get much of a performance benefit from this but leaving it here all the same
    async with aiohttp.ClientSession() as session:
        async with session.get("https://contributors.novu.co/contributors-mini") as response:
            if response.status != 200:
                raise ResponseError()
            response = await response.json()
    return response["list"]


async def get_contributors_mini():
    await update_contributors_mini_cache()
    return contributors_mini[0]

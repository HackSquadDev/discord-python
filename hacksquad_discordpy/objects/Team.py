from typing import List, TypedDict

from objects.User import User


class Team(TypedDict):
    id: str
    name: str
    slug: str
    score: int
    owner_id: str
    prs: str
    github_team_id: None
    allow_auto_assign: bool
    disqualified: bool
    users: List[User]
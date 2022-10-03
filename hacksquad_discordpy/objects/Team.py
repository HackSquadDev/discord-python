from typing import List
from objects.User import User

class Team:
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

    def __init__(self, id: str, name: str, slug: str, score: int, owner_id: str, prs: str, github_team_id: None, allow_auto_assign: bool, disqualified: bool, users: List[User]) -> None:
        self.id = id
        self.name = name
        self.slug = slug
        self.score = score
        self.owner_id = owner_id
        self.prs = prs
        self.github_team_id = github_team_id
        self.allow_auto_assign = allow_auto_assign
        self.disqualified = disqualified
        self.users = users

    def __repr__(self) -> str:
        return f'{self.name} - {self.slug}'
    
    def __str__(self) -> str:
        return self.__repr__()
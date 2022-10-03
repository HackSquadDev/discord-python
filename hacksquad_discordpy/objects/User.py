from  typing import TypedDict

class User(TypedDict):
    id: str
    name: str
    email: str
    email_verified: None
    image: str
    moderator: bool
    handle: str
    team_id: str
    disqualified: bool
    github_user_id: None

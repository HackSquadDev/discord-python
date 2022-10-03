class User:
    id: str
    name: str
    email: str
    emailVerified: None
    image: str
    moderator: bool
    handle: str
    teamId: str
    disqualified: bool
    github_user_id: None

    def __init__(self, id: str, name: str, email: str, email_verified: None, image: str, moderator: bool, handle: str, team_id: str, disqualified: bool, github_user_id: None) -> None:
        self.id = id
        self.name = name
        self.email = email
        self.email_verified = email_verified
        self.image = image
        self.moderator = moderator
        self.handle = handle
        self.team_id = team_id
        self.disqualified = disqualified
        self.github_user_id = github_user_id

    def __repr__(self) -> str:
        return f'{self.name} - {self.handle}'

    def __str__(self) -> str:
        return self.__repr__()
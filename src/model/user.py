from typing import List


class User:
    email: str = None
    id: int = None
    name: str = None
    permissions: List[int] = None

    def __init__(self, _id, name, email, permissions):
        self.id = _id
        self.name = name
        self.email = email
        self.permissions = permissions

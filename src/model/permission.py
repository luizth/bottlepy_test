class Permission:
    description: str = None
    id: int = None
    name: str = None

    def __init__(self, _id, name, description):
        self.id = _id
        self.name = name
        self.description = description

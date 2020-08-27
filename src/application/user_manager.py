from typing import List, Optional

from src.env import U_DATA_PATH
from src.model.user import User
from src.utils.json_utils import read_json, write_json


def get_many() -> List[User]:
    users = __load_users()

    output = []
    for key, value in users.items():
        user = get_one(key)
        output.append(user)

    return output


def get_one(_id) -> Optional[User]:
    users = __load_users()
    if _id not in users:
        return None

    return User( _id=_id, name=users[_id]['name'], email=users[_id]['email'], permissions=users[_id]['permissions'] )


def insert(user: User) -> int:
    users = __load_users()

    _id = __generate_user_id()
    users[ str(_id) ] = { 'name': user.name, 'email': user.email, 'permissions': user.permissions }

    __dump_users(users)
    return _id


def remove(_id) -> Optional[int]:
    users = __load_users()
    if _id not in users:
        return None

    del users[_id]

    __dump_users(users)
    return _id


def update(_id, user: User) -> Optional[int]:
    users = __load_users()
    if _id not in users:
        return None

    users[_id]['name'] = user.name
    users[_id]['email'] = user.email

    __dump_users(users)
    return _id


def get_permissions(_id) -> Optional[List[int]]:
    users = __load_users()
    if _id not in users:
        return None

    return users[ str(_id) ]['permissions']


def update_permissions(_id, permissions: List[int]) -> Optional[int]:
    users = __load_users()
    if _id not in users:
        return None

    users[_id]['permissions'] = permissions

    __dump_users(users)
    return _id


def __load_users() -> Optional[dict]:
    return read_json(U_DATA_PATH)


def __dump_users(users):
    write_json(U_DATA_PATH, users)


def __generate_user_id():
    users = __load_users()

    return int( max(users) ) + 1

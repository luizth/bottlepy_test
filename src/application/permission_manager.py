from typing import List, Optional

from src.env import P_DATA_PATH
from src.model.permission import Permission
from src.utils.json_utils import read_json, write_json


def get_many() -> List[Permission]:
    permissions = __load_permissions()

    output: List[Permission] = []
    for key, value in permissions.items():
        permission = Permission( _id=key, name=value['name'], description=value['description'] )
        output.append(permission)

    return output


def get_one(_id) -> Optional[Permission]:
    permissions = __load_permissions()
    if _id not in permissions:
        return None

    return Permission( _id=_id, name=permissions[_id]['name'], description=permissions[_id]['description'] )


def insert(permission: Permission) -> Optional[int]:
    permissions = __load_permissions()

    _id = __generate_permission_id()
    permissions[ str(_id) ] = { 'name': permission.name, 'description': permission.description }

    __dump_permissions(permissions)
    return _id


def remove(_id) -> Optional[int]:
    permissions = __load_permissions()
    if _id not in permissions:
        return None

    del permissions[_id]

    __dump_permissions(permissions)
    return _id


def update(_id, permission: Permission) -> Optional[int]:
    permissions = __load_permissions()
    if _id not in permissions:
        return None

    permissions[_id]['name'] = permission.name
    permissions[_id]['description'] = permission.description

    __dump_permissions(permissions)
    return _id


def __load_permissions():
    return read_json(P_DATA_PATH)


def __dump_permissions(permissions):
    write_json(P_DATA_PATH, permissions)


def __generate_permission_id():
    permissions = __load_permissions()

    return int( max(permissions) ) + 1

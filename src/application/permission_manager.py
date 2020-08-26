import os
import json
from typing import List, Optional

from src.env import ROOT_PATH, P_DATA_PATH
from src.model.permission import Permission
from src.utils.http_utils import response_bad_request  # Remover métodos do cliente/servidor


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


def insert(permission: Permission) -> int:
    permissions = __load_permissions()

    _id = __generate_permission_id()
    permissions[ str(_id) ] = { 'name': permission.name, 'description': permission.description }

    __dump_permissions(permissions)
    return _id


def __load_permissions():
    try:
        with open(os.path.normpath(os.path.join(ROOT_PATH, P_DATA_PATH))) as f:
            permissions = json.load(f)
            return permissions
    except Exception:
        return {}


def __dump_permissions(permissions):
    try:
        with open(os.path.normpath(os.path.join(ROOT_PATH, P_DATA_PATH))) as f:
            json.dump(permissions, f)
    except Exception:
        pass


def __generate_permission_id():
    permissions = __load_permissions()

    return int( max(permissions)) + 1

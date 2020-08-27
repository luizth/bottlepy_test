from typing import List

from bottle import request

from src.application import permission_manager
from src.exceptions.attribute_not_found import AttributeNotFound
from src.model.permission import Permission
from src.utils.http_utils import response_ok, response_bad_request, response_not_found, response_internal_server_error
from src.utils.json_utils import instance_to_dict
from src.utils.validation_utils import require_attrs, require_dict


def get_many():
    permissions: List[Permission] = permission_manager.get_many()
    output: List[dict] = [instance_to_dict(permission) for permission in permissions]

    return response_ok(output)


def get_one(_id):
    permission: Permission = permission_manager.get_one(_id)

    if permission is None:
        return response_not_found()

    output: dict = instance_to_dict(permission)
    return response_ok(output)


def insert():
    data: dict = request.json

    try:
        require_dict(data)
        permission: Permission = __create_permission(data)
        _id: int = permission_manager.insert(permission)
        return response_ok({ 'id': _id })
    except (NotADirectoryError, AttributeNotFound):
        return response_bad_request()
    except Exception:
        return response_internal_server_error()


def remove(_id):
    deleted_id = permission_manager.remove(_id)

    if deleted_id is None:
        return response_bad_request()

    return response_ok({ 'id': deleted_id })


def update(_id):
    permission: Permission = permission_manager.get_one(_id)

    if permission is None:
        return response_not_found()

    data: dict = request.json

    try:
        require_dict(data)
        permission = __update_permission(permission, data)
        permission_id = permission_manager.update(_id, permission)
        return response_ok({ 'id': permission_id })
    except (NotADirectoryError, AttributeNotFound):
        return response_bad_request()
    except Exception:
        return response_internal_server_error()


def __create_permission(data: dict) -> Permission:
    require_attrs(['name', 'description'], data)
    name: str = data['name']
    description: str = data['description']

    return Permission( _id=None, name=name, description=description )


def __update_permission(permission: Permission, data: dict) -> Permission:
    require_attrs(['name', 'description'], data)

    name: str = data['name']
    description: str = data['description']

    permission.name = name
    permission.description = description

    return permission

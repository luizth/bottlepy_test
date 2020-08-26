from bottle import request

from src.application import permission_manager
from src.exceptions.attribute_not_found import AttributeNotFound
from src.model.permission import Permission
from src.utils.http_utils import response_ok, response_bad_request, response_not_found, response_internal_server_error
from src.utils.validation_utils import require_attrs, require_dict


def get_many():
    return response_ok(permission_manager.get_many())


def get_one(_id):
    permission: Permission = permission_manager.get_one(_id)

    if permission is None:
        return response_not_found()

    return response_ok(permission)


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


def update(_id):
    permission: Permission = permission_manager.get_one(_id)

    if permission is None:
        return response_not_found()


def __create_permission(data: dict) -> Permission:
    require_attrs(['name', 'description'], data)
    name: str = data['name']
    description: str = data['description']

    return Permission( _id=None, name=name, description=description )

# def __update_permission(permission: Permission, data: dict) -> Permission:

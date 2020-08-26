from typing import List

from bottle import request

from src.application import user_manager
from src.controllers import permission_controller
from src.exceptions.attribute_not_found import AttributeNotFound
from src.exceptions.not_a_list import NotAListError
from src.model.permission import Permission
from src.model.user import User
from src.utils.http_utils import response_bad_request, response_ok, response_not_found, response_internal_server_error
from src.utils.validation_utils import require_attrs, require_dict, require_attr, require_list


def get_many():
    return response_ok(user_manager.get_many())


def get_one(_id):
    user: User = user_manager.get_one(_id)

    if user is None:
        return response_not_found()

    return response_ok(user)


def insert():
    data: dict = request.json

    try:
        require_dict(data)
        user = __create_user(data)
        _id = user_manager.insert(user)
        return response_ok({ 'id': _id })
    except (NotADirectoryError, AttributeNotFound):
        return response_bad_request()
    except Exception:
        return response_internal_server_error()


def remove(_id):
    _id = user_manager.remove(_id)

    if _id is None:
        return response_bad_request()

    return response_ok({ 'id': _id })


def update_one(_id):
    user: User = user_manager.get_one(_id)

    if user is None:
        return response_bad_request()

    data: dict = request.json

    try:
        require_dict(data)
        user = __update_user(user, data)
        user_id = user_manager.update_one(_id, user)
        return response_ok({ 'id': user_id })
    except (NotADirectoryError, AttributeNotFound):
        return response_bad_request()
    except Exception:
        return response_internal_server_error()


def get_permissions(_id):
    permissions: List[int] = user_manager.get_permissions(_id)

    if permissions is None:
        return response_not_found()

    permission_list: List[Permission] = []
    for permission_id in permissions:
        permission_list.append(permission_controller.get_one(permission_id))

    return response_ok({ 'id': _id, 'permissions': permission_list })


def update_permissions(_id):
    permissions: List[int] = user_manager.get_permissions(_id)

    if permissions is None:
        return response_not_found()

    data: dict = request.json

    try:
        require_dict(data)
        permission_update = __get_permissions(data)
        permission_update = list( set( permissions + permission_update ))
        user_manager.update_permissions(_id, permission_update)
        return response_ok({ 'id': _id })
    except (NotADirectoryError, AttributeNotFound, NotAListError):
        return response_bad_request()
    except Exception:
        return response_internal_server_error()


def __create_user(data: dict) -> User:
    require_attrs(['name', 'email'], data)
    name: str = data['name']
    email: str = data['email']

    return User( _id=None, name=name, email=email, permissions=None )


def __update_user(user: User, data: dict) -> User:
    require_attrs(['name', 'email'], data)
    name: str = data['name']
    email: str = data['email']

    user.name = name
    user.email = email

    return user


def __get_permissions(data: dict) -> List[int]:
    require_attr('permissions', data)
    require_list(data['permissions'])

    permissions: List[int] = []
    for key in data['permissions']:
        permissions.append(permission_controller.get_one(key))

    return permissions

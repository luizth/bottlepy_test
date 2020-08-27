from typing import List

from bottle import request

from src.application import user_manager, permission_manager
from src.exceptions.attribute_not_found import AttributeNotFound
from src.exceptions.invalid_email_address import InvalidEmailAddress
from src.exceptions.invalid_permission_id import InvalidPermissionId
from src.exceptions.not_a_list import NotAListError
from src.model.permission import Permission
from src.model.user import User
from src.utils.http_utils import response_bad_request, response_ok, response_not_found, response_internal_server_error
from src.utils.json_utils import instance_to_dict
from src.utils.validation_utils import require_attrs, require_dict, require_attr, require_list, require_email


def get_many():
    users: List[User] = user_manager.get_many()
    output: List[dict] = [instance_to_dict(user) for user in users]

    return response_ok(output)


def get_one(_id):
    user: User = user_manager.get_one(_id)

    if user is None:
        return response_not_found()

    output: dict = instance_to_dict(user)
    return response_ok(output)


def insert():
    data: dict = request.json

    try:
        require_dict(data)
        user = __create_user(data)
        _id = user_manager.insert(user)
        return response_ok({ 'id': _id })
    except (NotADirectoryError, AttributeNotFound, InvalidEmailAddress):
        return response_bad_request()
    except Exception:
        return response_internal_server_error()


def remove(_id):
    deleted_id = user_manager.remove(_id)

    if deleted_id is None:
        return response_bad_request()

    return response_ok({ 'id': deleted_id })


def update(_id):
    user: User = user_manager.get_one(_id)

    if user is None:
        return response_bad_request()

    data: dict = request.json

    try:
        require_dict(data)
        user = __update_user(user, data)
        user_id = user_manager.update(_id, user)
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
        permission = permission_manager.get_one( str(permission_id) )
        permission_list.append(instance_to_dict(permission))

    return response_ok({ 'id': _id, 'permissions': permission_list })


def update_permissions(_id):
    permissions: List[int] = user_manager.get_permissions(_id)

    if permissions is None:
        return response_not_found()

    data: dict = request.json

    try:
        require_dict(data)
        permissions = __validate_permissions(data)
        user_manager.update_permissions(_id, permissions)
        return response_ok({ 'id': _id })
    except (NotADirectoryError, AttributeNotFound, NotAListError, InvalidPermissionId):
        return response_bad_request()
    except Exception:
        return response_internal_server_error()


def __create_user(data: dict) -> User:
    require_attrs(['name', 'email'], data)
    require_email(data['email'])

    name: str = data['name']
    email: str = data['email']

    return User( _id=None, name=name, email=email, permissions=None )


def __update_user(user: User, data: dict) -> User:
    require_attrs(['name', 'email'], data)
    require_email(data['email'])

    name: str = data['name']
    email: str = data['email']

    user.name = name
    user.email = email

    return user


def __validate_permissions(data: dict) -> List[int]:
    require_attr('permissions', data)
    require_list(data['permissions'])

    for _id in data['permissions']:
        if not permission_manager.get_one( str(_id) ):
            raise InvalidPermissionId

    return data['permissions']

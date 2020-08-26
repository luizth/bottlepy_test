from json import dump, load
import os


def load_user_create(body):
    if 'name' not in body:
        return {}

    users = load_users_json()
    if not users:
        return {}

    user = {}
    for key in body:
        if key not in list(users.values())[0]:
            continue
        user[key] = body[key]
    if user:
        user["permissions"] = []

    return user


def load_user_update(body):
    users = load_users_json()
    if not users:
        return {}

    user = {}
    for key in body:
        if key not in list(users.values())[0]:
            continue
        user[key] = body[key]

    return user


def load_permissions_update(body):
    if 'permissions' not in body:
        return []

    permissions = load_permissions_json()
    if not permissions:
        return []

    p_update = []
    for p_id in body['permissions']:
        str_p_id = str(p_id)

        if str_p_id not in permissions:
            continue
        p_update.append(p_id)

    return p_update

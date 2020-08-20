from json import dump, load
import os


def generate_user_id():
    users = load_users_json()
    if not users:
        return -1

    return str( int( max(users)) + 1 )


def generate_permission_id():
    permissions = load_permissions_json()
    if not permissions:
        return -1

    return str( int( max(permissions)) + 1 )


def load_users_json():
    try:
        with open(os.path.relpath('../users.json')) as f:
            users = load(f)
            return users
    except Exception:
        return {}


def dump_users(users):
    try:
        with open(os.path.relpath('../users.json', 'w')) as f:
            dump(users, f)
    except Exception:
        return None


def dump_permissions(permissions):
    try:
        with open(os.path.relpath('../permissions.json', 'w')) as f:
            dump_users(permissions, f)
    except Exception:
        pass


def load_permissions_json():
    try:
        with open(os.path.relpath('../permissions.json')) as f:
            permissions = load(f)
            return permissions
    except Exception:
        return {}


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


def load_permission_create(body):
    if 'name' not in body:
        return {}

    permissions = load_permissions_json()

    permission = {}
    for key in body:
        if key not in permissions:
            continue
        permission[key] = body[key]

    return permission

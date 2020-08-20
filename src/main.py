from bottle import run, request, route
from src.server_response import *
from src.dao import *


@route('/api/user', method='GET')
def get_users():
    users = load_users_json()
    if not users:
        return response_bad_request()

    u_output = []
    for key, value in users.items():
        user = {
            'id': key,
            'name': value['name'],
            'email': value['email'],
            'permissions': value['permissions']
        }
        u_output.append(user)

    return response_ok(u_output)


@route('/api/user/<_id>', method='GET')
def get_user(_id):
    users = load_users_json()
    if not users:
        return response_bad_request()
    elif _id not in users:
        return response_not_found()

    u_output = {
        'id': _id,
        'name': users[_id]['name'],
        'email': users[_id]['email'],
        'permissions': users[_id]['permissions']
    }

    return response_ok(u_output)


@route('/api/user', method='POST')
def post_user():
    user = load_user_create(request.json)
    if not user:
        return response_bad_request()

    users = load_users_json()
    if not users:
        return response_bad_request()

    u_id = generate_user_id()
    if u_id == -1:
        return response_bad_request()

    users[u_id] = user

    dump_users(users)
    return response_ok({ 'id': u_id })


@route('/api/user/<_id>', method='DELETE')
def delete_user(_id):
    users = load_users_json()
    if not users:
        return response_bad_request()
    elif _id not in users:
        return response_not_found()

    del users[_id]

    dump_users(users)
    return response_ok({ 'id': _id })


@route('/api/user/<_id>', method='PATCH')
def update_user(_id):
    user = load_user_update(request.json)
    if not user:
        return response_bad_request()

    users = load_users_json()
    if not users:
        return response_bad_request()
    elif _id not in users:
        return response_not_found()

    u_update = users[_id]
    for key in user:
        u_update[key] = user[key]

    users[_id].update(u_update)

    dump_users(users)
    return response_ok({ 'id': _id })


@route('/api/user/<_id>/permissions', method='GET')
def get_user_permissions(_id):
    users = load_users_json()
    if _id not in users:
        return response_not_found()

    permissions = load_permissions_json()
    if not permissions:
        return response_bad_request()

    p_output = []
    for p_id in users[_id]['permissions']:
        str_p_id = str(p_id)

        permission = {
            'id': p_id,
            'name': permissions[str_p_id]['name']
        }
        p_output.append(permission)

    output = {
        'id': _id,
        'name': users[_id]['name'],
        'permissions': p_output
    }

    return response_ok(output)


@route('/api/user/<_id>/permissions', method='PUT')
def update_user_permissions(_id):
    users = load_users_json()
    if _id not in users:
        return response_not_found()

    update_list = load_permissions_update(request.json)
    if not update_list:
        return response_bad_request()

    current_list = users[_id]['permissions']
    new_current_list = list(set(current_list + update_list))
    users[_id]['permissions'] = new_current_list

    dump_users(users)
    return response_ok({'id': _id})


@route('/api/permissions', method='GET')
def get_permissions():
    permissions = load_permissions_json()

    p_output = []
    for key, value in permissions.items():
        permission = {
            'id': key,
            'name': value['name'],
            'description': value['description']
        }
        p_output.append(permission)

    return response_ok(permission)


@route('/api/permissions/<_id>', method='GET')
def get_permission(_id):
    permissions = load_permissions_json()
    if not permissions:
        return response_bad_request()
    elif _id not in permissions:
        return response_not_found()

    p_output = {
        'id': _id,
        'name': permissions[_id]['name'],
        'description': permissions[_id]['description']
    }

    return response_ok(p_output)


@route('/api/permissions', method='POST')
def post_permission():
    permission = load_permission_create(request.json)
    if not permission:
        return response_bad_request()

    permissions = load_permissions_json()
    if not permissions:
        return response_bad_request()

    p_id = generate_permission_id()
    if p_id == -1:
        return response_bad_request()

    permissions[p_id] = permission

    dump_permissions(permissions)
    return response_ok({ 'id': p_id })


run(host='localhost', port=8080, reloader=True, debug=True)

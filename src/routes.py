from bottle import route, run

from src.controllers import permission_controller, user_controller


# Permissions
# -----------------------------------------------------------------------------
@route('/api/permission', method='GET')
def get_permissions():
    return permission_controller.get_many()


@route('/api/permission/<_id>', method='GET')
def get_permission(_id):
    return permission_controller.get_one(_id)


@route('/api/permission', method='POST')
def post_permission():
    return permission_controller.insert()


@route('/api/permission/<_id>', method='DELETE')
def delete_permission(_id):
    return permission_controller.remove(_id)


@route('/api/permission/<_id>', method='PATCH')
def patch_permission(_id):
    return permission_controller.update(_id)


# Users
# -----------------------------------------------------------------------------
@route('/api/user', method='GET')
def get_users():
    return user_controller.get_many()


@route('/api/user/<_id>', method='GET')
def get_user(_id):
    return user_controller.get_one(_id)


@route('/api/user', method='POST')
def post_user():
    return user_controller.insert()


@route('/api/user/<_id>', method='DELETE')
def delete_user(_id):
    return user_controller.remove(_id)


@route('/api/user/<_id>', method='PATCH')
def patch_user(_id):
    return user_controller.update(_id)


@route('/api/user/<_id>/permissions', method='GET')
def get_user_permissions(_id):
    return user_controller.get_permissions(_id)


@route('/api/user/<_id>/permissions', method='PATCH')
def patch_user_permissions(_id):
    return user_controller.update_permissions(_id)


run(host='localhost', port=8080, reloader=True)

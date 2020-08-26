from bottle import response
from json import dumps


def response_data(status, data):
    response.status = status
    response.content_type = 'application/json'
    return dumps(data)


def response_ok(data):
    return response_data(200, data)


def response_status(status):
    response.status = status
    response.content_type = 'application/json'
    return None


def response_bad_request():
    return response_status(400)


def response_not_found():
    return response_status(404)


def response_internal_server_error():
    return response_status(500)

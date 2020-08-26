from bottle import run, request, route
from src.utils.http_utils import *
from src.dao import *


run(host='localhost', port=8080, reloader=True, debug=True)

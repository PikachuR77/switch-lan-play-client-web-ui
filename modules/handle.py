from flask import Blueprint
from utils import make_error

handle = Blueprint('BlueprintHandle', __name__, url_prefix='/')


@handle.app_errorhandler(400)
def bad(e):
    return make_error(msg='Bad Request'), 400


@handle.app_errorhandler(404)
def miss(e):
    return make_error(msg='Not Found'), 404


@handle.app_errorhandler(405)
def not_allowed(e):
    return make_error(msg='Method Not Allowed'), 405


@handle.app_errorhandler(500)
def error(e):
    return make_error(msg='Server Exception'), 500

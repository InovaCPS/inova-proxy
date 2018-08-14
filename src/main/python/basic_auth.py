#   Date: 2018-08-13
#   Author: Lucas Nadalete
#
#   License: GPL v3


"""
    This module provides a simple Basi Authentication
    security level.
"""

from functools import wraps

from flask import Response, request

import webapp
from helper.config_helper import ConfigHelper

APP_RESOURCE = webapp.APP_RESOURCE

def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    global APP_RESOURCE
    config = ConfigHelper(APP_RESOURCE)
    auth_username = config.get_property_by_section('server', 'auth.username')
    auth_password = config.get_property_by_section('server', 'auth.password')
    return username == auth_username and password == auth_password

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
        'Could not verify your access level for that URL.\n'
        'You have to login with proper credentials', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated
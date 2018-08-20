#   Date: 2018-07-10
#   Author: Lucas Nadalete
#
#   License: GPL v3


"""
    This module provides a flask application responding
    to the endpoints of Logger.
"""

from functools import wraps

from flask import Flask, Response, request
from flask_restful import Api

from helper.config_helper import ConfigHelper


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


APP_RESOURCE = './src/main/resources/application.properties'
app = Flask(__name__)
api = Api(app)

from controller.proxy_controller import CnpqCvController, CnpqCvsController

api.add_resource(CnpqCvsController, "/cnpq/cvs", methods=["GET"])
api.add_resource(CnpqCvController, "/cnpq/cv/<string:id>", methods=["GET"])

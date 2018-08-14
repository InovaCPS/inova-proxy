#   Date: 2018-07-10
#   Author: Lucas Nadalete
#
#   License: GPL v3


"""
    Controller class used to get the log registers persisted and save
    a new log register.
"""

from flask import json
from flask_restful import Resource

from basic_auth import requires_auth
from webapp import api, app


@api.resource('/proxy/cnpq')
class CnpqProxyController(Resource):

    @requires_auth
    def get(self):
        response = app.response_class(
            response=json.dumps({'response' : 'To be develop.'}),
            status=200,
            mimetype='application/json'
        )
        return response

#   Date: 2018-07-10
#   Author: Lucas Nadalete
#
#   License: GPL v3


"""
    Controller class used to get a individual CV or a lot of CVs, consuming directly of the SOAP
    service provided by CNPq.
"""

from json import dumps

from flask import request
from flask_restful import Resource, abort

from basic_auth import requires_auth
from service.cnpq_soap_service import CnpqSoapService
from webapp import app


class CnpqCvsController(Resource):

    def __init__(self):
        super().__init__()
        self.service = CnpqSoapService()

    @requires_auth
    def post(self):
        response = None
        curriculos = []
        cpfs = list(set(request.json['cpfs']))
        if len(cpfs) > 5:
            cpfs = cpfs[:5]
        for cpf in cpfs:
            xml_content = self.service.get_cv(cpf)
            if xml_content is not None:
                curriculos.append(xml_content)
        if len(curriculos) > 0:
            response = app.response_class(
                response=dumps({"curriculos": curriculos}),
                status=200,
                mimetype='application/json'
            )
        else:
            abort(404, message='No curriculum found to the CPFs informed')
        return response


class CnpqCvController(Resource):

    def __init__(self):
        super().__init__()
        self.service = CnpqSoapService()

    @requires_auth
    def get(self, cpf=None):
        response = None
        if cpf is not None:
            xml_content = self.service.get_cv(cpf)
            if xml_content is not None:
                response = app.response_class(
                    response=dumps(xml_content),
                    status=200,
                    mimetype='application/json'
                )
            else:
                abort(404, message='No curriculum found to the CPF informed')
        else:
            abort(412, message='No valid CPF value informed')
        return response

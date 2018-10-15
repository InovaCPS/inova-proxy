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
            cpfs = [cpf for cpf in cpfs[:5] if cpf is not None]
        for cpf in cpfs:
            json_content = self.service.get_json_cv(cpf)
            if json_content is not None:
                curriculos.append(json_content)
            else:
                curriculos.append(dict(cpf=cpf, message='No curriculum found to the CPF informed'))
        if len(curriculos) > 0:
            response = app.response_class(
                response=dumps({"curriculos": curriculos}),
                status=201,
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
        content_type = request.mimetype
        response = None
        if cpf is not None:
            if content_type == 'application/xml':
                xml_content = self.service.get_xml_cv(cpf)
            else:
                xml_content = self.service.get_json_cv(cpf)
                xml_content = dumps(xml_content)
            # Verify if the header content-type is JSON or XML
            if xml_content is not None:
                response = app.response_class(
                    response=xml_content,
                    status=200,
                    mimetype=content_type
                )
            else:
                abort(404, message='No curriculum found to the CPF informed or invalid mimetype')

        else:
            abort(412, message='No valid CPF value informed')
        return response


class CnpqUpdateDateController(Resource):

    def __init__(self):
        super().__init__()
        self.service = CnpqSoapService()

    @requires_auth
    def get(self, cpf=None):
        response = {'cpf': cpf}
        if cpf is not None:
            identificador = self.service.get_identificador(cpf)
            if identificador is not None:
                response['identificador'] = identificador
                date = self.service.get_data_atualizacao_cv(identificador)
                if date is not None:
                    response['data_atualizacao'] = date
                    response = app.response_class(
                        response=dumps(response),
                        status=200,
                        mimetype='application/json'
                    )
                else:
                    abort(404, message='No update date found to the CPF informed')

        else:
            abort(412, message='No valid CPF value informed')
        return response

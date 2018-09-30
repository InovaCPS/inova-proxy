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

    @requires_auth
    def post(self):
        cpfs = request.json['cpfs']
        for cpf in cpfs:
            print("CPFs: " + cpf)
        cpfs = { "cpfsnew" : cpfs}
        # mapper = XmlMapper()
        # from mapper.xml_mapper import XmlMapper
        # curriculos = {"curriculos": []}
        # set_files = glob.glob('src/main/resources/cvs/*.xml')
        # if len(set_files) > 0:
        #     for nfile in set_files:
        #         file = open(nfile, encoding="iso-8859-1")
        #         xml_content = file.read()
        #         curriculos["curriculos"].append(mapper.convert_to_dict(xml_content))
        #     response = app.response_class(
        #         response=dumps(curriculos),
        #         status=200,
        #         mimetype='application/json'
        #     )
        # else:
        #     abort(404, message='No curriculum found')
        response = app.response_class(dumps(cpfs), status=200, mimetype='application/json')
        return response


class CnpqCvController(Resource):

    @requires_auth
    def get(self, cpf=None):
        response = None
        if cpf is not None:
            service = CnpqSoapService()
            xml_content = service.get_cv(cpf)
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

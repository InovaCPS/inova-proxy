#   Date: 2018-07-10
#   Author: Lucas Nadalete
#
#   License: GPL v3


"""
    Controller class used to get a individual CV or a lot of CVs, consuming directly of the SOAP
    service provided by CNPq.
"""

import glob
import os.path
from json import dumps

from flask_restful import Resource, abort

from basic_auth import requires_auth
from helper.xml_helper import XmlHelper
from webapp import app


class CnpqCvsController(Resource):

    @requires_auth
    def get(self):
        helper = XmlHelper()
        curriculos = {"curriculos": []}
        set_files = glob.glob('src/main/resources/cvs/*.xml')
        if len(set_files) > 0:
            for nfile in set_files:
                file = open(nfile, encoding="iso-8859-1")
                xml_content = file.read()
                curriculos["curriculos"].append(helper.convert_to_dict(xml_content))
            response = app.response_class(
                response=dumps(curriculos),
                status=200,
                mimetype='application/json'
            )
        else:
            abort(404, message='No curriculum found')
        return response



class CnpqCvController(Resource):

    @requires_auth
    def get(self, id):
        path = "src/main/resources/cvs/curriculo_" + id + ".xml"
        if os.path.exists(path):
            file = open(path, encoding="iso-8859-1")
            helper = XmlHelper()
            xml_content = file.read()
            response = app.response_class(
                response=dumps(helper.convert_to_dict(xml_content)),
                status=200,
                mimetype='application/json'
            )
        else:
            abort(404, message='No curriculum found to the identifier')
        return response

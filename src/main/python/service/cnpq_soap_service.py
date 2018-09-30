#   Date: 2018-09-27
#   Author: Lucas Nadalete
#
#   License: GPL v3


"""
    Service implemments a common accesses to the CNPq services.
"""

import base64
import os
import shutil
import time
import zipfile
import urllib

from suds.client import Client

from mapper.xml_mapper import XmlMapper


class CnpqSoapService:

    def __init__(self):
        """
            Instanciate the SoapService based in a custom WSDL.
        """
        self.client = Client('http://servicosweb.cnpq.br/srvcurriculo/WSCurriculo?wsdl')
        self.xmlmapper = XmlMapper()

    def get_identificador(self, cpf):
        """
        Get the CNPq lattes identifier based in the cpf
        :param cpf: CPF of the instituion employee
        :return: Identifier of the instituion employee
        """
        self.client.set_options(headers={'SOAPAction': 'getIdentificadorCNPq', 'Content-Type' : 'text/xml; charset=ISO-8859-1'})
        result = self.client.service.getIdentificadorCNPq(cpf,'','')
        identificador = result
        if result != None:
            identificador = "".join( chr(x) for x in result.encode('utf-8'))
        return identificador # Return None if the CPF to be invalid

    def get_data_atualizacao_cv(self, identificador):
        self.client.set_options(headers={'SOAPAction': 'getDataAtualizacaoCV', 'Content-Type' : 'text/xml; charset=ISO-8859-1'})
        result = self.client.service.getDataAtualizacaoCV(identificador)
        return "".join( chr(x) for x in result.encode('utf-8'))

    def get_cv_lattes(self, identificador):
        """
        Query the CV of the employee
        :param identificador: Identifier of the instituion employee
        :return: CV in XML format
        """
        self.client.set_options(headers={'SOAPAction': 'getCurriculoCompactado', 'Content-Type' : 'text/xml; charset=ISO-8859-1'})
        result = self.client.service.getCurriculoCompactado(identificador)
        # Decodifica o conteudo em Base64 e escreve em um arquivo local com nome do identificador.xml
        zipfilename = identificador + "-" + str(int(time.time()))
        basedirpath = "src/main/resources/tmp/"
        if not os.path.exists(basedirpath + zipfilename):
            os.makedirs(basedirpath + zipfilename)
        zipstream = base64.b64decode(result.encode('utf-8'))
        zipout = open(basedirpath + zipfilename + "/" + zipfilename + ".zip", "wb")
        zipout.write(zipstream)
        zipout.close()
        zip = zipfile.ZipFile(basedirpath + zipfilename + "/" + zipfilename + ".zip")
        zip.extractall(basedirpath + zipfilename)
        zip.close()
        xmlin = open(basedirpath + zipfilename + "/" + identificador + ".xml", encoding='iso-8859-1')
        xmlcv = xmlin.read()
        xmlin.close()
        if os.path.exists(zipfilename):
            shutil.rmtree(basedirpath + zipfilename)
        return xmlcv.encode('iso-8859-1')

    def get_cv(self, cpf):
        cv = {}
        cv['cpf'] = cpf
        cv['identificador'] = self.get_identificador(cpf)
        if cv['identificador'] is not None:
            cv['data_atualizacao'] = self.get_data_atualizacao_cv(cv['identificador'])
            grossxml = self.get_cv_lattes(cv['identificador'])
            cv['data'] = self.xmlmapper.convert_to_dict(grossxml)
        else:
            cv = None
        return cv
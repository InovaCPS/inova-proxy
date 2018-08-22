#   Date: 2018-10-19
#   Author: Lucas Nadalete
#
#   License: GPL v3


"""
    Config helper implemments a common methods used convert XML to other formats or
    transform other formats to XML.
"""

from collections import OrderedDict

from xmltodict import parse


class XmlMapper:

    def convert_to_dict(self, xml_content):
        """Method used to convert XML to JSON format.

        :param xml_content: The XML content.
        :type xml_content: str.
        :returns:  str -- The generated JSON.

        """
        data_dict = dict(parse(xml_content, encoding="iso-8859-1"))
        data_dict = self.rename_keys_to_lower(data_dict, '@', '')
        return data_dict

    def rename_keys_to_lower(self, iterable, str_find, str_replace):
        """Method used to replace all dict keys to LOWER replacing
        removing @ character

        :param iterable: XML converted to dict as the content file.
        :type iterable: dict.
        :param str_find: String pattern to be replaced.
        :type str_find: str.
        :param str_replace: String pattern applied in replace action.
        :type str_replace: str.
        :returns:  str -- The JSON with the keys updated.

        """
        new_iterable = {} if type(iterable) in (dict, OrderedDict) else []
        if type(iterable) in (dict, OrderedDict):
            for key in iterable.keys():
                new_key = key.lower().replace(str_find, str_replace)
                if type(iterable[key]) in (dict, OrderedDict) or type(iterable[key]) is list:
                    new_iterable[new_key] = self.rename_keys_to_lower(iterable[key], str_find, str_replace)
                else:
                    new_iterable[new_key] = iterable[key]
        elif type(iterable) is list:
            for item in iterable:
                new_iterable.append(self.rename_keys_to_lower(item, str_find, str_replace))
        return new_iterable

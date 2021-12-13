"""
    API Response 정보 Model class
"""


class ResponseInfo:
    def __init__(self, status_code,  content_type, description, schema):
        self.__status_code = status_code
        self.__content_type = content_type
        self.__description = description
        self.__schema = schema

    @property
    def status_code(self):
        return self.__status_code

    @status_code.setter
    def status_code(self, status_code):
        self.__status_code = status_code

    @property
    def content_type(self):
        return self.__content_type

    @content_type.setter
    def content_type(self, content_type):
        self.__content_type = content_type

    @property
    def description(self):
        return self.__description

    @description.setter
    def description(self, description):
        self.__description = description

    @property
    def schema(self):
        return self.__schema

    @schema.setter
    def schema(self, schema):
        self.__schema = schema
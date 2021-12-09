"""
    API Request 정보 Model class
"""


class RequestInfo:
    def __init__(self, content_type, required, schema):
        self.__content_type = content_type
        self.__required = required
        self.__schema = schema

    @property
    def content_type(self):
        return self.__content_type

    @content_type.setter
    def content_type(self, content_type):
        self.__content_type = content_type

    # getter
    @property
    def required(self):
        return self.__required

    # setter
    @required.setter
    def required(self, required):
        self.__required = required

    @property
    def schema(self):
        return self.__schema

    @schema.setter
    def schema(self, schema):
        self.__schema = schema


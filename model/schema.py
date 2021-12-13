"""
    schema 정보
"""


class ReqSchema:

    def __init__(self, name, title, required, type, default, description):
        self.__name = name
        self.__title = title
        self.__required = required
        self.__type = type
        self.__default = default
        self.__description = description

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name

    @property
    def title(self):
        return self.__title

    @title.setter
    def title(self, title):
        self.__title = title

    @property
    def required(self):
        return self.__required

    @required.setter
    def required(self, required):
        self.__required = required

    @property
    def type(self):
        return self.__type

    @type.setter
    def type(self, type):
        self.__type = type

    @property
    def default(self):
        return self.__default

    @default.setter
    def default(self, default):
        self.__default = default

    @property
    def description(self):
        return self.__description

    @description.setter
    def description(self, description):
        self.__description = description


class ParamSchema:

    def __init__(self, name, title, schema_in, required, type, default, description):
        self.__name = name
        self.__title = title
        self.__schema_in = schema_in
        self.__required = required
        self.__type = type
        self.__default = default
        self.__description = description

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name

    @property
    def title(self):
        return self.__title

    @title.setter
    def title(self, title):
        self.__title = title

    @property
    def schema_in(self):
        return self.__schema_in

    @schema_in.setter
    def schema_in(self, schema_in):
        self.__schema_in = schema_in

    @property
    def required(self):
        return self.__required

    @required.setter
    def required(self, required):
        self.__required = required

    @property
    def type(self):
        return self.__type

    @type.setter
    def type(self, type):
        self.__type = type

    @property
    def default(self):
        return self.__default

    @default.setter
    def default(self, default):
        self.__default = default

    @property
    def description(self):
        return self.__description

    @description.setter
    def description(self, description):
        self.__description = description





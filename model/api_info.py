"""
    API 정보 Model class
"""


class ApiInfo:

    def __init__(self, summary, description, method, uri, security, request, responses):
        self.__summary = summary
        self.__description = description
        self.__method = method
        self.__uri = uri
        self.__security = security
        self.__request = request
        self.__responses = responses

    # getter
    @property
    def summary(self):
        return self.__summary

    # setter
    @summary.setter
    def summary(self, summary):
        self.__summary = summary

    @property
    def description(self):
        return self.__description

    @description.setter
    def description(self, description):
        self.__description = description

    @property
    def method(self):
        return self.__method

    @method.setter
    def method(self, method):
        self.__method = method

    @property
    def uri(self):
        return self.__uri

    @uri.setter
    def uri(self, uri):
        self.__uri = uri

    @property
    def security(self):
        return self.__security

    @security.setter
    def security(self, security):
        self.__security = security

    @property
    def request(self):
        return self.__request

    @request.setter
    def request(self, request):
        self.__request = request

    @property
    def responses(self):
        return self.__responses

    @responses.setter
    def responses(self, responses):
        self.__responses = responses


if __name__ == "__main__":
    test = ApiInfo("인증토큰 발급", "테스트입니다.", "get", "/////")
    test.security = "security....."
    print(test.summary, test.description, test.method, test.uri, test.security)

class SDKException(Exception):
    code = None

    def __init__(self, message='', code=None):
        if code:
            self.code = code
        super().__init__(f'<{self.code}> {message}')


class UrlNotFoundException(SDKException):
    code = 404


class ParamException(SDKException):
    code = 'PARAM_ERROR'


class ConverterException(SDKException):
    """

    """


EXCEPTIONS = {
    ParamException.code: ParamException
}

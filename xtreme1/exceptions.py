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


class DatasetIdException(SDKException):
    code = 'DATASET_NOT_FOUND'


class NameDuplicatedException(SDKException):
    code = 'NAME_DUPLICATED'


class ConverterException(SDKException):
    code = 'NOT_SUPPORT'


class SourceException(SDKException):
    code = 'UNPARSEABLE'


class NoPermissionException(SDKException):
    code = 'NO_PERMISSION'


EXCEPTIONS = {
    ParamException.code: ParamException,
    DatasetIdException.code: DatasetIdException,
    NameDuplicatedException.code: NameDuplicatedException,
    ConverterException.code: ConverterException
}

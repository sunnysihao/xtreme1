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


class ConverterException(SDKException):
    code = 'ANNOTATIONS_DO_NOT_SUPPORT_THIS_FORMAT'


class SourceException(SDKException):
    code = ''


EXCEPTIONS = {
    ParamException.code: ParamException,
    DatasetIdException.code: DatasetIdException
}

class BFException(Exception):
    def __init__(self, code, message=''):
        super().__init__(f'<{code}> {message}')



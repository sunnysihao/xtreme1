import requests

from .exceptions import SDKException


class Api:

    def __init__(self, access_token, base_url):
        self.access_token = access_token
        self._headers = {
            'Authorization': f'Bearer {access_token}'
        }
        self.base_url = base_url

    def _base_request(
            self,
            method,
            headers,
            endpoint,
            params=None,
            files=None,
            data=None,
            json=None,
            full_url=None
    ):

        if not full_url:
            full_url = f'{self.base_url}/api/{endpoint}'

        resp = requests.request(method=method, url=full_url, headers=headers, params=params, files=files, data=data,
                                json=json)

        if resp.status_code == 200:
            info = resp.json()
            if info['code'] == 'OK':
                return info['data']
            else:
                raise SDKException(code=info['code'], message=info['message'])
        else:
            raise SDKException(code=resp.status_code)

    def get_request(self, endpoint, params, headers=True, full_url=None):
        if headers:
            headers = self._headers
        return self._base_request(method='GET', headers=headers, endpoint=endpoint, params=params, full_url=full_url)

    def post_request(self, endpoint, payload, files=None, headers=True, full_url=None):
        if headers:
            headers = self._headers
        return self._base_request(method='POST', headers=headers, endpoint=endpoint, json=payload, files=files,
                                  full_url=full_url)

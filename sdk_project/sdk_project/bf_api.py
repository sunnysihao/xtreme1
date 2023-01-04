from requests import Session
from requests.adapters import HTTPAdapter, Retry

from bf_exceptions import BFException

BASIC_FINDER_API_ROOT_URL = 'https://x1-community.alidev.beisai.com/api'

# retry strategy
TOTAL_RETRIES = 3
BACKOFF_FACTOR = 2
STATUS_FORCE_LIST = []


class BFApi:

    def __init__(self, access_token):
        self.access_token = access_token
        self._headers = {
            'Authorization': f'Bearer {access_token}'
        }

    @staticmethod
    def _base_request(method, url, headers=None, params=None, files=None, data=None):
        ss = Session()
        retry_strategy = Retry(
            total=TOTAL_RETRIES,
            backoff_factor=BACKOFF_FACTOR,
            status_forcelist=STATUS_FORCE_LIST,
        )

        adapter = HTTPAdapter(max_retries=retry_strategy)
        ss.mount(prefix='https://', adapter=adapter)

        resp = ss.request(method=method, url=url, params=params, headers=headers, files=files, json=data)

        return resp

    def _api_request(self, method, headers, endpoint, params=None, files=None, data=None):
        full_url = f'{BASIC_FINDER_API_ROOT_URL}/{endpoint}'
        resp = self._base_request(method, full_url, headers, params, files, data)

        if resp.status_code == 200:
            info = resp.json()
            if info['code'] == 'OK':
                return info['data']
            else:
                raise BFException(code=info['code'], message=info['message'])
        else:
            raise BFException(code=resp.status_code)

    def get_request(self, endpoint, params, headers=True):
        if headers:
            headers = self._headers
        return self._api_request(method='GET', headers=headers, endpoint=endpoint, params=params)

    def post_request(self, endpoint, data, files=None, headers=True):
        if headers:
            headers = self._headers
        return self._api_request(method='POST', headers=headers, endpoint=endpoint, data=data, files=files)

    def put_request(self, endpoint, data, headers=True):
        if headers:
            headers = self._headers
        return self._api_request(method='POST', headers=headers, endpoint=endpoint, data=data)


def main():
    api = BFApi
    api.post_request()


if __name__ == '__main__':
    main()

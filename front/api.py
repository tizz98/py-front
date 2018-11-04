import urllib.parse

from .marshalling import FrontObject
from .requests import RequestsRequester, RequestOptions


class Api:
    base_url = 'https://api2.frontapp.com'

    def __init__(self, api_key: str) -> None:
        self._api_key = api_key
        self._requester = RequestsRequester()

    def me(self, options: RequestOptions = None):
        return self._get('me', options)

    def _get(self, url, options: RequestOptions = None):
        return self._request('get', url, options)

    def _request(self, method, endpoint, options: RequestOptions = None) -> FrontObject:
        options = options or RequestOptions('', '')
        options.method = method
        options.url = urllib.parse.urljoin(self.base_url, endpoint)

        resp = self._requester.request(options)
        return FrontObject.from_bytes(resp.content)

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

    def teams(self, options: RequestOptions = None):
        return self._get('teams', options)

    def team(self, team_id: str, options: RequestOptions = None):
        return self._get('teams/{id}'.format(id=team_id), options)

    def _get(self, url, options: RequestOptions = None):
        return self._request('get', url, options)

    def _request(self, method, endpoint, options: RequestOptions = None) -> FrontObject:
        options = options or RequestOptions('', '')
        options.method = method
        options.url = urllib.parse.urljoin(self.base_url, endpoint)

        options.headers = (options.headers or {})
        options.headers.setdefault('Authorization', 'Bearer {}'.format(self._api_key))
        options.headers.setdefault('Content-Type', 'application/json')
        options.headers.setdefault('Accept', 'application/json')

        resp = self._requester.request(options)
        return FrontObject.from_bytes(resp.content)

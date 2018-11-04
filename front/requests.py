import abc
from http.cookiejar import CookieJar
from typing import Union, TextIO, BinaryIO, List, Any

import requests


FileLike = Union[TextIO, BinaryIO]


class RequestOptions:
    __slots__ = (
        'method',
        'url',
        'params',
        'data',
        'json',
        'headers',
        'cookies',
        'files',
        'auth',
        'timeout',
        'allow_redirects',
        'proxies',
        'verify',
        'stream',
        'cert',
    )

    _default = object()

    def __init__(
        self,
        method: str = '',
        url: str = '',
        params: Union[dict, bytes] = _default,
        data: Union[dict, List[tuple], bytes, FileLike] = _default,
        json: dict = _default,
        headers: dict = _default,
        cookies: Union[dict, CookieJar] = _default,
        files=_default,
        auth=_default,
        timeout=_default,
        allow_redirects=_default,
        proxies=_default,
        verify=_default,
        stream=_default,
        cert=_default,
    ):
        self.method = method
        self.url = url

        self._set_value('params', params)
        self._set_value('data', data)
        self._set_value('json', json)
        self._set_value('headers', headers)
        self._set_value('cookies', cookies)
        self._set_value('files', files)
        self._set_value('auth', auth)
        self._set_value('timeout', timeout)
        self._set_value('allow_redirects', allow_redirects, True)
        self._set_value('proxies', proxies)
        self._set_value('verify', verify)
        self._set_value('stream', stream)
        self._set_value('cert', cert)

    def add_parameter(self, name: str, value: Any) -> None:
        if not self.params:
            self.params = {}

        if name in self.params:
            if not isinstance(self.params[name], list):
                self.params[name] = [self.params[name]]
            self.params[name].append(value)
        else:
            self.params[name] = value

    def _set_value(self, attr: str, value: Any, default: Any = None) -> None:
        if value is self._default:
            value = default
        setattr(self, attr, value)


class RequesterInterface(abc.ABC):
    @abc.abstractmethod
    def request(self, options: RequestOptions) -> requests.Response:
        pass

    def get(self, method, url, params, options: RequestOptions = None) -> requests.Response:
        options = options or RequestOptions(method, url)
        options.params = params
        return self.request(options)


class RequestsRequester(RequesterInterface):
    def request(self, options: RequestOptions) -> requests.Response:
        return requests.request(
            options.method,
            options.url,
            params=options.params,
            data=options.data,
            json=options.json,
            headers=options.headers,
            cookies=options.cookies,
            files=options.files,
            auth=options.auth,
            timeout=options.timeout,
            allow_redirects=options.allow_redirects,
            proxies=options.proxies,
            verify=options.verify,
            stream=options.stream,
            cert=options.cert,
        )

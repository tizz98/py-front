import json
import os
import urllib.parse

import jwt
import responses
import requests

from front.requests import (
    RequesterInterface,
    RequestOptions,
    RequestsRequester,
)


def get_jwt() -> str:
    return jwt.encode({
        "scopes": [
            "shared:*",
            "private:*"
        ],
        "iss": "front",
        "sub": "api_development",
        "jti": "a6749308269eb388"
    }, "123").decode('utf-8')


TESTDATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), 'testdata'))


class RequesterMock(RequesterInterface):
    _allowed_methods = {
        'get',
    }

    def __init__(self):
        self.r = RequestsRequester()
        self.calls = []

    @responses.activate
    def request(self, options: RequestOptions) -> requests.Response:
        if options.method not in self._allowed_methods:
            raise RuntimeError('unsupported method: %r' % options.method)

        parsed = urllib.parse.urlparse(options.url)
        path = os.path.join(TESTDATA_DIR, parsed.path.lstrip('/'))

        if os.path.exists(path + '.json'):
            with open(path + '.json') as f:
                data = json.load(f)

            responses.add(options.method.upper(), options.url, json=data)
        elif os.path.exists(path):
            with open(path, 'rb') as f:
                data = f.read()

            responses.add(options.method.upper(), options.url, body=data)

        v = self.r.request(options)
        self.calls = list(responses.calls)
        return v

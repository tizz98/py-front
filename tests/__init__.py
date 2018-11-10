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
        'patch',
        'post',
    }

    def __init__(self):
        self.r = RequestsRequester()
        self.calls = []

    @responses.activate
    def request(self, options):
        if options.method not in self._allowed_methods:
            raise RuntimeError('unsupported method: %r' % options.method)

        parsed = urllib.parse.urlparse(options.url)
        path = os.path.join(TESTDATA_DIR, parsed.path.lstrip('/'))

        if options.method == 'get':
            if os.path.exists(path + '.json'):
                with open(path + '.json') as f:
                    data = json.load(f)

                responses.add(options.method.upper(), options.url, json=data)
            elif os.path.exists(path):
                with open(path, 'rb') as f:
                    data = f.read()

                responses.add(options.method.upper(), options.url, body=data)
            else:
                raise RuntimeError('no file found. Tried: {!r} and {!r}'.format(path, path + '.json'))
        elif options.method == 'patch':
            responses.add(options.method.upper(), options.url, status=204)
        elif options.method == 'post':
            data = None
            post_path = os.path.join(path, '_post.json')

            if os.path.exists(post_path):
                with open(post_path) as f:
                    data = json.load(f)

            responses.add(options.method.upper(), options.url, json=data, status=201)

        v = self.r.request(options)
        self.calls = list(responses.calls)
        return v

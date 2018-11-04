import codecs
from datetime import datetime
import json
from typing import Optional

from .exceptions import InvalidTimezoneError


# Taken from the json library. Needed for python 3.5 support
def detect_encoding(b):
    bstartswith = b.startswith
    if bstartswith((codecs.BOM_UTF32_BE, codecs.BOM_UTF32_LE)):
        return 'utf-32'
    if bstartswith((codecs.BOM_UTF16_BE, codecs.BOM_UTF16_LE)):
        return 'utf-16'
    if bstartswith(codecs.BOM_UTF8):
        return 'utf-8-sig'

    if len(b) >= 4:
        if not b[0]:
            # 00 00 -- -- - utf-32-be
            # 00 XX -- -- - utf-16-be
            return 'utf-16-be' if b[1] else 'utf-32-be'
        if not b[1]:
            # XX 00 00 00 - utf-32-le
            # XX 00 00 XX - utf-16-le
            # XX 00 XX -- - utf-16-le
            return 'utf-16-le' if b[2] or b[3] else 'utf-32-le'
    elif len(b) == 2:
        if not b[0]:
            # 00 XX - utf-16-be
            return 'utf-16-be'
        if not b[1]:
            # XX 00 - utf-16-le
            return 'utf-16-le'
    # default
    return 'utf-8'


class FrontObject:
    def __new__(cls, *args, **kwargs):
        """
        When the first argument is a dict, create a new front object.
        When the first argument is a list, create a new list of front objects.
        Otherwise just return the first argument.
        """
        # todo: is there a way to detect timestamps and automatically convert
        # them to datetime objects?
        if isinstance(args[0], dict):
            return super(FrontObject, cls).__new__(cls)
        elif isinstance(args[0], list):
            return [FrontObject(arg, args[1]) for arg in args[0]]
        return args[0]

    def __init__(self, data: dict, api) -> None:
        self._meta = data.pop('_meta', {})
        self._data = data.pop('data', data)
        self._api = api
        self._pagination = self._data.pop('_pagination', {})

        self.links = self._data.pop('_links', {})
        self.results = [FrontObject(r, api) for r in self._data.pop('_results', [])]
        self.error = self._data.pop('_error', None)

        new_data = {}
        for k, v in self._data.items():
            new_data[k] = FrontObject(v, api)
        self._data = new_data

    def __getattr__(self, item):
        if item in self._data:
            return self._data[item]
        raise AttributeError('no attribute %r' % item)

    def __getitem__(self, item):
        if item in self._data:
            return self._data[item]
        elif isinstance(item, int):
            return self.results[item]
        raise KeyError('no key %r' % item)

    def __iter__(self):
        return iter(self.results)

    def __len__(self):
        return len(self.results)

    def has_error(self) -> bool:
        return self.error is not None

    def next_page(self) -> Optional['FrontObject']:
        next_url = self._pagination.get('next')
        if next_url is not None:
            return self._api._request_url('get', next_url)
        return None

    def has_next_page(self) -> bool:
        return self.next_page() is not None

    def previous_page(self) -> Optional['FrontObject']:
        prev_url = self._pagination.get('prev')
        if prev_url is not None:
            return self._api._request_url('get', prev_url)
        return None

    def has_previous_page(self) -> bool:
        return self.previous_page() is not None

    @classmethod
    def from_bytes(cls, raw: bytes, api) -> 'FrontObject':
        raw = raw.decode(detect_encoding(raw), 'surrogatepass')  # this is to support python 3.5
        data = json.loads(raw)
        return cls(data, api)


def timestamp(dt: datetime) -> float:
    if dt.tzinfo is None:
        raise InvalidTimezoneError()
    return dt.timestamp()

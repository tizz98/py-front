import codecs
import json


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
    def __init__(self, data: dict) -> None:
        self._data = data

        self.links = self._data.pop('_links', {})
        self.results = self.results = [FrontObject(r) for r in self._data.pop('_results', [])]
        self.error = self._data.pop('_error', None)

    def __getattr__(self, item):
        if item in self._data:
            return self._data[item]
        raise AttributeError('no attribute %r' % item)

    def __getitem__(self, item):
        if item in self._data:
            return self._data[item]
        raise KeyError('no key %r' % item)

    def has_error(self) -> bool:
        return self.error is not None

    @classmethod
    def from_bytes(cls, raw: bytes) -> 'FrontObject':
        raw = raw.decode(detect_encoding(raw), 'surrogatepass')  # this is to support python 3.5
        data = json.loads(raw)
        return cls(data)

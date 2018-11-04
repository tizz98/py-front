import json


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
        raw = raw.decode(json.detect_encoding(raw), 'surrogatepass')  # this is to support python 3.5
        data = json.loads(raw)
        return cls(data)
